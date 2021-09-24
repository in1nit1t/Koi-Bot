import traceback
from datetime import timedelta, datetime

from core.util import Util
from core.logger import logger
from core.setting import setting
from dao.sign_in import SignInDAO
from service.hitokoto import Hitokoto


class SignIn:

    # INIT SETTINGS
    def __init__(self, uin=None):
        self.uin = uin
        self.sign_in_dao = SignInDAO()

    # REFRESH SIGN IN FLAG
    def refresh(self):
        return self.sign_in_dao.clear_signed()

    # SIGN IN SUCCESS
    def success(self, uid):
        info = self.sign_in_dao.select_order(uid)
        if not info:
            return Util.bot_error_response()

        order, continuous = int(info[0]), info[1]
        points = int(setting["service"]["group"]["sign_in"]["base_points"])
        msg = f"喵～主人，你是今天第{order}个签到的"

        # TOP 3 BONUS
        if order <= 3:
            points += 4 - order
            msg += f"(+{4 - order})"

        # CONTINUOUS SIGN IN BONUS
        if continuous > 1:
            msg += f"，这是你第{continuous}天连续签到"
        if continuous >= 30:
            points += 6
            msg += "(+6)"
        elif continuous >= 15:
            points += 4
            msg += "(+4)"
        elif continuous >= 5:
            points += 2
            msg += "(+2)"

        if not self.sign_in_dao.update_points(uid, points):
            logger.warning("<签到> 积分增加失败", f"用户id：{uid}\n分数：{points}", True)
        msg += f"，获得{points}点积分~(*'▽'*)♪"

        # ADD HITOKOTO SENTENCE
        sentence, _ = Hitokoto.random_sentence()
        if sentence:
            msg += f"\n\n属于你的语录～：\n『{sentence}』 —— {_}"
        return msg

    # SIGN IN STATUS
    def get_status(self):
        data = self.sign_in_dao.select_all_by_uin(self.uin)
        if not data:
            return Util.bot_error_response()
        signed, last_time, continuous, max_continuous, total = data
        msg = f"今天{'已经签到了捏' if signed else '还没有签到捏'}\n"
        msg += f"上次签到时间：{last_time}\n"
        msg += f"当前连续签到天数：{continuous}天\n"
        msg += f"最大连续签到天数：{max_continuous}天\n"
        msg += f"累计签到次数：{total}次"
        return msg

    # DO SIGN IN
    def exec(self):
        # GET UID & HISTORY SIGN IN INFO
        uid = self.sign_in_dao.get_uid_by_uin(self.uin)
        if not uid:
            return Util.bot_error_response()
        info = self.sign_in_dao.select_signed_time(uid)
        if not info:
            return Util.bot_error_response()

        signed, last_time = info
        if not signed:
            if last_time is None:   # FIRST TIME
                ret = self.sign_in_dao.first_time_sign_in(uid)
            else:
                if datetime.now() - last_time < timedelta(hours=24):
                    ret = self.sign_in_dao.update_continuous(uid)
                else:
                    ret = self.sign_in_dao.update_discontinuous(uid)
            return self.success(uid) if ret else Util.bot_error_response()
        else:
            return "铁咩，你今天已经签过到了，再签到你吗必死~"
