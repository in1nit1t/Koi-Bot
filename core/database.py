import pymysql
import traceback

from core.logger import logger
from core.setting import setting
from core.decorator import Decorator


class Database:

    # INIT SETTINGS
    def __init__(self):
        # GET DATABASE SETTINGS
        db_config = setting["database"]

        try:
            # CONNECT DATABASE & GET CURSOR
            self.connect = pymysql.connect(
                host=db_config["host"],
                user=db_config["user"],
                password=db_config["db_password"],
                db=db_config["db_name"],
                charset="utf8"
            )
        except:
            logger.error('', traceback.format_exc(), False)
            exit("数据库连接失败")
        self.cursor = self.connect.cursor()

    # DELETE MAGIC FUNCTION
    def __del__(self):
        try:
            self.cursor.close()
            self.connect.close()
        except:
            pass

    # ADD NEW USER
    def new_user(self, uin):
        try:
            # INSERT `user` TABLE
            sql = "insert into user(`uin`) values(%s)"
            self.cursor.execute(sql, uin)
            uid = self.cursor.lastrowid

            # INSERT `speak_ranking` TABLE
            sql = "insert into speak_ranking(`uid`) values(%s)"
            self.cursor.execute(sql, uid)

            # INSERT `sign_in` TABLE
            sql = "insert into sign_in(`uid`) values(%s)"
            self.cursor.execute(sql, uid)
            self.connect.commit()
            return uid
        except:
            logger.error(f"<MySQL> 添加新用户 {uin} 失败", traceback.format_exc())
            self.connect.rollback()
            return 0

    # UPDATE POINTS
    @Decorator.db_modify
    def update_points(self, uid, delta, increase=True):
        sql = f"update `user` set `points`=`points`{'+' if increase else '-'}{delta} where `id`=%s"
        self.cursor.execute(sql, uid)

    # SELECT POINTS BY UID
    @Decorator.db_select_one
    def select_points(self, uid):
        sql = "select `points` from user where `id`=%s"
        self.cursor.execute(sql, uid)

    # SELECT USER BY UIN
    @Decorator.db_select_one
    def select_user_by_uin(self, uin):
        sql = "select * from user where `uin`=%s"
        self.cursor.execute(sql, uin)

    # GET UID BY UIN
    def get_uid_by_uin(self, uin):
        res = self.select_user_by_uin(uin)
        if res:
            return res[0]
        elif res is None:
            # AUTOMATICALLY ADD USER IF NOT EXIST
            return self.new_user(uin)
