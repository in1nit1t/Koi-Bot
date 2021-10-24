from core.database import Database
from core.decorator import Decorator


class VoiceDAO(Database):

    # INIT SETTINGS
    def __init__(self):
        # BASE INITIAL
        super().__init__()

    # INSERT VOICE
    @Decorator.db_insert
    def insert_voice(self, message_id, uid, filename, url, tag):
        sql = "insert into voice(`message_id`, `uid`, `file`, `url`, `tag`) values(%s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (message_id, uid, filename, url, tag))

    # DELETE VOICE BY ID
    @Decorator.db_modify
    def delete_voice_by_id(self, vid):
        sql = "delete from voice where `id`=%s"
        self.cursor.execute(sql, vid)

    # DELETE VOICE BY MESSAGE ID
    @Decorator.db_modify
    def delete_voice_by_message_id(self, message_id):
        sql = "delete from voice where `message_id`=%s"
        self.cursor.execute(sql, message_id)

    # UPDATE VOICE TAG BY ID
    @Decorator.db_modify
    def update_tag_by_id(self, vid, tag):
        sql = "update voice set `tag`=%s where `id`=%s"
        self.cursor.execute(sql, (tag, vid))

    # UPDATE VOICE TAG BY MESSAGE ID
    @Decorator.db_modify
    def update_tag_by_message_id(self, message_id, tag):
        sql = "update voice set `tag`=%s where `message_id`=%s"
        self.cursor.execute(sql, (tag, message_id))

    # RETURN ALL VOICE
    @Decorator.db_select_all
    def select_all(self):
        sql = "select * from voice"
        self.cursor.execute(sql)

    # RETURN ONE VOICE BY ID
    @Decorator.db_select_one
    def select_voice_by_id(self, vid):
        sql = "select * from voice where `id`=%s"
        self.cursor.execute(sql, vid)

    # RETURN ONE VOICE BY MESSAGE ID
    @Decorator.db_select_one
    def select_voice_by_message_id(self, message_id):
        sql = "select * from voice where `message_id`=%s"
        self.cursor.execute(sql, message_id)

    # RETURN ALL VOICE BY UID
    @Decorator.db_select_all
    def select_voice_by_uid(self, uid):
        sql = "select * from voice where `uid`=%s"
        self.cursor.execute(sql, uid)

    # RETURN ALL VOICE BY TAG
    @Decorator.db_select_all
    def select_voice_by_tag(self, tag):
        sql = "select * from voice where `tag` like %s"
        self.cursor.execute(sql, f"%{tag}%")

    # RECORD VOICE
    def record_voice(self, message_id, uin, voice_params, tag):
        uid = self.get_uid_by_uin(uin)
        if uid:
            filename, url = voice_params
            return self.insert_voice(message_id, uid, filename, url, tag)
        return 0

    # GET VOICE BY UIN
    def get_voice_by_uin(self, uin):
        uid = self.get_uid_by_uin(uin)
        return self.select_voice_by_uid(uid) if uid else 0
