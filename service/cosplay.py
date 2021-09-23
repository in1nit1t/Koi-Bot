import os
import requests
import traceback

from core.util import Util
from core.logger import logger
from core.setting import setting


class Cosplay:

    api_url = "http://api520.ltd/api/cosplay.php"
    cache_directory = setting["misc"]["cache_directory"]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Alt-Used": "www.moestack.com",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "If-Modified-Since": "Wed, 09 Dec 2020 11:43:28 GMT",
        "If-None-Match": "5fd0b860-52a6d",
        "Cache-Control": "max-age=0",
        "TE": "trailers"
    }

    @staticmethod
    def save_pic():
        try:
            response = requests.get(Cosplay.api_url, timeout=5)
            response = requests.get(response.text, headers=Cosplay.headers, timeout=15)
            file_path = os.path.join(Cosplay.cache_directory, Util.random_string(32) + ".jpg")
            with open(file_path, "wb") as f:
                f.write(response.content)
            return file_path
        except:
            logger.error("<Cosplay> 图片获取失败", traceback.format_exc())
            return ''

    @staticmethod
    def random_picture():
        file_path = Cosplay.save_pic()
        if not file_path:
            return Util.bot_error_response()
        return "收好了捏~" + Util.local_picture_pack(file_path)
