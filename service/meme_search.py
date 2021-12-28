import re
import time
import requests
import traceback
from lxml import etree

from core.util import Util
from core.logger import logger


class MemeSearch:

    search_html = ''
    definition_html = ''
    definition_base_url = "https://jikipedia.com/definition/"

    # INIT SETTINGS
    def __init__(self, keyword):
        self.keyword = keyword
        self.search_url = f"https://jikipedia.com/search?phrase={self.keyword}"

    # ERROR HINT
    def website_error(self):
        return "技能CD中，请稍后再试~"

    # ENSURE HTML IS MEANINGFUL
    def fetch_html(self, url, max_try=5):
        if max_try > 0:
            try:
                html = requests.get(url).text
                if "访问过于频繁" in html:
                    time.sleep(1.5)
                    return self.fetch_html(url, max_try - 1)
                else:
                    return html
            except:
                logger.warning(f"<梗百科> 获取 [{url}] 内容失败", traceback.format_exc())
                return self.fetch_html(url, max_try - 1)
        else:
            return None

    # GET DEFINITION ID
    def get_did(self, seq):
        # SELECT LABEL <div> THAT CONTAINS TITLE
        tree = etree.HTML(self.search_html)
        result_div = tree.xpath("//strong[@class='title pre']")

        # GET DID THROUGH SEQUENCE
        seq -= 1
        if 0 <= seq < len(result_div):
            return result_div[seq].getparent().getparent().getparent().getparent().get("data-id")
        return False

    # GET REFERENCES THAT DEFINITION USED
    def get_references(self):
        ret = ''
        try:
            # GET FROM JAVASCRIPT
            references = re.search(r"[a-zA-Z]{1,2}\.references=\[{(.+?)}]", self.definition_html).group(1)
            references_info = re.findall(r"path:\"(.+?)\",title:\"(.+?)\"", references)
            for idx, info in enumerate(references_info):
                url, title = info
                ret += f"\n{idx + 1}. {title}：{Util.unicode_decode(url)}"
            return ret
        except:
            return None

    # PARSE SEARCH & RETURN ENTRIES
    def parse_search(self):
        # SELECT LABEL <div> THAT CONTAINS TITLE
        tree = etree.HTML(self.search_html)
        result_div = tree.xpath("//strong[@class='title pre']")

        # ENTRIES SPLICING
        ret = ''
        for idx, div in enumerate(result_div):
            ret += f"{idx+1}. {div.text}\n"
        return ret

    # PARSE DEFINITION PAGE
    def parse_definition(self, seq):
        # SELECT LABEL <span> THAT CONTAINS DEFINITION PIECE
        tree = etree.HTML(self.definition_html)
        texts = tree.xpath("//div[@class='content']/div/span/text()")

        # DEFINITION SPLICING
        ret = f"以下是关于 [{self.keyword}] 的第 {seq} 条定义：\n{'-' * 20}\n"
        ret += ''.join(map(lambda x: re.sub(u"[\u200c\u200b]", '', x), texts))

        # ADD PICTURE IF EXIST
        content_div = tree.xpath("//div[@class='content']")[0]
        next_div = content_div.getnext()
        if type(next_div) is type(content_div):  # NEXT MAY BE COMMENT LIKE <!---->
            if "show image button" in next_div.get("class"):
                img = next_div.find(".//img")
                if img is not None:
                    img_url = img.get("src")
                    ret += Util.online_picture_pack(img_url)

        # ADD REFERENCES IF EXIST
        references = self.get_references()
        if references:
            ret += f"\n{'-' * 20}\n<- 参考 ->\n{references}"
        return ret

    # SEARCH WITH KEYWORD
    def do_search(self):
        # ACCESS SEARCH PAGE
        self.search_html = self.fetch_html(self.search_url)
        if self.search_html is None:
            return self.website_error()

        # PARSE HTML
        parsed_result = self.parse_search()
        if parsed_result:
            ret = "为您找到以下条目：\n\n"
            ret += parsed_result
            ret += f"\n请使用 [梗百科 {self.keyword} 序号] 展开对应序号的条目"
        else:
            ret = f"没有找到 [{self.keyword}] 相关的定义"
        return ret

    # GET DEFINITION
    def definition(self, seq='1'):
        if not seq.isdigit():
            return Util.bot_invalid_input_response()

        # SEQUENCE 0 -> LIST SEARCH RESULT
        seq = int(seq)
        if seq == 0:
            return self.do_search()

        # ACCESS SEARCH PAGE
        self.search_html = self.fetch_html(self.search_url)
        if self.search_html is None:
            return self.website_error()

        # GET EXACT DESCRIPTION ID
        did = self.get_did(seq)
        if did is False:
            if seq == 1:
                return f"没有找到 [{self.keyword}] 相关的定义"
            return Util.bot_invalid_input_response()
        if not did.isdigit():
            return self.website_error()

        # ACCESS DEFINITION PAGE
        self.definition_html = self.fetch_html(f"{self.definition_base_url}{did}?action=lite-card")
        if self.definition_html is None:
            return self.website_error()
        return self.parse_definition(seq)
