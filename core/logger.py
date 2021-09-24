import os
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from core.setting import setting


class Logger:

    # INIT SETTINGS
    def __init__(self, log_dir):
        # CREATE LOG FILE HANDLE
        file_path = os.path.join(log_dir, "botlog")
        time_handler = TimedRotatingFileHandler(file_path, when="midnight", backupCount=5, encoding="utf-8")
        time_handler.setLevel(logging.INFO)
        time_handler.suffix = "%Y-%m-%d.log"
        time_handler.setFormatter(logging.Formatter(fmt='[%(asctime)s] %(message)s'))

        # ADD HANDLE TO LOGGER
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.INFO)
        self._logger.addHandler(time_handler)

        self.admin_uin = setting["account"]["qq"]["admin"]

    # INFORMATION LOG
    def info(self, msg):
        self._logger.info(f"- INFO - {msg}")

    # SUCCESS LOG
    def success(self, msg):
        self._logger.info(f"- SUCCESS - {msg}")

    # WARNING LOG
    def warning(self, keyword, msg, notice=False):
        msg = msg.strip()
        if notice:
            from core.util import CQHTTP
            CQHTTP.send_private_message(f"[{datetime.now()}] WARNING\n\n{keyword}\n\n{msg}", self.admin_uin)
        self._logger.error(f"- WARNING - \n{msg}")

    # ERROR LOG
    def error(self, keyword, msg, notice=True):
        msg = msg.strip()
        if notice:
            from core.util import CQHTTP
            CQHTTP.send_private_message(f"[{datetime.now()}] ERROR\n\n{keyword}\n\n{msg}", self.admin_uin)
        self._logger.error(f"- ERROR - \n{msg}")

    # CRITICAL ERROR LOG
    def critical(self, keyword, msg, notice=True):
        msg = msg.strip()
        if notice:
            from core.util import CQHTTP
            CQHTTP.send_private_message(f"[{datetime.now()}] !CRITICAL!\n\n{keyword}\n\n{msg}", self.admin_uin)
        self._logger.critical(f"- !CRITICAL! - \n{msg}")


# GLOBAL VARIABLE
logger = Logger(setting["misc"]["log_directory"])
