import os
import random
import requests
import traceback
import threading
from lxml import etree
from typing import Tuple

from core.util import Util
from core.logger import logger
from core.setting import setting


class Cosplay:

    base_url = "https://www.moestack.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "TE": "trailers",
        "Connection": "close"
    }

    # GET RANDOM PICTURE
    @staticmethod
    def random_pic() -> str:
        image_dir = Util.get_image_resource_dir("cosplay")
        cosplay_dir = os.listdir(image_dir)
        if not cosplay_dir:
            return "图库中还没有图片捏~"

        random_dir = os.path.join(image_dir, random.choice(cosplay_dir))
        pics = os.listdir(random_dir)
        if not pics:
            return Util.bot_error_response()
        return Util.local_picture_pack(os.path.join(random_dir, random.choice(pics)))

    # SAVE PICTURE THREAD
    class _SavePicThread(threading.Thread):

        # INIT SETTINGS
        def __init__(self, args) -> None:
            super().__init__()
            self.args = args
            self.thread_result = -1

        # GET THREAD RESULT
        def get_result(self) -> int:
            # 0: FAILED
            # 1: SUCCESS
            # 2: ALREADY SAVED
            return self.thread_result

        # OVERRIDE
        def run(self) -> None:
            save_path, pic_url = self.args

            # ALREADY SAVED
            if os.path.exists(save_path):
                self.thread_result = 2
                return

            try:
                response = requests.get(pic_url, headers=Cosplay.headers, timeout=20)
                if response.status_code == 200:
                    with open(save_path, "wb") as f:
                        f.write(response.content)
                    self.thread_result = 1
                    logger.success(f"<Cosplay> 保存图片 [{pic_url}] 成功")
                else:
                    logger.warning('', f"<Cosplay> 保存图片 [{pic_url}] 出错，响应码{response.status_code}")
                    self.thread_result = 0
            except:
                logger.error("<Cosplay> 图片获取失败", traceback.format_exc(), False)
                self.thread_result = 0

    # DOWNLOAD PICTURES IN ONE ALBUM
    @staticmethod
    def download_album(album_url: str) -> Tuple[bool, int]:
        try:
            response = requests.get(album_url, headers=Cosplay.headers, timeout=20)
            tree = etree.HTML(response.text)

            # GET ALBUM TITLE & CREATE DIR
            title = tree.xpath("//*[@class='entry-title']/text()")[0].replace('[', '').replace(']', '')
            save_dir = os.path.join(Util.get_image_resource_dir("cosplay"), title)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            # SAVE PICTURES
            pools = []
            pic_urls = tree.xpath("//*/div[2]/div/div[1]/p/img/@src")
            for pic_url in pic_urls:
                save_path = os.path.join(save_dir, pic_url.split('/')[-1])
                t = Cosplay._SavePicThread((save_path, pic_url))
                pools.append(t)
            for t in pools:
                t.start()
            for t in pools:
                t.join()

            thread_results = [t.get_result() for t in pools]
            return all(thread_results), thread_results.count(1)
        except:
            logger.error(f"<Cosplay> 获取相册 [{album_url}] 失败", traceback.format_exc(), False)
            return False, 0

    # GET ALBUM URLS IN PAGES
    @staticmethod
    def page_get_album_urls(page_num: int) -> list:
        try:
            response = requests.get(
                f"{Cosplay.base_url}/all/page/{page_num}?order=date",
                headers=Cosplay.headers,
                timeout=20
            )
            tree = etree.HTML(response.text)
            return tree.xpath("//*[@class='entry-media']/div/a/@href")
        except:
            logger.error(f"<Cosplay> 获取页面{page_num}中的专题URL失败", traceback.format_exc(), False)
            return []

    # GET PAGE COUNT
    @staticmethod
    def get_page_count() -> int:
        try:
            response = requests.get(f"{Cosplay.base_url}/all?order=date", headers=Cosplay.headers, timeout=20)
            tree = etree.HTML(response.text)
            return int(tree.xpath("/html/body/div/div[3]/div/div[2]/div/div/main/div[2]/ul/li[6]/a/text()")[0])
        except:
            logger.error("<Cosplay> 获取页面数失败", traceback.format_exc(), False)
            return 0

    # UPDATE COSPLAY PICTURE
    @staticmethod
    def update_pic() -> bool:
        pic_success_count = 0
        album_success_count = 0
        album_download_failed = []
        page_get_album_urls_failed = []

        # GET PAGE COUNT FIRST
        page_count = Cosplay.get_page_count()
        if not page_count:
            return False

        # GO THROUGH ALL PAGES & DOWNLOAD ALBUMS
        Util.notice_admin(f"萌栈当前共有{page_count}页，准备开始更新图库")
        for page_num in range(1, page_count + 1):
            album_urls = Cosplay.page_get_album_urls(page_num)
            if album_urls:
                for album_url in album_urls:
                    success, downloaded_count = Cosplay.download_album(album_url)
                    if success:
                        if downloaded_count:
                            album_success_count += 1
                            pic_success_count += downloaded_count
                            logger.success(f"<Cosplay> 相册 [{album_url}] 下载完毕")
                        else:
                            logger.info(f"<Cosplay 相册 [{album_url}] 曾被缓存>")
                    else:
                        album_download_failed.append(album_url)
                        logger.warning('', f"<Cosplay> 相册 [{album_url}] 下载未完成")
            else:
                page_get_album_urls_failed.append(page_count)

        msg = f"更新完成，本次共更新{album_success_count}个相册，{pic_success_count}张图片"
        if page_get_album_urls_failed:
            msg += f"\n{'-' * 20}\n页面 {str(page_get_album_urls_failed)[1:-1]} 爬取失败"

        if album_download_failed:
            msg += f"\n{'-' * 20}\n下列相册爬取失败：\n"
            for idx, failed in enumerate(album_download_failed):
                msg += f"\n{idx + 1}. {failed}"
        Util.notice_admin(msg)
