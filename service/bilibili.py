import os
import time
import traceback
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from core.util import Util
from core.logger import logger
from core.setting import setting
from core.decorator import Decorator


class Bilibili:

    dynamic_base_url = "https://t.bilibili.com"
    basic_status_url = "https://api.bilibili.com/x/relation/stat"
    followers_url = "https://api.bilibili.com/x/relation/followers"
    detail_status_url = "https://api.bilibili.com/x/space/acc/info"
    space_history_url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history"

    # INIT SETTINGS
    def __init__(self, uid):
        self.uid = uid

    # GET BASIC STATUS
    @Decorator.bilibili_fetch(basic_status_url)
    def api_basic_status(self):
        return {"vmid": self.uid}

    # GET DETAIL STATUS
    @Decorator.bilibili_fetch(detail_status_url)
    def api_detail_status(self):
        return {"mid": self.uid}

    # GET SPACE HISTORY
    @Decorator.bilibili_fetch(space_history_url)
    def api_space_history(self, offset_did):
        params = {
            "visitor_uid": 0,
            "host_uid": self.uid,
            "offset_dynamic_id": offset_did
        }
        return params

    # GET FOLLOWERS
    @Decorator.bilibili_fetch(followers_url)
    def api_follower(self, page, per_page, order="desc"):
        params = {
            "vmid": self.uid,
            "pn": page,
            "ps": per_page,
            "order": order
        }
        return params

    # GET DYNAMIC SCREENSHOT BY ID
    @staticmethod
    def dynamic_screenshot(dynamic_id):
        # GET PAGE
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        driver_path = setting["misc"]["executable_path"]["chrome_driver"]
        try:
            driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)
            driver.set_page_load_timeout(500)
            driver.get(f"{Bilibili.dynamic_base_url}/{dynamic_id}")

            # FIND ELEMENTS & AVOID UNLOGIN POPUP
            unlogin_avatar = driver.find_element_by_xpath("//div[@class='unlogin-avatar']")
            card = driver.find_element_by_xpath(f"//div[@data-did='{dynamic_id}']")
            card_content = card.find_elements_by_class_name("card-content")[0]
            # panel_area = driver.find_element_by_xpath("//div[@class='panel-area']")
            ActionChains(driver).move_to_element(unlogin_avatar).move_to_element(card).perform()
            time.sleep(0.3)

            # RESET WINDOW SIZE
            width = driver.execute_script("return document.documentElement.scrollWidth")
            height = driver.execute_script("return document.documentElement.scrollHeight")
            driver.set_window_size(width, height)
            time.sleep(0.1)

            # SAVE SCREENSHOT
            cache_directory = setting["misc"]["cache_directory"]
            save_path = os.path.join(cache_directory, Util.random_string(32)) + ".png"
            driver.save_screenshot(save_path)
        except:
            logger.error(f"<Bilibili> {dynamic_id} 全屏幕截图失败", traceback.format_exc())
            return False

        # CROP SCREENSHOT
        left = card.location['x'] + 7
        top = card.location['y'] + 5
        right = card.location['x'] + card.size["width"]
        # bottom = panel_area.location['y']
        bottom = card_content.location['y'] + card_content.size["height"] + 7
        try:
            image = Image.open(save_path)
            image = image.crop((left, top, right, bottom))
            image.save(save_path)
        except:
            logger.error(f"<Bilibili> {dynamic_id} 图片裁剪失败", traceback.format_exc())
            return False
        driver.close()
        return save_path

        # GET FOLLOWER COUNT
    def follower_count(self):
        status = self.api_basic_status()
        return status["follower"] if status else -1

    # GET LATEST FOLLOWER'S INFO
    def latest_follower(self):
        follower = self.api_follower(1, 1)

        # ERROR HAPPENED
        if not follower:
            return False

        # DON'T HAVE FOLLOWER
        follower_list = follower["list"]
        if not follower_list:
            return None

        latest_follower = follower_list[0]
        return latest_follower["uname"], latest_follower["face"]

    # GET LATEST DYNAMIC INFO
    def latest_dynamic_info(self):
        history = self.api_space_history(0)

        # ERROR HAPPENED
        if not history:
            return False

        # DON'T HAVE DYNAMIC
        cards = history["cards"]
        if not cards:
            return None

        description = cards[0]["desc"]
        return description["dynamic_id_str"], description["type"]

    # GET LIVE STATUS
    def is_living(self):
        status = self.api_detail_status()
        return status["live_room"]["liveStatus"] if status else False

    # GET USER AVATAR
    def get_avatar_url(self):
        status = self.api_detail_status()
        return status["face"] if status else ''
