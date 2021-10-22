import re
import json
import requests
import traceback

from core.util import Util
from core.logger import logger


class Epidemic:
    api_url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"

    # INIT SETTINGS
    def __init__(self):
        self.data = None
        try:
            response = requests.get(Epidemic.api_url, timeout=3).json()
            if response["ret"] == 0:
                self.data = json.loads(response["data"])
        except:
            logger.error("<Epidemic> API调用失败", traceback.format_exc())

    # SEARCH NODE
    def bfs(self, key):
        lst = [self.data["areaTree"][0]]
        while len(lst):
            node = lst.pop(0)
            if node.__contains__("children"):
                for child in node["children"]:
                    if child["name"] == key:
                        child["prefix"] = node["name"]
                        return child
                lst.extend(node["children"])

    # CHINA TOTAL DATA
    def china_total(self):
        if not self.data:
            return Util.bot_error_response()

        diff = self.data["chinaAdd"]
        info = self.data["chinaTotal"]
        rate = self.data["areaTree"][0]["total"]
        ret = f"全国疫情情况\n" \
              f"数据更新时间：{self.data['lastUpdateTime']}\n" \
              f"{'-' * 20}\n【实时数据】\n\n" \
              f"本土现有确诊：{info['localConfirm']}（较昨日{'+' if diff['localConfirm'] >= 0 else ''}{diff['localConfirm']}）\n" \
              f"现有确诊（含港澳台）：{info['nowConfirm']}（较昨日{'+' if diff['nowConfirm'] >= 0 else ''}{diff['nowConfirm']}）\n" \
              f"无症状感染者：{info['noInfect']}（较昨日{'+' if diff['noInfect'] >= 0 else ''}{diff['noInfect']}）\n" \
              f"境外输入：{info['importedCase']}（较昨日{'+' if diff['importedCase'] >= 0 else ''}{diff['importedCase']}）\n" \
              f"疑似病例：{info['suspect']}（较昨日{'+' if diff['suspect'] >= 0 else ''}{diff['suspect']}）" \
              f"{'-' * 20}\n【累计数据】\n\n" \
              f"累计确诊：{info['confirm']}（较昨日+{diff['confirm']}）\n" \
              f"累计死亡：{info['dead']}（较昨日+{diff['dead']}）\n" \
              f"累计治愈：{info['heal']}（较昨日+{diff['heal']}）\n" \
              f"死亡率：{rate['deadRate']}%\n" \
              f"治愈率：{rate['healRate']}%"
        return ret

    # AREA DATA
    def area(self, area_name):
        if not self.data:
            return Util.bot_error_response()

        area_date = self.bfs(area_name)
        if not area_date:
            return f"没有找到 [{area_name}] 的疫情数据捏"

        info = area_date['total']
        ret = f"{area_date['prefix'] if area_date['prefix'] != '中国' else ''}{area_name}\n" \
              f"数据更新时间：{self.data['lastUpdateTime']}\n" \
              f"{'-' * 20}\n" \
              f"现有确诊人数：{info['nowConfirm']}\n" \
              f"现有疑似病例：{info['suspect']}\n" \
              f"无症状感染者：{info['wzz']}\n" \
              f"累计确诊人数：{info['confirm']}\n" \
              f"累计死亡人数：{info['dead']}\n" \
              f"累计治愈人数：{info['heal']}\n" \
              f"死亡率：{info['deadRate']}%\n" \
              f"治愈率：{info['healRate']}%"
        return ret

    # TOP LAYER
    def exec(self, raw_message):
        if raw_message == "疫情":
            return self.china_total()
        else:
            area_name = re.search(r"^(.{1,11})疫情$", raw_message).group(1)
            area_name = area_name[:-1] if area_name[-1] == "省" else area_name
            return self.area(area_name)
