from PIL import Image
from PyQt5 import QtGui


def calculate_width_and_height_fit(image_width, image_height, container_width, container_height):
    if image_width < container_width and image_height < container_height:
        return image_width, image_height
    else:
        return calculate_width_and_height_stretch(image_width, image_height, container_width, container_height)


def calculate_width_and_height_stretch(image_width, image_height, container_width, container_height):
    image_ratio = image_width / image_height
    label_ratio = container_width / container_height
    if image_ratio > label_ratio:  # Thin
        width = container_width
        height = width * (image_height / image_width)
    else:  # Fat
        height = container_height
        width = height * (image_width / image_height)
    return width, height


def pil2pixmap(im: Image):
    if im.mode == "RGB":
        r, g, b = im.split()
        im = Image.merge("RGB", (b, g, r))
    elif im.mode == "RGBA":
        r, g, b, a = im.split()
        im = Image.merge("RGBA", (b, g, r, a))
    elif im.mode == "L":
        im = im.convert("RGBA")
    # Bild in RGBA konvertieren, falls nicht bereits passiert
    im2 = im.convert("RGBA")
    data = im2.tobytes("raw", "RGBA")
    qim = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_ARGB32)
    pixmap = QtGui.QPixmap.fromImage(qim)
    return pixmap
