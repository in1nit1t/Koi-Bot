import time
import random
from datetime import datetime

from core.setting import setting
from core.util import Util, CQHTTP

from service.alapi import AlApi
from service.sign_in import SignIn
from service.bilibili import Bilibili
from service.speak_ranking import speak_ranking

g_history_dynamic = []


class Periodic:

    # INIT SETTINGS
    def __init__(self):
        self.sign_in_flag = True
        self.morning_push_flag = True
        self.speak_ranking_flag = True

        # BILIBILI CONFIG
        self.koi_bilibili = Bilibili(setting["account"]["bilibili"]["koi_uid"])
        self.previous_follower_count = self.koi_bilibili.follower_count()
        self.previous_dynamic_info = self.koi_bilibili.latest_dynamic_info()
        self.notice_config = setting["service"]["group"]["bilibili"]["notice"]

        # SIGN IN REFRESH TIME
        sign_in_config = setting["service"]["group"]["sign_in"]
        self.sign_in_refresh_hour = int(sign_in_config["refresh_time"]["hour"])
        self.sign_in_refresh_minute = int(sign_in_config["refresh_time"]["minute"])

    # BILIBILI DYNAMIC STATUS CHECK
    def dynamic_status_check(self):
        latest_dynamic_info = self.koi_bilibili.latest_dynamic_info()
        if not latest_dynamic_info or self.previous_dynamic_info == latest_dynamic_info or \
                latest_dynamic_info in g_history_dynamic:
            return

        with_screenshot = False
        g_history_dynamic.append(latest_dynamic_info)
        dynamic_id, dynamic_type = latest_dynamic_info
        if dynamic_type == 1 and self.notice_config["new_dynamic_forwarding"]["enable"]:  # DYNAMIC FORWARDING
            msg = "koi转发了一条动态~"
            if self.notice_config["new_dynamic_forwarding"]["with_screenshot"]:
                with_screenshot = True
        elif dynamic_type in [2, 4] and self.notice_config["new_dynamic"]["enable"]:  # DYNAMIC
            msg = "koi发布了新的动态~"
            if self.notice_config["new_dynamic"]["with_screenshot"]:
                with_screenshot = True
        elif dynamic_type == 8 and self.notice_config["new_post"]["enable"]:  # POST
            msg = "koi发布了新的作品~"
            if self.notice_config["new_post"]["with_screenshot"]:
                with_screenshot = True
        else:
            return
        msg += "\n\n"

        # ADD DYNAMIC SCREENSHOT IF ENABLE
        if with_screenshot:
            screenshot_path = Bilibili.dynamic_screenshot(dynamic_id)
            if screenshot_path:
                msg += Util.local_picture_pack(screenshot_path)

        msg += f"传送门 -> {Bilibili.dynamic_base_url}/{dynamic_id}"
        CQHTTP.send_group_message(msg)
        self.previous_dynamic_info = latest_dynamic_info

    # BILIBILI NEW FOLLOWER NOTICE
    def new_follower_notice(self):
        current_follower_count = self.koi_bilibili.follower_count()
        if current_follower_count == -1:
            return
        if self.previous_follower_count < current_follower_count:
            msg = "有新的小可爱关注了koi哟~"

            # ADD NEW FOLLOWER'S INFO
            latest_follower = self.koi_bilibili.latest_follower()
            if latest_follower:
                msg += "\n\n"
                nick_name, face_url = latest_follower
                if self.notice_config["new_follower"]["with_avatar"]:
                    msg += Util.online_picture_pack(face_url)
                msg += f"B站昵称：{nick_name}"
            CQHTTP.send_group_message(msg)
        self.previous_follower_count = current_follower_count

    # MORNING PUSH
    def morning_push(self):
        pre_msg = "哦哈哟米娜桑，美好的一天开始啦~\n"

        # ADD ACG PICTURE
        pic_url = AlApi.acg_picture()
        if pic_url:
            pre_msg += Util.online_picture_pack(pic_url)

        # ADD TODAY IN HISTORY
        time.sleep(1)
        event_list = AlApi.today_in_history()
        if event_list:
            event = random.choice(event_list)
            title, date = event["title"], event["date"]
            pre_msg += f"\n你知道吗？{date[:date.find('年')]}年的今天，{title}。"
        CQHTTP.send_group_message(pre_msg)

        # SEND MORNING PAPER
        time.sleep(1)
        image_url = AlApi.morning_paper()
        if image_url:
            msg = Util.online_picture_pack(image_url.replace("webp", "png"))
            CQHTTP.send_group_message(msg)
        self.morning_push_flag = False

    # SPEAK RANKING
    def rank_speak(self):
        speak_ranking.ranking("today" if datetime.now().weekday() < 6 else "week")
        self.speak_ranking_flag = False

    # REFRESH TODAY'S SIGN IN
    def refresh_sign_in(self):
        SignIn().refresh()
        self.sign_in_flag = False

    # EXECUTE
    def exec(self):
        # BILIBILI STATUS CHECK
        self.dynamic_status_check()
        if self.notice_config["new_follower"]["enable"]:
            self.new_follower_notice()

        # CRON JOB
        now = time.strftime("%H:%M:%S", time.localtime())
        if "08:00:00" <= now < "08:00:30" and self.morning_push_flag:
            self.morning_push()
        if "22:00:00" <= now < "22:00:30" and self.speak_ranking_flag:
            self.rank_speak()
        if "%02d:%02d:00" % (self.sign_in_refresh_hour, self.sign_in_refresh_minute) <= now \
                < "%02d:%02d:30" % (self.sign_in_refresh_hour, self.sign_in_refresh_minute) \
                and self.sign_in_flag:
            self.refresh_sign_in()

        # RECOVERY FLAGS
        if "03:00:00" <= now < "03:00:30":
            self.sign_in_flag = True
            self.morning_push_flag = True
            self.speak_ranking_flag = True
