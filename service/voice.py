import random

from core.setting import setting
from core.util import Util, CQHTTP
from dao.voice import VoiceDAO


class Voice:

    koi_qq = setting["account"]["qq"]["koi"]

    # INIT SETTINGS
    def __init__(self, to):
        self.to = to
        self.voice_dao = VoiceDAO()

    # SEND VOICE
    def send(self, vid, filename):
        data = CQHTTP.send_group_message(Util.online_voice_pack(filename))
        if data:
            second_message = Util.at_pack(f"收好了捏，本条语音id：{vid}", self.to)
            CQHTTP.send_group_message(second_message)

    # RETURN KOI'S VOICE RANDOMLY
    def koi_voice(self):
        voices = self.voice_dao.get_voice_by_uin(self.koi_qq)
        if voices:
            voice = random.choice(voices)
            return self.send(voice[0], voice[3])
        return "koi你说句话呀QAQ"

    # SEARCH VOICE BY TAG
    def voice_search(self, tag):
        voices = self.voice_dao.select_voice_by_tag(tag)
        if voices:
            voice = random.choice(voices)
            return self.send(voice[0], voice[3])
        return f"没有找到与标签 [{tag}] 相关的语音捏~"

    # GET OTHER'S VOICE
    def others_voice(self, uin):
        if uin == self.koi_qq:
            return self.koi_voice()

        voices = self.voice_dao.get_voice_by_uin(uin)
        if voices:
            voice = random.choice(voices)
            return self.send(voice[0], voice[3])

        # TARGET DOESN'T HAVE VOICE
        data = CQHTTP.group_member_info(uin)
        return f"{data['nickname'] if data else '宝'}你说句话呀QAQ"

    # MANAGE VOICE THROUGH ID
    def manage_voice(self, vid, op, param=''):
        voice = self.voice_dao.select_voice_by_id(vid)
        if not voice:
            return "没有找到这条语音捏~"

        if param:
            # OPERATION WITH PARAM
            if op == "更新标签" and Util.has_high_privilege(self.to):
                # UPDATE TAG
                if self.voice_dao.update_tag_by_id(vid, param):
                    return "标签更新成功☆"
                return Util.bot_error_response()
        else:
            # OPERATION WITHOUT PARAM
            if op == "播放":
                # PLAY VOICE
                self.send(vid, voice[3])
            elif op == "删除" and Util.has_high_privilege(self.to):
                # DELETE VOICE
                if self.voice_dao.delete_voice_by_id(vid):
                    return "语音删除成功★"
                return Util.bot_error_response()
            elif op == "标签":
                # SHOW TAG
                tag = voice[5]
                return f"本条语音的标签为：{tag}" if tag else "这条语音还没有标签捏~"
