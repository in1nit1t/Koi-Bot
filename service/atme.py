import jieba
import random

from core.util import Util

jieba.setLogLevel(jieba.logging.INFO)


class AtMe:

    # INIT SETTINGS
    def __init__(self, content):
        self.content = content

    # GENERATE REPLY
    def reply(self):
        if not self.content:
            return Util.bot_invalid_input_response()

        cut_words = jieba.lcut(self.content)
        if cut_words:
            corpora = Util.load_corpora_resource("anime_thesaurus")
            for word in cut_words:
                if corpora.__contains__(word):
                    return random.choice(corpora[word])
        return "咱还不太明白你的意思捏，等咱再学学>w<"
