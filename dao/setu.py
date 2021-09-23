from core.database import Database
from core.decorator import Decorator


class SetuDAO(Database):

    # INIT SETTINGS
    def __init__(self):
        # BASE INITIAL
        super().__init__()

    # INSERT RECORD
    @Decorator.db_modify
    def insert(self, pid, small_url, original_url):
        res = self.select(pid)

        # UPDATE IF URL CHANGED
        if res:
            ori_small, ori_original = res
            if ori_small != small_url or ori_original != original_url:
                self.update(pid, small_url, original_url)
            return

        # INSERT WHEN RECORD NOT EXIST
        if res is None:
            sql = "insert into setu(`pid`, `small_url`, `original_url`) values(%s, %s, %s)"
            self.cursor.execute(sql, (pid, small_url, original_url))

    # UPDATE RECORD
    @Decorator.db_modify
    def update(self, pid, small_url, original_url):
        sql = "update setu set `small_url`=%s, `original_url`=%s where `pid`=%s"
        self.cursor.execute(sql, (small_url, original_url, pid))

    # SELECT RECORD
    @Decorator.db_select_one
    def select(self, pid):
        sql = "select `small_url`, `original_url` from setu where `pid`=%s"
        self.cursor.execute(sql, pid)
