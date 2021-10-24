import os
import re
import time
import html
import json
import random
import base64
import string
import traceback
import threading
import collections
from PIL import Image
from io import BytesIO

from core.logger import logger
from core.setting import setting
from core.decorator import Decorator


class Util:

    # CONVERT REQUEST CONTENT TO JSON FORMAT
    @staticmethod
    def request2json(req: str) -> dict:
        try:
            return json.loads(req[req.find('{'):])
        except:
            logger.error('', traceback.format_exc(), False)
            return {}

    # PACK HTTP RESPONSE HEAD
    @staticmethod
    def response_head_pack(status: int, headers: dict) -> str:
        head = "HTTP/1.1 "
        if status == 200:
            head += "200 OK"
        elif status == 500:
            head += "500 Internal Server Error"
        for key, value in headers.items():
            head += f"\r\n{key}: {value}"
        head += "\r\n\r\n"
        return head

    # LOAD JSON FILE
    @staticmethod
    def load_json(file_path: str) -> str:
        try:
            with open(file_path, encoding="utf-8") as f:
                return json.loads(f.read())
        except:
            logger.error(f"<Util> 加载 json 文件 [{file_path}] 失败", traceback.format_exc())
            return ''

    # PARSE UNICODE
    @staticmethod
    def unicode_decode(raw: str) -> str:
        return raw.encode("utf-8").decode("unicode-escape")

    # GET RANDOM STRING
    @staticmethod
    def random_string(length: int) -> str:
        return ''.join(random.sample(string.ascii_letters + string.digits, length))

    # CONVERT PICTURE TO BASE64 (PILLOW)
    @staticmethod
    def picture2base64(picture: Image) -> str:
        buffer = BytesIO()
        picture.save(buffer, format="png")
        return base64.b64encode(buffer.getvalue()).decode()

    # CALL FUNCTION AT PROBABILITY
    @staticmethod
    def run_at_probability(probability: int, func, *args) -> tuple:
        if probability == 0:
            return False, None
        lst = [1 for _ in range(probability)] + [0 for _ in range(100 - probability)]
        if random.choice(lst) == 1:
            return True, func(*args)
        return False, None

    # GET VOICE RESOURCE PATH
    @staticmethod
    def get_voice_resource(whom):
        voice_directory = f"./resource/voice/{whom}/"
        voice = random.choice(os.listdir(voice_directory))
        return os.path.abspath(os.path.join(voice_directory, voice))

    # GET IMAGE RESOURCE PATH
    @staticmethod
    def get_image_resource(image_type: str, filename: str) -> str:
        relative_path = f"./resource/image/{image_type}/{filename}"
        return os.path.abspath(relative_path)

    # GET IMAGE RESOURCE DIR
    @staticmethod
    def get_image_resource_dir(image_type: str):
        relative_path = f"./resource/image/{image_type}"
        return os.path.abspath(relative_path)

    # GET FONT RESOURCE PATH
    @staticmethod
    def get_font_resource(font_name: str) -> str:
        relative_path = f"./resource/font/{font_name}"
        return os.path.abspath(relative_path)

    # GET GOODS RESOURCE PATH
    @staticmethod
    def get_goods_resource(goods_name: str) -> str:
        relative_path = f"./resource/goods/{goods_name}"
        return os.path.abspath(relative_path)

    # LOAD CORPORA RESOURCE
    @staticmethod
    def load_corpora_resource(rsc_name: str) -> dict or None:
        return Util.load_json(f"./resource/corpora/{rsc_name}.json")

    # LOAD SCRIPT RESOURCE
    @staticmethod
    def load_script_resource(script_name: str) -> str:
        script_path = f"./resource/script/{script_name}"
        with open(script_path, encoding="utf-8") as f:
            return f.read()

    # LOAD MISC RESOURCE
    @staticmethod
    def load_misc_resource(rsc_name: str) -> str:
        rsc_path = f"./resource/misc/{rsc_name}"
        with open(rsc_path, encoding="utf-8") as f:
            return f.read()

    # CHECK IF IS VOICE MESSAGE
    @staticmethod
    def is_voice_message(message: str) -> bool:
        return re.search(r"\[CQ:record,(.+?)]", message) is not None

    # VOICE MESSAGE EXTRACT
    @staticmethod
    def voice_message_extract(message: str) -> tuple:
        params = re.search(r"\[CQ:record,(.+?)]", message).group(1) + ','
        try:
            filename = re.search(r"file=(.+?),", params).group(1)
        except:
            return tuple()
        try:
            url = html.unescape(re.search(r"url=(.+?),", params).group(1))
            return filename, url
        except:
            return filename, ''

    # PACK AT MESSAGE
    @staticmethod
    def at_pack(raw_message: str, to: str) -> str:
        return f"[CQ:at,qq={to}] {raw_message}"

    # PACK REPLY MESSAGE
    @staticmethod
    def reply_pack(raw_message: str, reply_mid: str, to: str) -> str:
        return f"[CQ:reply,id={reply_mid}][CQ:at,qq={to}] {raw_message}"

    # PACK REPLY & AT MESSAGE
    @staticmethod
    def reply_at_pack(raw_message: str, reply_mid: str, to: str) -> str:
        return f"[CQ:reply,id={reply_mid}][CQ:at,qq={to}] {Util.at_pack(raw_message, to)}"

    # PACK ONLINE PICTURE MESSAGE
    @staticmethod
    def online_picture_pack(pic_url: str) -> str:
        return f"[CQ:image,file={pic_url}]"

    # PACK LOCAL PICTURE MESSAGE
    @staticmethod
    def local_picture_pack(pic_location: str) -> str:
        return f"[CQ:image,file=file:///{pic_location}]"

    # PACK BASE PICTURE MESSAGE
    @staticmethod
    def base64_picture_pack(b64: str) -> str:
        return f"[CQ:image,file=base64://{b64}]"

    # PACK ONLINE VOICE MESSAGE
    @staticmethod
    def online_voice_pack(filename: str) -> str:
        return f"[CQ:record,file={filename}]"

    # PACK LOCAL VOICE MESSAGE
    @staticmethod
    def local_voice_pack(filename: str) -> str:
        return f"[CQ:record,file=file:///{filename}]"

    # PACK NETEASE CLOUD MUSIC
    @staticmethod
    def music_163_pack(sid: str) -> str:
        return f"[CQ:music,type=163,id={sid}]"

    # PACK CUSTOM MUSIC
    @staticmethod
    def music_custom_music_pack(audio_url: str, title: str, content: str = '', img_url: str = ''):
        return f"[CQ:music,type=custom,url=https://space.bilibili.com/210127180,audio={audio_url}," \
               f"title={title},content={content},image={img_url}] "

    # PACK POCK MESSAGE
    @staticmethod
    def poke_pack(to: str) -> str:
        return f"[CQ:poke,qq={to}]"

    # AT MESSAGE EXTRACT
    @staticmethod
    def at_extract(raw_message: str) -> str:
        result = re.search(r"\[CQ:at,qq=(.+?)]", raw_message)
        return result.group(1) if result else ''

    # CHECK IF IS FRIEND
    @staticmethod
    def is_friend(target_uin: str) -> bool:
        friend_list = CQHTTP.get_friend_list()
        return re.search(f"'user_id': {target_uin}", str(friend_list)) is not None

    # CHECK IF CAN AT ALL
    @staticmethod
    def can_at_all() -> bool:
        data = CQHTTP.group_at_all_remain()
        if data:
            return data["can_at_all"] and data["remain_at_all_count_for_uin"] > 0
        return False

    # CHECK IF USER IS ADMIN / OWNER
    @staticmethod
    def has_high_privilege(uin: str) -> bool:
        user_info = CQHTTP.group_member_info(uin)
        if user_info:
            return user_info["role"] in ["admin", "owner"]
        return False

    # NOTICE ADMIN
    @staticmethod
    def notice_admin(msg: str) -> None:
        CQHTTP.send_private_message(msg, setting["account"]["qq"]["admin"])

    # GET A RANDOM ERROR RESPONSE
    @staticmethod
    def bot_error_response() -> str:
        seq = [
            "咦 好像哪里出错了Σ(ﾟдﾟlll)",
            "忒嘿 好像粗了一小小小点问题（逃",
        ]
        return random.choice(seq)

    # GET A RANDOM INVALID INPUT RESPONSE
    @staticmethod
    def bot_invalid_input_response() -> str:
        seq = [
            "再乱输我要生气啦[○･｀Д´･ ○]",
            "别戏弄我啦，真是的ヽ(●-`Д´-)ノ",
        ]
        return random.choice(seq)


