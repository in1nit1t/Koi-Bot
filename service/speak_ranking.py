import random

from core.util import Util, CQHTTP
from dao.speak_ranking import SpeakRankingDAO


class SpeakRanking:

    # INIT SETTINGS
    def __init__(self):
        self.ranking_dao = SpeakRankingDAO()

    # UPDATE SPEAK TIMES
    def record(self, uin):
        uid = self.ranking_dao.get_uid_by_uin(uin)
        if uid:
            self.ranking_dao.update_today(uid)

    # SPEAK RANKING
    def ranking(self, level):
        keyword = "今天" if level == "today" else "本周"

        # ADD SUNDAY'S FIRST
        if level == "week":
            self.ranking_dao.update_week()

        # RANK SPLICING
        pairs = self.ranking_dao.select(level)
        if pairs:
            msg = f"下面是{keyword}的发言数排行榜：\n"
            for idx, pair in enumerate(pairs):
                msg += '\n'

                # SERIAL NUMBER
                if idx == 0:
                    msg += "🥇 "
                elif idx == 1:
                    msg += "🥈 "
                elif idx == 2:
                    msg += "🥉 "
                else:
                    msg += f"{idx + 1}. "

                # TEMPLATE
                msg += Util.at_pack(f"{keyword}说了 {pair[1]} 句话", pair[0])

                # SUFFIX
                if idx == 0:
                    suffix = [
                        "真能 bb",
                        "不愧是你",
                        "就你话多",
                        "能不能去学习",
                        "住在尼斯湖？",
                        "你这个人话很多啊"
                    ]
                    msg += '，' + random.choice(suffix)
        else:
            # NO ONE SPEAK
            msg = f"啊咧，{keyword}没有人说话呢，人家好寂寞..."
        CQHTTP.send_group_message(msg)

        # TRUNCATE RECORD
        if level == "today":
            self.ranking_dao.update_week()
        else:
            self.ranking_dao.update_week(True)


# GLOBAL VARIABLE
speak_ranking = SpeakRanking()
