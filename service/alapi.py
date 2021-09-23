import time
import random

from core.setting import setting
from core.decorator import Decorator


class AlApi:

    token = setting["api"]["alapi"]["token"]

    # API: TU WEI QING HUA
    # REFERENCE: https://www.alapi.cn/api/view/98
    @staticmethod
    @Decorator.alapi_fetch("qinghua", "content")
    def tu_wei_qing_hua():
        params = {
            "token": AlApi.token,
            "format": "json"
        }
        return params

    # API: TIAN GOU RI JI
    # REFERENCE: https://www.alapi.cn/api/view/3
    @staticmethod
    @Decorator.alapi_fetch("dog", "content")
    def tian_gou_ri_ji():
        params = {
            "token": AlApi.token,
            "format": "json"
        }
        return params

    # API: DU JI TANG
    # REFERENCE: https://www.alapi.cn/api/view/2
    @staticmethod
    @Decorator.alapi_fetch("soul", "content")
    def du_ji_tang():
        params = {
            "token": AlApi.token,
            "format": "json"
        }
        return params

    # API: HAO HAO SHUO HUA
    # REFERENCE: https://www.alapi.cn/api/view/99
    @staticmethod
    @Decorator.alapi_fetch("abbr", "explain")
    def hao_hao_shuo_hua(abbr):
        params = {
            "token": AlApi.token,
            "abbr": abbr
        }
        return params

    # API: CANG TOU SHI
    # REFERENCE: https://www.alapi.cn/api/view/48
    @staticmethod
    @Decorator.alapi_fetch("poem", "poem")
    def cang_tou_shi(keyword, num, _type):
        params = {
            "token": AlApi.token,
            "keyword": keyword,
            "num": num,
            "type": _type,
            "rhyme": random.randint(1, 3)
        }
        return params

    # API: ACG PICTURE
    # REFERENCE: https://www.alapi.cn/api/view/9
    @staticmethod
    @Decorator.alapi_fetch("acg", "url")
    def acg_picture():
        params = {
            "token": AlApi.token,
            "format": "json"
        }
        return params

    # API: TODAY IN HISTORY
    # REFERENCE: https://www.alapi.cn/api/view/17
    @staticmethod
    @Decorator.alapi_fetch("eventHistory")
    def today_in_history():
        params = {
            "token": AlApi.token,
            "monthday": time.strftime("%m%d")
        }
        return params

    # API: MORNING PAPER
    # REFERENCE: https://www.alapi.cn/api/view/93
    @staticmethod
    @Decorator.alapi_fetch("zaobao", "image")
    def morning_paper():
        params = {
            "token": AlApi.token,
            "format": "json"
        }
        return params
