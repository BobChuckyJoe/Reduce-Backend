import base64
from io import BytesIO

from PIL import Image


def to_base64(img: Image):
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    img_b64 = base64.b64encode(buffer.getvalue())

    return img_b64


def to_img(base64_img):
    decoded = base64.b64decode(base64_img)
    img = Image.open(BytesIO(decoded))

    return img
