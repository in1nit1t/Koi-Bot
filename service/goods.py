import os
import shutil
import hashlib
import traceback

from core.logger import logger
from core.setting import setting
from core.util import Util, CQHTTP

from dao.order import OrderDAO
from service.bilibili import Bilibili


class Goods:

    # INIT SETTINGS
    def __init__(self, uin=None):
        self.uin = uin
        self.order_dao = OrderDAO()

    # GET POINTS
    def points_status(self):
        uid = self.order_dao.get_uid_by_uin(self.uin)
        if not uid:
            return Util.bot_error_response()

        points = self.order_dao.select_points(uid)
        if points:
            return f"你目前有 {points[0]} 点积分~"
        return Util.bot_error_response()

    # LIST EXCHANGE GOODS
    def exchange_list(self):
        goods = self.order_dao.select_all_unexpired_goods()
        if not goods:
            return "还没有东西可以兑换捏~"

        # COMMON GOODS
        msg = "可兑换物品：\n"
        common_goods = [thing for thing in goods if thing[4] is None]
        for idx, thing in enumerate(common_goods):
            name, description, _, price, expire_time = thing
            if expire_time is None:
                msg += f"\n{idx+1}. {name}({price}积分)：{description}"

        # TIME LIMITED GOODS
        time_limited_goods = [thing for thing in goods if thing[4] is not None]
        if time_limited_goods:
            msg += f"\n{'-' * 20}\n！！！限时物品！！！\n"
            for idx, thing in enumerate(time_limited_goods):
                name, description, _, price, expire_time = thing
                msg += f"\n{idx+1}. {name}({price}积分)：{description}，将于 {expire_time} 停止兑换"
        return msg

    # PACK VOICE GOODS
    @staticmethod
    def voice_goods_pack(name, description):
        avatar_url = Bilibili(setting["account"]["bilibili"]["koi_uid"]).get_avatar_url()

        # COPY FILE TO WEB DIRECTORY
        root_dir = setting["misc"]["web"]["root_directory"]
        target_dir = os.path.join(root_dir, "koibot/goods/")
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        hash_value = hashlib.md5(f"{name}koi{description}".encode()).hexdigest()
        target_path = os.path.join(target_dir, f"{hash_value}.mp3")
        if not os.path.exists(target_path):
            try:
                shutil.copyfile(Util.get_goods_resource(name + ".mp3"), target_path)
            except:
                logger.error(f"<积分兑换> 音频 /{name}/ 拷贝失败", traceback.format_exc())
                return None

        # PACK & SEND
        music_url = f"{setting['misc']['web']['host']}/koibot/goods/{hash_value}.mp3"
        return Util.music_custom_music_pack(music_url, name, description, avatar_url)

    # FINISH ORDER
    def finish_order(self, order_id):
        if not Util.is_friend(self.uin):
            return "兑换成功！但我们还不是好友捏，快来加我领取学习资料吧♂"

        order = self.order_dao.select_order_by_id(order_id)
        if not order:
            CQHTTP.send_private_message("没有找到订单捏", self.uin)
            return None

        # GET ORDER INFO
        _, _, goods_id, completed, _, _ = order
        if completed:
            CQHTTP.send_private_message("肿么回事，明明订单已完成了呀", self.uin)
            return None

        # GET GOODS INFO
        goods = self.order_dao.select_goods_by_id(goods_id)
        if not goods:
            return Util.bot_error_response()
        name, description, goods_type, _, _ = goods

        # PACK GOODS MESSAGE
        msg = None
        if goods_type == "voice":
            msg = self.voice_goods_pack(name, description)
        # elif goods_type == "picture"

        if not msg:
            CQHTTP.send_private_message(Util.bot_error_response(), self.uin)
            return None

        # SEND GOODS MESSAGE
        CQHTTP.send_private_message(f"这是你兑换的 [{name}]，收好了捏~", self.uin)
        if CQHTTP.send_private_message(msg, self.uin):
            self.order_dao.update_order_status(order_id)
            return "兑换成功！物品已发送，请查收~"
        else:
            msg = f"订单id：{order_id}\n品名：{name}\n商品类型：{goods_type}\n兑换人qq：{self.uin}\n兑换失败"
            logger.warning("<积分兑换> 发送商品失败", msg, True)
            CQHTTP.send_private_message("我超，出了点问题，自我维修功能启动中...", self.uin)
            return None

    # DO EXCHANGE
    def exchange(self, goods_name):
        uid = self.order_dao.get_uid_by_uin(self.uin)
        if not uid:
            return Util.bot_error_response()

        goods = self.order_dao.select_unexpired_goods_by_name(goods_name)
        if not goods:
            return f"没有找到 [{goods_name}] 捏"
        goods_id, _, price, expire_time = goods

        # CHECK IF USER HAD BOUGHT BEFORE
        history = self.order_dao.select_order_by_uid_gid(uid, goods_id)
        if history:
            return "你已经兑换过这个物品辣~"

        # CHECK USER POINTS
        points = self.order_dao.select_points(uid)
        if not points:
            return Util.bot_error_response()
        if points[0] < price:
            return "积分不足！"

        # GENERATE ORDER & TYR TO FINISH
        order_id = self.order_dao.insert_order(uid, goods_id)
        if order_id and self.order_dao.update_points(uid, price, False):
            return self.finish_order(order_id)
        else:
            return "订单创建失败呜呜呜"
