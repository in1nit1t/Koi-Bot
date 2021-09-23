import re
import random
import hashlib
import requests

from core.setting import setting


# REFERENCE: https://api.fanyi.baidu.com/doc/21
class BaiduTranslate:

    config = setting["api"]["baidu_translate"]
    api_url = "https://api.fanyi.baidu.com/api/trans/vip/translate"
    lang_map = {
        "中文": "zh", "英语": "en", "粤语": "yue", "文言文": "wyw", "日语": "jp", "繁体中文": "cht",
        "俄语": "ru", "葡萄牙语": "pt", "德语": "de", "意大利语": "it", "希腊语": "el", "韩语": "kor",
        "法语": "fra", "西班牙语": "spa", "泰语": "th", "阿拉伯语": "ara", "荷兰语": "nl", "波兰语": "pl",
        "保加利亚语": "bul", "爱沙尼亚语": "est", "丹麦语": "dan", "芬兰语": "fin", "捷克语": "cs",
        "罗马尼亚语": "rom", "斯洛文尼亚语": "slo", "匈牙利语": "hu", "越南语": "vie"
    }
    error_map = {
        "52001": "请求超时，请重试",
        "52002": "系统错误，请重试",
        "54003": "访问频率受限，请降低调用频率",
        "54004": "账户余额不足，请前往管理控制台为账户充值",
        "54005": "访问频率受限，请降低调用频率",
        "58001": "译文语言方向不支持，检查译文语言是否在语言列表里"
    }

    # INIT SETTINGS
    def __init__(self, query):
        query = re.sub("(\r\n)+", ' ', query)
        self.query = re.sub("\n+", ' ', query)

        # API CONFIG
        self.appid = self.config["appid"]
        self.secret_key = self.config["secret_key"]

    # LANGUAGE MAPPING
    def language_mapping(self, raw):
        if self.lang_map.__contains__(raw):
            return self.lang_map[raw]
        return ''
    # GENERATE QUERY SIGN
    def generate_sign(self, salt):
        plain = f"{self.appid}{self.query}{salt}{self.secret_key}"
        return salt, hashlib.md5(plain.encode()).hexdigest()

    # FETCH TRANSLATION THROUGH API
    def do_translation(self, lang_dst):
        salt = random.randint(100000, 999999)
        params = {
            'q': self.query,
            "from": "auto",
            "to": lang_dst,
            "appid": self.appid,
            "salt": salt,
            "sign": self.generate_sign(salt)
        }

        # CALL API
        response = requests.get(url=self.api_url, params=params).json()
        try:
            lang_src = response["from"]
            translated = response["trans_result"][0]["dst"]
            return lang_src, translated
        except:
            # ERROR OCCURRED
            error_code = response["error_code"]
            if self.error_map.__contains__(error_code):
                error_hint = self.error_map[error_code]
            else:
                error_hint = ''
            return None, error_hint

    # OTHER LANGUAGES -> CHINESE
    def to_chinese(self):
        lang_src, translated = self.do_translation("zh")
        if lang_src == "zh":
            return False
        return translated

    # TO OTHER LANGUAGES
    def to_others(self, target):
        lang_dst = self.language_mapping(target)
        if not lang_dst:
            lang_list = '，'.join(self.lang_map.keys())
            return f"暂不支持 <{target}>，目前支持的语种有：\n{lang_list}"

        lang_src, translated = self.do_translation(lang_dst)
        if lang_src == lang_dst:
            return False
        return translated