class CQHTTP:

    # GET MESSAGE THROUGH ID
    @staticmethod
    @Decorator.cqhttp_api("get_msg")
    def get_message(message_id: str) -> dict:
        return {"message_id": message_id}

    # GET FRIEND LIST
    @staticmethod
    @Decorator.cqhttp_api("get_friend_list")
    def get_friend_list():
        return dict()

    @staticmethod
    @Decorator.cqhttp_api("get_stranger_info")
    def get_stranger_info(uin):
        return {"user_id": uin}

    # SEND GROUP MESSAGE
    @staticmethod
    @Decorator.cqhttp_api("send_msg")
    def send_group_message(msg: str, group_uin: str = setting["account"]["qq"]["target_group"]) -> dict:
        params = {
            "message": msg,
            "group_id": group_uin,
            "auto_escape": False
        }
        return params

    # SEND PRIVATE MESSAGE
    @staticmethod
    @Decorator.cqhttp_api("send_msg")
    def send_private_message(msg: str, to: str) -> dict:
        params = {
            "message": msg,
            "user_id": to,
            "auto_escape": False
        }
        return params

    # GET GROUP MEMBER INFO
    @staticmethod
    @Decorator.cqhttp_api("get_group_member_info")
    def group_member_info(uin: str) -> dict:
        params = {
            "group_id": str(setting["account"]["qq"]["target_group"]),
            "user_id": uin
        }
        return params

    # GET AT ALL REMAIN
    @staticmethod
    @Decorator.cqhttp_api("get_group_at_all_remain")
    def group_at_all_remain() -> dict:
        return {"group_id": str(setting["account"]["qq"]["target_group"])}

    # BAN SINGLE USER
    @staticmethod
    @Decorator.cqhttp_api("set_group_ban")
    def ban_single_user(user_id: str, duration: int) -> dict:
        params = {
            "group_id": str(setting["account"]["qq"]["target_group"]),
            "user_id": user_id,
            "duration": duration
        }
        return params

    # SET FRIEND ADD REQUEST
    @staticmethod
    @Decorator.cqhttp_api("set_friend_add_request")
    def set_friend_add_request(flag: str, approve: bool, remark: str = '') -> dict:
        params = {
            "flag": flag,
            "approve": approve,
            "remark": remark
        }
        return params


# COUNT TIMES, THREAD SAFE
class Counter:

    # INIT SETTINGS
    def __init__(self, limit: int) -> None:
        self.lock = threading.Lock()
        self.limit = limit if limit > 0 else 1
        self.dict = collections.defaultdict(int)

    # COUNT AND CHECK COUNT LIMIT
    def count(self, key: int or str) -> int:
        self.lock.acquire()
        self.dict[key] += 1
        ret = self.dict[key] >= self.limit
        self.lock.release()
        return ret

    # SET COUNT
    def set(self, key: int or str, value: int) -> None:
        self.lock.acquire()
        self.dict[key] = value
        self.lock.release()

    # RESET COUNT
    def reset(self, key: int or str) -> None:
        self.lock.acquire()
        self.dict[key] = 0
        self.lock.release()


# SET CLOCK
class Clock:

    # INIT SETTINGS
    def __init__(self, seconds: int) -> None:
        self.alarm_time = int(time.time()) + seconds

    # CHECK IF TIMEOUT
    def is_timeout(self):
        return int(time.time()) >= self.alarm_time
