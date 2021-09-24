import random
from threading import Thread

from core.setting import setting
from core.util import Util, Counter, CQHTTP
from service.goods import Goods
from service.alapi import AlApi
from handler import message

g_poke_config = setting["service"]["group"]["poke"]
g_poke_counter = Counter(g_poke_config["ban"]["limit_times"])


class NoticeHandler(Thread):

    target_group = int(setting["account"]["qq"]["target_group"])
    poke_corpora = Util.load_corpora_resource("poke")

    # INIT SETTINGS
    def __init__(self, content):
        super().__init__()
        self.setDaemon(True)

        # RESTORE PROPERTY
        self.self_uin = content["self_id"]
        self.notice_type = content["notice_type"]
        self.sub_type = content["sub_type"] if content.__contains__("sub_type") else ''
        self.sender_uin = content["user_id"] if content.__contains__("user_id") else ''
        self.group_uin = content["group_id"] if content.__contains__("group_id") else ''
        self.target_uin = content["target_id"] if content.__contains__("target_id") else ''

    # POKE REPLY
    def poke_reply(self):
        msg = None

        message.g_bai_lan_lock.acquire()
        if message.g_bai_lan_flag:
            if message.g_bai_lan_clock.is_timeout():
                message.g_bai_lan_flag = False
            else:
                return message.g_bai_lan_lock.release()
        message.g_bai_lan_lock.release()

        # BAN USER IF POKE TIMES OVER THE LIMITATION
        count = g_poke_counter.count(self.sender_uin)
        if count:
            if random.random() <= g_poke_config["ban"]["probability"] / 100:
                g_poke_counter.reset(self.sender_uin)
                self_info = CQHTTP.group_member_info(self.self_uin)
                target_info = CQHTTP.group_member_info(self.sender_uin)
                if self_info and target_info:
                    self_role, target_role = self_info["role"], target_info["role"]
                    if self_role in ["admin", "owner"] \
                            and target_role in ["member", "admin"] and self_role != target_role:
                        CQHTTP.ban_single_user(self.sender_uin, g_poke_config["ban"]["time"])
                        msg = "我生气了！！！" + random.choice(self.poke_corpora["生气"])
                        return CQHTTP.send_group_message(msg)
            else:
                return CQHTTP.send_group_message(random.choice(self.poke_corpora["正常"]))

        rand = random.random()
        if rand <= 0.33:
            msg = Util.poke_pack(self.sender_uin)
        elif rand <= 0.67:
            msg = Util.local_voice_pack(Util.get_voice_resource(g_poke_config["voice_source"]))
        else:
            pic_url = AlApi.acg_picture()
            if pic_url:
                msg = Util.online_picture_pack(pic_url)
        CQHTTP.send_group_message(msg)

    # WELCOME NEW MEMBER
    def welcome_new_group_member(self):
        corpora = random.choice(Util.load_corpora_resource("welcome")["新成员"])
        msg = Util.at_pack(corpora, self.sender_uin)
        CQHTTP.send_group_message(msg)

    # WELCOME NEW FRIEND
    def welcome_new_friend(self):
        corpora = random.choice(Util.load_corpora_resource("welcome")["新好友"])
        info = CQHTTP.get_stranger_info(self.sender_uin)
        if info:
            corpora = info["nickname"] + corpora
        CQHTTP.send_private_message(corpora, self.sender_uin)

    # CHECK IF FRIEND HAS UNCOMPLETED ORDER
    def check_order(self):
        goods_service = Goods(self.sender_uin)

        orders = goods_service.order_dao.select_uncompleted_order_by_uin(self.sender_uin)
        if not orders: return

        for order in orders:
            goods_service.finish_order(order[0])

    # OVERRIDE
    def run(self):
        if self.group_uin == self.target_group:
            # NOTICE - POKE
            if self.sub_type == "poke" and g_poke_config["enable"] and self.target_uin == self.self_uin != '':
                self.poke_reply()

            # NOTICE - NEW GROUP MEMBER
            if self.notice_type == "group_increase" and self.sub_type in ["approve", "invite"]:
                self.welcome_new_group_member()

        # NOTICE - FRIEND ADD
        if self.notice_type == "friend_add":
            self.welcome_new_friend()
            self.check_order()
