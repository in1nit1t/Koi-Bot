from core.decorator import Decorator
from dao.goods import GoodsDAO


class OrderDAO(GoodsDAO):

    # INIT SETTINGS
    def __init__(self):
        super().__init__()

    # INSERT ORDER
    @Decorator.db_insert
    def insert_order(self, uid, goods_id):
        sql = "insert into `order`(`uid`, `goods_id`) values(%s, %s)"
        self.cursor.execute(sql, (uid, goods_id))

    # UPDATE ORDER STATUS
    @Decorator.db_modify
    def update_order_status(self, order_id):
        sql = "update `order` set `completed`=1, `complete_time`=CURRENT_TIMESTAMP where `id`=%s"
        self.cursor.execute(sql, order_id)

    # SELECT ORDER BY ID
    @Decorator.db_select_one
    def select_order_by_id(self, order_id):
        sql = "select * from `order` where `id`=%s"
        self.cursor.execute(sql, order_id)

    # SELECT ORDER BY ID
    @Decorator.db_select_all
    def select_uncompleted_order_by_uid(self, uid):
        sql = "select `id` from `order` where `uid`=%s and `completed`=0"
        self.cursor.execute(sql, uid)

    # SELECT ORDER BY UID & GOODS ID
    @Decorator.db_select_one
    def select_order_by_uid_gid(self, uid, goods_id):
        sql = "select `id` from `order` where `uid`=%s and `goods_id`=%s"
        self.cursor.execute(sql, (uid, goods_id))

    # SELECT ORDER BY UIN
    def select_uncompleted_order_by_uin(self, uin):
        uid = self.get_uid_by_uin(uin)
        return self.select_uncompleted_order_by_uid(uid) if uid else False
