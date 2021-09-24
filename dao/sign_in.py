from core.database import Database
from core.decorator import Decorator


class SignInDAO(Database):

    # INIT SETTINGS
    def __init__(self):
        # BASE INITIAL
        super().__init__()

    # CLEAR SIGNED FLAG
    @Decorator.db_modify
    def clear_signed(self):
        sql = "update sign_in set `signed`=0"
        self.cursor.execute(sql)

    # UPDATE CONTINUOUS SIGN IN
    @Decorator.db_modify
    def update_continuous(self, uid):
        data = self.select_continuous(uid)
        sql = f"update sign_in set `signed`=1, `last_time`=CURRENT_TIMESTAMP, `continuous`=`continuous`+1" \
              f"{', `max_continuous`=`continuous`' if data[0] >= data[1] else ''}, `total`=`total`+1 where `uid`=%s"
        self.cursor.execute(sql, uid)

    # UPDATE DISCONTINUOUS SIGN IN
    @Decorator.db_modify
    def update_discontinuous(self, uid, first_time=False):
        sql = "update sign_in set `signed`=1, `last_time`=CURRENT_TIMESTAMP, `continuous`=1, " \
              f"`total`=`total`+1{', `max_continuous`=1' if first_time else ''} where `uid`=%s"
        self.cursor.execute(sql, uid)

    # SELECT SIGN IN ORDER
    @Decorator.db_select_one
    def select_order(self, uid):
        sql = "select t.`id`, t.`continuous` from (select (@i:=@i+1) `id`, `uid`, `continuous` \
               from sign_in, (select @i:=0) i where `signed`=1 order by `last_time` asc) t where t.`uid`=%s"
        self.cursor.execute(sql, uid)

    # SELECT LAST SIGN IN TIME
    @Decorator.db_select_one
    def select_signed_time(self, uid):
        sql = "select `signed`, `last_time` from sign_in where `uid`=%s"
        self.cursor.execute(sql, uid)

    # SELECT CONTINUOUS INFORMATION
    @Decorator.db_select_one
    def select_continuous(self, uid):
        sql = "select `continuous`, `max_continuous` from sign_in where `uid`=%s"
        self.cursor.execute(sql, uid)

    # SELECT SIGN IN INFO
    @Decorator.db_select_one
    def select_all(self, uid):
        sql = "select `signed`, `last_time`, `continuous`, `max_continuous`, `total` from sign_in where `uid`=%s"
        self.cursor.execute(sql, uid)

    # SELECT SIGN IN INFO BY UIN
    def select_all_by_uin(self, uin):
        uid = self.get_uid_by_uin(uin)
        return self.select_all(uid) if uid else False

    # FIRST TIME SIGN IN
    def first_time_sign_in(self, uid):
        return self.update_discontinuous(uid, first_time=True)
