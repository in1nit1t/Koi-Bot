import socket
import traceback

from core.util import Util
from core.logger import logger
from core.periodic import Periodic

from handler.notice import NoticeHandler
from handler.message import MessageHandler
from handler.request import RequestHandler


class Server:

    work_flag = True
    periodic_work = Periodic()

    # INIT SETTINGS
    def __init__(self, port):
        # NETWORK SETUP
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("127.0.0.1", port))
        self.server_socket.listen(64)

    # STOP SERVER
    def stop(self):
        self.work_flag = False

    # SERVER MAINLOOP
    def mainloop(self):
        print(f"[+] Server successfully launched at 127.0.0.1:{self.port}")
        while self.work_flag:
            client_socket, _ = self.server_socket.accept()

            # RECEIVE POST & RESPONSE
            request = client_socket.recv(10240).decode("utf-8").strip()
            content = Util.request2json(request)
            response = Util.response_head_pack(200 if content else 500, {"Content-Type": "text/html"})
            client_socket.sendall(response.encode("utf-8"))
            client_socket.close()
            if not content:
                continue

            # DIFFERENTIATE POST TYPE
            try:
                post_type = content["post_type"]
                if post_type == "message":
                    message_handler = MessageHandler(content)
                    message_handler.start()
                elif post_type == "notice":
                    notice_handler = NoticeHandler(content)
                    notice_handler.start()
                elif post_type == "request":
                    request_handler = RequestHandler(content)
                    request_handler.start()
                else:
                    # PULSE
                    self.periodic_work.exec()
            except:
                logger.error(f"<Server> 内部错误", traceback.format_exc())
