import re

from core.setting import setting
from core.util import Util, CQHTTP

g_group_service_config = setting["service"]["group"]


class BaiLan:

    # MESSAGE REPLY
    @staticmethod
    def msg_reply(raw_message):
        msg = None
        split_message = re.sub(r" +", ' ', raw_message).split(' ')
        command = split_message[0]

        # MENU MODULE
        if command == "菜单":
            msg = "忘了"

        # SIGN IN MODULE
        elif command == "签到" and g_group_service_config["sign_in"]["enable"]:
            msg = "看我干嘛 我又不是签到表"

        # POINTS MODULE
        elif command in ["积分兑换", "兑换清单", "兑换列表"] and g_group_service_config["sign_in"]["enable"]:
            msg = "\n\n\n"

        # SETU MODULE
        elif re.search(r"(涩图|色图|涩涩|色色|setu)", command):
            msg = "要看自己去找 咱懒得动了"

        # MEME SEARCH MODULE
        elif command == "梗百科":
            msg = "!@#$3%*1)9+%*+$7+;/|%"

        # VOICE MODULE
        elif command == "语音":
            CQHTTP.send_group_message(Util.local_voice_pack(Util.get_voice_resource("senpai")))

        # MUSIC MODULE
        elif command == "点歌":
            msg = "啦啦啦（捧读）"

        # TRANSLATE MODULE
        elif command[:2] == "翻译":
            msg = "不会"

        # COSPLAY PICTURE
        elif command.lower() in ["cos", "coser", "cosplay"]:
            msg = "要看自己去找 咱懒得动了"

        # TU WEI QING HUA
        elif command in ["情话", "土味情话", "twqh"]:
            msg = "你是铸币"

        # TIAN GOU RI JI
        elif command in ["日记", "舔狗日记", "tgrj"]:
            msg = "舔到最后一无所有"

        # DU JI TANG
        elif command in ["鸡汤", "毒鸡汤", "djt"]:
            msg = "不喜欢喝鸡汤 不过鸡翅味道挺不错的"

        # HAO HAO SHUO HUA
        elif command == "好好说话":
            msg = "njbsa"

        # JI CHOU
        elif command in ["记仇", "小本本记下来", "这仇我记下了", "这个仇我记下了"]:
            msg = "阿弥陀佛 善哉善哉"

        # AT ME
        elif command == f"[CQ:at,qq={setting['account']['qq']['bot']}]":
            msg = "爪巴"

        # GENERATE INSTRUCTION
        elif re.search(r"^生成(.+?)", raw_message):
            msg = "哔哔...boom...生成失败"

        # SAVE INSTRUCTION
        elif re.search(r"\[CQ:reply,id=(.+?)]\[CQ:at,qq=\d+] 保存", raw_message):
            msg = "存了 但是没完全存"

        # DELETE INSTRUCTION
        elif re.search(r"\[CQ:reply,id=(.+?)]\[CQ:at,qq=\d+] 删除", raw_message):
            msg = "删了 但是没完全删"

        elif raw_message in ["摆烂模式", "开始摆烂"]:
            msg = "在摆了在摆了（流汗黄豆）"

        return msg
