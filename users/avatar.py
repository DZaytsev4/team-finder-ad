import hashlib
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

AVATAR_SIZE_PX = 200
COLOR_BASE = 80
COLOR_MOD = 100

DEFAULT_FONT_SIZE = 100
TEXT_Y_OFFSET = 6
TEXT_FILL_RGB = (255, 255, 255)

AVATAR_IMAGE_MODE = "RGB"
FONT_ARIAL = "arial.ttf"
FONT_DEJAVU = "DejaVuSans.ttf"


def build_letter_avatar(letter: str) -> ContentFile:
    """Создаёт PNG-аватар с первой буквой имени на мягком фоне."""
    ch = (letter or "?")[:1].upper()
    size = AVATAR_SIZE_PX
    h = hashlib.md5(ch.encode("utf-8"), usedforsecurity=False).hexdigest()
    r = COLOR_BASE + int(h[0:2], 16) % COLOR_MOD
    g = COLOR_BASE + int(h[2:4], 16) % COLOR_MOD
    b = COLOR_BASE + int(h[4:6], 16) % COLOR_MOD
    image = Image.new(AVATAR_IMAGE_MODE, (size, size), color=(r, g, b))
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype(FONT_ARIAL, DEFAULT_FONT_SIZE)
    except OSError:
        try:
            font = ImageFont.truetype(FONT_DEJAVU, DEFAULT_FONT_SIZE)
        except OSError:
            font = ImageFont.load_default()
    if hasattr(font, "getbbox"):
        x0, y0, x1, y1 = font.getbbox(ch)
        tw, th = x1 - x0, y1 - y0
    else:
        tw, th = font.getsize(ch)
    draw.text(
        ((size - tw) / 2, (size - th) / 2 - TEXT_Y_OFFSET),
        ch,
        fill=TEXT_FILL_RGB,
        font=font,
    )
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return ContentFile(buffer.read(), name=f"avatar_{ch}.png")
