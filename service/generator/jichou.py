import textwrap
import traceback
from PIL import ImageFont, ImageDraw, Image

from core.util import Util
from core.logger import logger


class JiChou:

    # INIT SETTINGS
    def __init__(self, content):
        self.content = content.replace('\n', '').strip()

    # BUILD PICTURE
    def build_picture(self, new=True):
        try:
            text = textwrap.wrap(self.content, width = 15 if new else 18)
            font = ImageFont.truetype(Util.get_font_resource("WenQuanYi Micro Hei.ttf"), 20 if new else 50)
            image = Image.open(Util.get_image_resource("jichou", "jichou.jpg" if new else "jichou_old.jpg"))
            image_width, image_height = image.size
            draw = ImageDraw.Draw(image)

            # DRAW EACH LINE
            current_y = 291 if new else 770
            for idx, line in enumerate(text):
                line_width, line_height = draw.textsize(line, font=font)
                current_x = (image_width - line_width) // 2
                draw.text((current_x, current_y), line, font=font, fill=(0, 0, 0))
                current_y += line_height
            current_y += 5 if new else 10

            # CROP IF SHORTER
            if current_y < image_height:
                image = image.crop((0, 0, image_width, current_y))
            return "记下来了哟~\n" + Util.base64_picture_pack(Util.picture2base64(image))
        except:
            logger.error("<记仇表情包> 生成失败", traceback.format_exc())
            return Util.bot_error_response()

    # TOP LAYER
    def generate(self, new=True):
        if not self.content:
            return "想记点啥？"
        if (new and len(self.content) > 100) or (not new and len(self.content) > 180):
            return "感受到你的一袋米了，咱能记得少点吗"
        return self.build_picture(new)
