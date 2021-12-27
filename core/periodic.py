import time
import random
from datetime import datetime

from core.setting import setting
from core.util import Util, CQHTTP

from service.alapi import AlApi
from service.sign_in import SignIn
from service.bilibili import Bilibili
from service.contribute import Contribution
from service.speak_ranking import speak_ranking


class Periodic:

    # INIT SETTINGS
    def __init__(self):
        self.sign_in_flag = True
        self.morning_push_flag = True
        self.speak_ranking_flag = True
        self.contribution_push_flag = True

        # BILIBILI LISTEN USERS
        self.bilibili_listen = []
        listen_dict = setting["account"]["bilibili"]["event_listen"]
        for nick_name, uid in listen_dict.items():
            self.bilibili_listen.append(Bilibili(uid, nick_name))

        # SIGN IN REFRESH TIME
        sign_in_config = setting["service"]["group"]["sign_in"]
        self.sign_in_refresh_hour = int(sign_in_config["refresh_time"]["hour"])
        self.sign_in_refresh_minute = int(sign_in_config["refresh_time"]["minute"])

        # CONTRIBUTION
        contrib_config = setting["service"]["group"]["contribution"]
        self.contrib_enable = contrib_config["enable"]
        self.contrib_push_hour = int(contrib_config["push_time"]["hour"])
        self.contrib_push_minute = int(contrib_config["push_time"]["minute"])

    # MORNING PUSH
    def morning_push(self):
        pre_msg = "哦哈哟米娜桑，美好的一天开始啦~\n"

        # ADD ACG PICTURE
        pic_url = AlApi.acg_picture()
        if pic_url:
            pre_msg += Util.online_picture_pack(pic_url)

        # ADD TODAY IN HISTORY
        time.sleep(1)
        event_list = AlApi.today_in_history()
        if event_list:
            event = random.choice(event_list)
            title, date = event["title"], event["date"]
            pre_msg += f"\n你知道吗？{date[:date.find('年')]}年的今天，{title}。"
        CQHTTP.send_group_message(pre_msg)

        # SEND MORNING PAPER
        time.sleep(1)
        image_url = AlApi.morning_paper()
        if image_url:
            msg = Util.online_picture_pack(image_url.replace("webp", "png"))
            CQHTTP.send_group_message(msg)
        self.morning_push_flag = False

    # SPEAK RANKING
    def rank_speak(self):
        speak_ranking.ranking("today" if datetime.now().weekday() < 6 else "week")
        self.speak_ranking_flag = False

    # REFRESH TODAY'S SIGN IN
    def refresh_sign_in(self):
        SignIn().refresh()
        self.sign_in_flag = False

    # LIST CONTRIBUTION
    def list_contribution(self):
        contrib = Contribution()
        contrib.do_contribution_list()
        contrib.delete_contrib()
        self.contribution_push_flag = False

    # BILIBILI STATUS CHECK
    def bilibili_status_check(self):
        for listener in self.bilibili_listen:
            listener.live_status_check()
            listener.dynamic_status_check()
            if listener.notice_config["new_follower"]["enable"]:
                listener.new_follower_notice()

    # EXECUTE
    def exec(self):
        # CRON JOB
        now = time.strftime("%H:%M:%S", time.localtime())
        if "08:00:00" <= now < "08:00:30" and self.morning_push_flag:
            self.morning_push()
        if "22:00:00" <= now < "22:00:30" and self.speak_ranking_flag:
            self.rank_speak()
        if "%02d:%02d:00" % (self.sign_in_refresh_hour, self.sign_in_refresh_minute) <= now \
                < "%02d:%02d:30" % (self.sign_in_refresh_hour, self.sign_in_refresh_minute) \
                and self.sign_in_flag:
            self.refresh_sign_in()
        if self.contrib_enable and datetime.now().weekday() == 6 and self.contribution_push_flag and \
                "%02d:%02d:00" % (self.contrib_push_hour, self.contrib_push_minute) <= now \
                < "%02d:%02d:30" % (self.contrib_push_hour, self.contrib_push_minute):
            self.list_contribution()

        # RECOVERY FLAGS
        if "03:00:00" <= now < "03:00:30":
            self.sign_in_flag = True
            self.morning_push_flag = True
            self.speak_ranking_flag = True
            self.contribution_push_flag = True

        self.bilibili_status_check()
