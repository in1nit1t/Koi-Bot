import execjs

from core.util import Util


class JueJueZi:

    # JS ENGINE
    engine = execjs.compile(Util.load_script_resource("gen_jjz.js"))

    # GENERATE RANDOM
    @staticmethod
    def random_generate():
        return JueJueZi.engine.call("random_generate")

    # GENERATE THROUGH KEYWORD
    @staticmethod
    def generate(keyword):
        if len(keyword.split(' ')) == 2:
            return JueJueZi.engine.call("build", keyword)
        return Util.bot_invalid_input_response()
