import re
import random
import threading
from threading import Thread

from core.setting import setting
from core.util import Util, Clock, CQHTTP
from dao.voice import VoiceDAO
from service.menu import Menu
from service.setu import Setu
from service.atme import AtMe
from service.voice import Voice
from service.music import Music
from service.alapi import AlApi
from service.goods import Goods
from service.bailan import BaiLan
from service.sign_in import SignIn
from service.cosplay import Cosplay
from service.meme_search import MemeSearch
from service.generator.jichou import JiChou
from service.generator.juejuezi import JueJueZi
from service.translate import BaiduTranslate
from service.speak_ranking import speak_ranking

# SERVICE CONFIG
g_group_service_config = setting["service"]["group"]
g_auto_save_config = g_group_service_config["auto_save"]
g_group_msg_ctx_config = g_group_service_config["message_context"]

# FUDU GLOBAL VARIABLE
g_fudu_count = 0
g_last_fudu = ''
g_previous_msg = ''
g_fudu_lock = threading.Lock()

# BAI LAN NODE
g_bai_lan_flag = False
g_bai_lan_clock = None
g_bai_lan_lock = threading.Lock()


class MessageHandler(Thread):

    # FREQUENTLY USED CONFIG
    fudu_limit_count = g_group_msg_ctx_config["fudu_limit_count"]
    bai_lan_mode_enable = g_group_msg_ctx_config["bai_lan_mode"]["enable"]

    # ACCOUNT INFO
    koi_qq = int(setting["account"]["qq"]["koi"])
    target_group = int(setting["account"]["qq"]["target_group"])

    # INIT SETTINGS
    def __init__(self, content):
        super().__init__()
        self.setDaemon(True)

        # RESTORE PROPERTY
        self.message = content["message"]
        self.message_id = content["message_id"]
        self.message_type = content["message_type"]
        self.sender_uin = content["sender"]["user_id"]
        self.raw_message = content["raw_message"].strip()
        self.group_uin = content["group_id"] if content.__contains__("group_id") else ''
        self.anonymous = content["anonymous"] if content.__contains__("anonymous") else ''

        # LOAD RESOURCE
        self.msg_ctx_corpora = Util.load_corpora_resource("message_context")

    # CHECK IF USER IS BOT ADMIN
    def is_bot_admin(self):
        return str(self.sender_uin) == str(setting["account"]["qq"]["admin"])

    # CHECK IF IS A EXCHANGE COMMAND
    def is_exchange_command(self):
        return re.search(r"^兑换.+", self.raw_message)

    # CHECK IF IS A GENERATE COMMAND
    def is_generate_command(self):
        return re.search(r"^生成.+", self.raw_message)

    # CHECK IF IS A SAVE MESSAGE COMMAND
    def is_save_command(self):
        cq_code = re.search(r"\[CQ:reply,id=(.+?)]\[CQ:at,qq=\d+] 保存", self.raw_message)
        return cq_code.group(1) if cq_code else ''

    # CHECK IF IS A DELETE MESSAGE COMMAND
    def is_delete_command(self):
        cq_code = re.search(r"\[CQ:reply,id=(.+?)]\[CQ:at,qq=\d+] 删除", self.raw_message)
        return cq_code.group(1) if cq_code else ''

    # CHECK IF IS A COMMAND
    def is_command(self):
        raw_message = re.sub(r" +", ' ', self.raw_message).split(' ')
        command = raw_message[0]

        return command == "菜单" or command == "签到" or command in ["查询签到", "签到情况", "签到查询"] or \
            command in ["积分兑换", "兑换清单", "兑换列表"] or self.is_exchange_command() or \
            command in ["积分查询", "查询积分"] or re.search(r"(涩图|色图|涩涩|色色|setu)", command) or \
            command == "梗百科" or command == "语音" or \
            command == "点歌" or command[:2] == "翻译" or command.lower() in ["cos", "coser", "cosplay"] or \
            command in ["情话", "土味情话", "twqh"] or command in ["日记", "舔狗日记", "tgrj"] or \
            command in ["鸡汤", "毒鸡汤", "djt"] or command == "好好说话" or \
            command in ["记仇", "小本本记下来", "这仇我记下了", "这个仇我记下了"] or \
            command == f"[CQ:at,qq={setting['account']['qq']['bot']}]" or self.is_generate_command() or \
            self.is_save_command() or self.is_delete_command()

    # GENERATE COMMAND
    def generate(self, gen_type, param):
        if gen_type == "绝绝子":
            return JueJueZi.generate(param) if param else JueJueZi.random_generate()

    # AUTO SAVE CHECK
    def auto_save_check(self):
        # VOICE
        if g_auto_save_config["voice"]["enable"] and Util.is_voice_message(self.raw_message):
            uin_list = g_auto_save_config["voice"]["target_qq"]
            if self.sender_uin in uin_list:
                voice_params = Util.voice_message_extract(self.message)
                if voice_params:
                    return VoiceDAO().record_voice(self.message_id, self.sender_uin, voice_params, '')

    # SAVE PREVIOUS MESSAGE
    def save_previous_message(self, message_id, arg):
        previous_message = CQHTTP.get_message(message_id)
        if previous_message:
            raw_message = previous_message["raw_message"]
            sender_uin = previous_message["sender"]["user_id"]

            # CASE VOICE
            if Util.is_voice_message(raw_message):
                voice_dao = VoiceDAO()

                # ALREADY SAVED
                voice = voice_dao.select_voice_by_message_id(message_id)
                if voice:
                    if arg:
                        ret = voice_dao.update_tag_by_message_id(message_id, arg)
                        return "标签更新成功☆" if ret else Util.bot_error_response()
                    else:
                        return "这条语音已经被保存过啦~"

                # DO SAVE
                voice_params = Util.voice_message_extract(raw_message)
                if voice_params:
                    vid = voice_dao.record_voice(message_id, sender_uin, voice_params, arg)
                    if vid:
                        return f"语音保存成功，id为{vid}"
                return Util.bot_error_response()
        else:
            return Util.bot_error_response()

    # DELETE SAVED MESSAGE
    def delete_previous_message(self, message_id):
        previous_message = CQHTTP.get_message(message_id)
        if previous_message:
            raw_message = previous_message["raw_message"]

            # CASE VOICE
            if Util.is_voice_message(raw_message):
                voice_dao = VoiceDAO()
                voice = voice_dao.select_voice_by_message_id(message_id)
                if voice:
                    if voice_dao.delete_voice_by_message_id(message_id):
                        return "语音删除成功★"
                    return Util.bot_error_response()
                return "这条语音没有被保存过哟~"
        else:
            return Util.bot_error_response()

    # DO SETU SERVICE
    def setu(self, raw_message, r18=0):
        if len(raw_message) > 1:
            # WITH PARAMETER
            try:
                # GET EXACT ORIGINAL PICTURE WITH PID
                pid = int(raw_message[1])
                setu = Setu(pid=pid, quality="original")
            except:
                # SEARCH PICTURE WITH TAG
                tag = '|'.join(raw_message[1:])
                setu = Setu(tag=tag, r18=r18)
        else:
            # WITHOUT PARAMETER
            setu = Setu(r18=r18)
        return setu.exec()

    # DO MEME SEARCH SERVICE
    def meme(self, raw_message):
        argc = len(raw_message)
        if argc > 1:
            searcher = MemeSearch(raw_message[1])
            if argc == 2:
                return searcher.definition()  # SHOW FIRST ENTRY AS DEFAULT
            return searcher.definition(raw_message[2])
        else:
            return Util.bot_invalid_input_response()

    # DO VOICE SERVICE
    def voice(self, raw_message):
        voice_service = Voice(self.sender_uin)

        # DIFFERENT REACTION
        argc = len(raw_message)
        if argc == 1:
            # KOI'S VOICE
            return voice_service.koi_voice()
        elif argc == 2:
            # SEARCH VOICE BY TAG
            return voice_service.voice_search(raw_message[1])
        elif argc == 3:
            # OPERATE VOICE THROUGH ID
            _, vid, op = raw_message
            if not vid.isdigit():
                return Util.bot_invalid_input_response()
            return voice_service.manage_voice(vid, op)
        elif argc == 4:
            # OPERATE VOICE WITH PARAMETER
            _, vid, op, param = raw_message
            if not vid.isdigit():
                return Util.bot_invalid_input_response()
            return voice_service.manage_voice(vid, op, param)

    # DO MUSIC SERVICE
    def music(self, raw_message):
        argc = len(raw_message)
        if argc == 2:
            return Music(raw_message[1]).order()  # SHOW FIRST ENTRY AS DEFAULT
        elif argc > 2:
            # THERE MAY BE SPACE IN THE SONG NAME
            if raw_message[-1].isdigit():
                song_name = ' '.join(raw_message[1:-1])
                return Music(song_name).order(raw_message[-1])
            else:
                song_name = ' '.join(raw_message[1:])
                return Music(song_name).order()
        else:
            return "想听啥你说啊"

    # DO TRANSLATE SERVICE
    def translate(self, raw_message):
        if len(raw_message) < 2:
            return Util.bot_invalid_input_response()
        command = raw_message[0]

        # TRANSLATE TO CHINESE
        if command == "翻译":
            query = ' '.join(raw_message[1:])
            translated = BaiduTranslate(query).to_chinese()
            if translated is False:
                return "你好像有个大病..."
            return translated

        # TRANSLATE TO OTHER LANGUAGE
        if command[:3] == "翻译成":
            target = command[3:]
            if target:
                query = ' '.join(raw_message[1:])
                translated = BaiduTranslate(query).to_others(target)
                if translated is False:
                    return "你好像有个大病..."
                return translated
            else:
                return Util.bot_invalid_input_response()

    # DISPATCH THE MESSAGE TO DIFFERENT GROUP SERVICE
    def group_service_dispatch(self):
        msg = None

        # DIRECT INSTRUCTIONS
        raw_message = re.sub(r" +", ' ', self.raw_message).split(' ')
        command = raw_message[0]

        # MENU MODULE
        if command == "菜单":
            msg = Menu.detail(raw_message[1]) if len(raw_message) > 1 else Menu.main_content()

        # SIGN IN MODULE
        elif command == "签到" and g_group_service_config["sign_in"]["enable"]:
            msg = SignIn(self.sender_uin).exec()
        elif command in ["查询签到", "签到情况", "签到查询"] and g_group_service_config["sign_in"]["enable"]:
            msg = SignIn(self.sender_uin).get_status()

        # POINTS MODULE
        elif command in ["积分兑换", "兑换清单", "兑换列表"] and g_group_service_config["sign_in"]["enable"]:
            msg = Goods().exchange_list()
        elif command in ["积分查询", "查询积分"] and g_group_service_config["sign_in"]["enable"]:
            msg = Goods(self.sender_uin).points_status()
        elif self.is_exchange_command() and g_group_service_config["sign_in"]["enable"]:
            param = re.search(r"^兑换(.+)$", self.raw_message)
            msg = Goods(self.sender_uin).exchange(param.group(1))

        # SETU MODULE
        elif re.search(r"(涩图|色图|涩涩|色色|setu)", command):
            msg = self.setu(raw_message)

        # MEME SEARCH MODULE
        elif command == "梗百科":
            msg = self.meme(raw_message)

        # VOICE MODULE
        elif command == "语音":
            msg = self.voice(raw_message)

        # MUSIC MODULE
        elif command == "点歌":
            msg = self.music(raw_message)

        # TRANSLATE MODULE
        elif command[:2] == "翻译":
            msg = self.translate(raw_message)

        # COSPLAY PICTURE
        elif command.lower() in ["cos", "coser", "cosplay"] and g_group_service_config["cosplay"]["enable"]:
            msg = Cosplay.random_pic()

        # TU WEI QING HUA
        elif command in ["情话", "土味情话", "twqh"]:
            qing_hua = AlApi.tu_wei_qing_hua()
            msg = qing_hua if qing_hua else Util.bot_error_response()

        # TIAN GOU RI JI
        elif command in ["日记", "舔狗日记", "tgrj"]:
            ri_ji = AlApi.tian_gou_ri_ji()
            msg = ri_ji if ri_ji else Util.bot_error_response()

        # DU JI TANG
        elif command in ["鸡汤", "毒鸡汤", "djt"]:
            ji_tang = AlApi.du_ji_tang()
            msg = ji_tang if ji_tang else Util.bot_error_response()

        # HAO HAO SHUO HUA
        elif command == "好好说话":
            if len(raw_message) > 1:
                hhsh = AlApi.hao_hao_shuo_hua(raw_message[1])
                msg = hhsh if hhsh else "技能CD中..."
            else:
                msg = Util.bot_invalid_input_response()

        # JI CHOU
        elif command in ["记仇", "小本本记下来", "这仇我记下了", "这个仇我记下了"] and g_group_service_config["jichou"]["enable"]:
            version = setting["service"]["group"]["jichou"]["version"]
            msg = JiChou(' '.join(raw_message[1:])).generate(version == "new") if len(raw_message) > 1 else "想记点啥？"

        # AT ME
        elif command == f"[CQ:at,qq={setting['account']['qq']['bot']}]":
            msg = AtMe(' '.join(raw_message[1:])).reply()

        # GENERATE INSTRUCTION
        elif self.is_generate_command():
            param = re.search(r"^生成(.+?)( .+)?$", self.raw_message)
            msg = self.generate(param.group(1), param.group(2).strip() if param.group(2) is not None else None)

        # SAVE INSTRUCTION
        replied_id = self.is_save_command()
        if replied_id and Util.has_high_privilege(self.sender_uin):
            tag = re.search(r"\[CQ:reply,id=.+?]\[CQ:at,qq=\d+] 保存 (.+)", self.raw_message)
            msg = self.save_previous_message(replied_id, tag.group(1) if tag else '')

        # DELETE INSTRUCTION
        replied_id = self.is_delete_command()
        if replied_id and Util.has_high_privilege(self.sender_uin):
            msg = self.delete_previous_message(replied_id)

        # SEND MESSAGE TO GROUP
        if msg:
            reply = Util.reply_at_pack(msg, self.message_id, self.sender_uin)
            CQHTTP.send_group_message(reply)

    # GROUP MESSAGE CONTEXT
    def group_message_context(self):
        global g_bai_lan_flag, g_bai_lan_clock, g_bai_lan_lock
        global g_fudu_count, g_last_fudu, g_previous_msg, g_fudu_lock
        raw_message = self.raw_message

        # BAI LAN MODE CHECK
        g_bai_lan_lock.acquire()
        if g_bai_lan_flag:
            if g_bai_lan_clock.is_timeout():
                g_bai_lan_flag = False
            else:
                msg = BaiLan.msg_reply(raw_message)
                if msg:
                    msg = Util.reply_at_pack(msg, self.message_id, self.sender_uin)
                    CQHTTP.send_group_message(msg)
                g_bai_lan_lock.release()
                return 0xFC
        g_bai_lan_lock.release()

        # FU DU
        if self.fudu_limit_count > 0:
            g_fudu_lock.acquire()

            send_flag = False
            if raw_message == g_previous_msg and not self.is_command():
                g_fudu_count += 1
                if g_fudu_count == self.fudu_limit_count:
                    g_fudu_count = 0

                    # AVOID REPEATING SAME MESSAGE
                    if raw_message != g_last_fudu:
                        g_last_fudu = raw_message
                        send_flag = True
            else:
                g_fudu_count = 1
            g_previous_msg = raw_message

            g_fudu_lock.release()
            if send_flag:
                sent, _ = Util.run_at_probability(
                    g_group_msg_ctx_config["probability"]["fudu_break"],
                    CQHTTP.send_group_message,
                    random.choice(self.msg_ctx_corpora["打断复读"])
                )
                if not sent:
                    CQHTTP.send_group_message(raw_message)
                return

        # KOI SPEAK
        if self.sender_uin == self.koi_qq:
            msg = None

            # GOOD MORNING
            if re.search(r"起床(.?)了", raw_message) or \
                    re.search(r"^(大家|米娜桑)?(早|早安|早捏|早安捏|早早早|早上好|哦哈)([啊呀哦哟])?$", raw_message):
                msg = random.choice(self.msg_ctx_corpora["早安"])

            # GOOD NIGHT
            if re.search(r"^(大家|米娜桑)?(晚安|晚安捏|哦呀斯密)([啊呀哦哟])?.*", raw_message):
                msg = random.choice(self.msg_ctx_corpora["晚安"])

            # BAI LAN MODE START
            if raw_message in ["摆烂模式", "开始摆烂"] and self.bai_lan_mode_enable:
                g_bai_lan_lock.acquire()
                g_bai_lan_flag = True
                g_bai_lan_clock = Clock(g_group_msg_ctx_config["bai_lan_mode"]["recovery_time"])
                msg = Util.local_picture_pack(Util.get_image_resource("bailan", "bailan.jpg"))
                g_bai_lan_lock.release()
            if msg:
                return CQHTTP.send_group_message(msg)

        # HAO HAO HAO
        if "好好好" in raw_message or re.search(r"^好{1,2}$", raw_message):
            msg = random.choice(self.msg_ctx_corpora["好好好"])
            sent, _ = Util.run_at_probability(
                g_group_msg_ctx_config["probability"]["haohaohao"],
                CQHTTP.send_group_message,
                msg
            )
            if sent: return

        # HAO YE
        if "好耶" in raw_message or "好诶" in raw_message:
            msg = random.choice(self.msg_ctx_corpora["好耶"])
            sent, _ = Util.run_at_probability(
                g_group_msg_ctx_config["probability"]["haoye"],
                CQHTTP.send_group_message,
                msg
            )
            if sent: return

        # CAO
        if "草" in raw_message:
            msg = random.choice(self.msg_ctx_corpora["草"])
            sent, _ = Util.run_at_probability(
                g_group_msg_ctx_config["probability"]["cao"],
                CQHTTP.send_group_message,
                msg
            )
            if sent: return

        # JXT
        if re.search(r"捏$", raw_message):
            msg = random.choice(self.msg_ctx_corpora["捏"])
            sent, _ = Util.run_at_probability(
                g_group_msg_ctx_config["probability"]["jxt"],
                CQHTTP.send_group_message,
                msg
            )
            if sent: return

        # SHI BA
        if re.search(r"是吧$", raw_message):
            msg = random.choice(self.msg_ctx_corpora["是吧"])
            sent, _ = Util.run_at_probability(
                g_group_msg_ctx_config["probability"]["shiba"],
                CQHTTP.send_group_message,
                msg
            )
            if sent: return

    # DISPATCH THE MESSAGE TO DIFFERENT PRIVATE SERVICE
    def private_service_dispatch(self):
        raw_message = re.sub(r" +", ' ', self.raw_message).split(' ')
        command = raw_message[0]

        if command in ["cos更新", "更新cos"] and self.is_bot_admin():
            Cosplay.update_pic()

    # OVERRIDE
    def run(self):
        # PRIVATE MESSAGE
        if self.message_type == "private":
            return self.private_service_dispatch()

        # GROUP MESSAGE
        elif self.message_type == "group":
            # LISTEN ON TARGET GROUP & AVOID ANONYMOUS
            if self.group_uin != self.target_group or self.anonymous:
                return

            # RECORD SPEAK TIMES AND ENSURE THE MESSAGE IS MEANINGFUL
            speak_ranking.record(self.sender_uin)
            if not self.raw_message:
                return

            # AUTO SAVE CHECK IF ENABLED
            if g_auto_save_config["enable"]:
                self.auto_save_check()

            # CHECK IF SATISFY MESSAGE CONTEXT
            if g_group_msg_ctx_config["enable"]:
                if self.group_message_context() == 0xFC:  # BAI LAN
                    return

            # SERVICE DISPATCH
            self.group_service_dispatch()
