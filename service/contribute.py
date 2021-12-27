import time

from core.util import Util, CQHTTP
from dao.contribution import ContributionDAO


class Contribution:

    # INIT SETTINGS
    def __init__(self, uin=None):
        self.uin = uin
        self.contrib_dao = ContributionDAO()

    # ADD NEW CONTRIBUTION
    def add_contrib(self, raw_message):
        if len(raw_message) < 2:
            return Util.bot_invalid_input_response()

        ret = self.contrib_dao.insert_contrib(self.uin, raw_message[1])
        return "投稿成功☆" if ret else Util.bot_error_response()

    # LIST CONTRIBUTION
    def do_contribution_list(self):
        contributions = self.contrib_dao.select_week_contrib()
        if not contributions:
            return "本周没有投稿，你们怎么回事？"

        CQHTTP.send_group_message("接下来将推送本周的投稿")
        for contrib in contributions:
            _, uid, content, create_time = contrib
            user = self.contrib_dao.select_user_by_uid(uid)
            nickname = Util.get_member_nickname(user[1]) if user else "暂无数据"

            self.contrib_dao.select_user_by_uid(uid)
            msg = f"投稿人：{nickname}\n" \
                  f"投稿时间：{create_time}\n\n" \
                  f"{content}"
            time.sleep(0.5)
            CQHTTP.send_group_message(msg)
