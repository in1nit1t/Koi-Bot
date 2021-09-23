import requests
import traceback

from core.logger import logger
from core.util import Util, CQHTTP
from dao.setu import SetuDAO


class Setu:

    # INIT SETTINGS
    def __init__(self, pid=0, quality="small", r18=0, tag=""):
        self.pid = pid
        self.r18 = r18
        self.tag = tag
        self.quality = quality
        self.setu_dao = SetuDAO()

    # GET ORIGINAL QUALITY
    def original_picture(self):
        res = self.setu_dao.select(self.pid)
        if res:
            # FOUND, HINT FIRST
            CQHTTP.send_group_message("原⚡画⚡很⚡大⚡你⚡要⚡等⚡一⚡下")
            ret = f"{Util.online_picture_pack(res[1])}高清大♂图 收好了哟~"
        elif res is None:
            # PICTURE NOT FOUND
            ret = "讨厌 人家没有这条记录啦>w<"
        else:
            logger.warning(f"<setu> SQL 查询失败", f"查询 {self.pid} 原图时发生错误")
            ret = Util.bot_error_response()
        return ret

    # FETCH NEW SETU
    def new_setu(self):
        try:
            # GET SETU INFO THROUGH API
            api_url = "https://api.lolicon.app/setu/v2"
            params = {
                "r18": self.r18,
                "tag": self.tag,
                "size": ["original", "small"]
            }
            response = requests.get(api_url, params=params).json()

            # DATA IS NOT EMPTY
            if response["data"]:
                # PARSE VALUES
                setu_info = response["data"][0]
                pid = setu_info["pid"]
                urls = setu_info["urls"]
                title = setu_info["title"]
                author = setu_info["author"]

                # SAVE BOTH PATH TO DATABASE
                self.setu_dao.insert(pid, urls["small"], urls["original"])

                # BUILD RAW RESPONSE
                ret = f"标题：{title}{Util.online_picture_pack(urls[self.quality])}pid：{pid} 画师：{author}"
            else:
                # PICTURE NOT FOUND
                ret = "对不起主人 没能找到您想要的图片 我真的好笨QAQ"
            return ret
        except:
            logger.error("<setu> 获取新图失败", traceback.format_exc())
            return Util.bot_error_response()

    # GET SETU RAW RESPONSE
    def exec(self):
        if self.pid:
            return self.original_picture()
        else:
            return self.new_setu()
