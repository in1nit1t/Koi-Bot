from core.database import Database
from core.decorator import Decorator


class GoodsDAO(Database):

    # INIT SETTINGS
    def __init__(self):
        super().__init__()

    # SELECT GOODS BY ID
    @Decorator.db_select_one
    def select_goods_by_id(self, goods_id):
        sql = "select `name`, `description`, `type`, `price`, `expire_time` from goods where `id`=%s"
        self.cursor.execute(sql, goods_id)

    # SELECT UNEXPIRED GOODS
    @Decorator.db_select_all
    def select_all_unexpired_goods(self):
        sql = "select `name`, `description`, `type`, `price`, `expire_time` from goods where `expire_time` > " \
              "CURRENT_TIMESTAMP or `expire_time` is NULL"
        self.cursor.execute(sql)

    # SELECT UNEXPIRED GOODS BY NAME
    @Decorator.db_select_one
    def select_unexpired_goods_by_name(self, goods_name):
        sql = "select `id`, `type`, `price`, `expire_time` from goods where `name`=%s and (`expire_time` > " \
              "CURRENT_TIMESTAMP or `expire_time` is NULL)"
        self.cursor.execute(sql, goods_name)
