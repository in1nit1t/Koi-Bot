import requests
import traceback

from core.util import Util
from core.logger import logger


class Music:

    api_url = "http://music.163.com/api/search/pc"

    # INIT SETTINGS
    def __init__(self, song_name):
        self.song_name = song_name

    # SEARCH SONG BY API
    def api_search_song(self):
        data = {
            "s": self.song_name,
            "type": 1,
            "offset": 0,
            "limit": 15
        }
        try:
            result = requests.post(Music.api_url, data=data).json()
            return result["result"]["songs"] if result["code"] == 200 else []
        except:
            logger.error(f"<网易云音乐> 搜索 /{self.song_name}/ 时 API 调用失败", traceback.format_exc())

    # GET SONG ID
    def get_sid(self, seq):
        seq -= 1
        songs = self.api_search_song()
        if 0 <= seq < len(songs):
            return songs[seq]["id"]
        return False

    # LIST SEARCHING RESULT
    def do_search(self):
        songs = self.api_search_song()
        if not songs:
            return f"没有找到与 [{self.song_name}] 相关的歌曲~"

        ret = "为您找到以下条目：\n\n"
        for idx, song in enumerate(songs):
            name = song["name"]
            artists = [entry["name"] for entry in song["artists"]]
            ret += f"{idx+1}. {name} - {', '.join(artists)}\n"
        ret += f"\n请使用 [点歌 {self.song_name} 序号] 选取序号对应的歌曲"
        return ret

    # ORDER SONG
    def order(self, seq='1'):
        if not seq.isdigit():
            return Util.bot_invalid_input_response()

        # SEQUENCE 0 -> LIST SEARCH RESULT
        seq = int(seq)
        if seq == 0:
            return self.do_search()

        # GET SONG ID & RETURN PACKED MESSAGE
        sid = self.get_sid(seq)
        if sid is False:
            if seq == 1:
                return f"没有找到与 [{self.song_name}] 相关的歌曲~"
            return Util.bot_invalid_input_response()
        return Util.music_163_pack(sid)
