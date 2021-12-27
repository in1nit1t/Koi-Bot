from core.database import Database
from core.decorator import Decorator


class ContributionDAO(Database):

    # INIT SETTINGS
    def __init__(self):
        super().__init__()

    # INSERT CONTRIBUTION
    @Decorator.db_insert
    def insert_contrib(self, uin, content):
        sql = "INSERT INTO `contribution`(`uid`, `content`) VALUES(%s, %s)"
        self.cursor.execute(sql, (uin, content))

    # SELECT THIS WEEK'S CONTRIBUTION
    @Decorator.db_select_all
    def select_week_contrib(self):
        sql = "SELECT * FROM `contribution`"
        self.cursor.execute(sql)

    # DELETE ALL CONTRIBUTION
    @Decorator.db_modify
    def delete_contrib(self):
        sql = "DELETE FROM `contribution`"
        self.cursor.execute(sql)
