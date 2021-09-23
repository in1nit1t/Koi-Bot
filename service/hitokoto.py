import requests
import traceback

from core.logger import logger


class Hitokoto:

    api_url = "https://v1.hitokoto.cn"

    # GET RANDOM SENTENCE
    @staticmethod
    def random_sentence() -> tuple:
        try:
            response = requests.get(url=Hitokoto.api_url).json()
        except:
            logger.error("<一言> 接口调用失败", traceback.format_exc())
            return None, None
        return response["hitokoto"], response["from"]
