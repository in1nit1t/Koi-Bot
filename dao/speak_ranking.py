from core.database import Database
from core.decorator import Decorator


class SpeakRankingDAO(Database):

    # INIT SETTINGS
    def __init__(self):
        # BASE INITIAL
        super().__init__()

    # UPDATE TODAY COLUMN
    @Decorator.db_modify
    def update_today(self, uid):
        sql = "update speak_ranking set `today`=`today`+1 where `uid`=%s"
        self.cursor.execute(sql, uid)

    # UPDATE WEEK COLUMN
    @Decorator.db_modify
    def update_week(self, clear=False):
        if clear:
            sql = "update speak_ranking set `week`=0"
            self.cursor.execute(sql)
        else:
            sql = "update speak_ranking set `week`=`week`+`today`"
            self.cursor.execute(sql)
            sql = "update speak_ranking set `today`=0"
            self.cursor.execute(sql)

    # SELECT RECORD
    @Decorator.db_select_all
    def select(self, level):
        sql = f"select u.uin, s.{level} from speak_ranking s inner join `user` u on (u.id = s.uid)" \
              f"where s.{level} > 0 order by s.{level} desc"
        self.cursor.execute(sql)
