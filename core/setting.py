import os
import json
import traceback


class Setting:

    # INIT SETTINGS
    def __init__(self):
        # GET SETTING FILE PATH
        app_path = os.path.abspath(os.getcwd())
        self.file_path = os.path.normpath(os.path.join(app_path, "setting.json"))
        if not os.path.isfile(self.file_path):
            exit("请检查项目根目录下是否存在 setting.json 配置文件。")

        # DO LOAD
        self.items = {}
        self.load()

    # LOAD SETTINGS TO JSON FORMAT
    def load(self):
        try:
            with open(self.file_path, encoding="utf-8") as f:
                self.items = json.loads(f.read())
        except:
            traceback.print_exc()
            exit("配置文件 setting.json 加载失败，请检查 json 语法是否正确。")


# GLOBAL VARIABLE
_ = Setting()
setting = _.items
