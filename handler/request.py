from threading import Thread

from core.util import CQHTTP


class RequestHandler(Thread):

    # INIT SETTINGS
    def __init__(self, content):
        super().__init__()
        self.setDaemon(True)

        self.flag = content["flag"]
        self.comment = content["comment"]
        self.user_uin = content["user_id"]
        self.self_uin = content["self_id"]
        self.request_type = content["request_type"]

    # ADD FRIEND
    def add_friend(self):
        CQHTTP.set_friend_add_request(self.flag, True)

    # OVERRIDE
    def run(self):
        # NEW FRIEND ADD REQUEST
        if self.request_type == "friend":
            self.add_friend()
