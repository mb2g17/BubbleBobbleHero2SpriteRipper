from enum import Enum
from typing import List, Optional

from PIL import Image
from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QFrame, QScrollBar, QRadioButton

from controller.files import FileLoader
from extraction.palette import PaletteFile
from extraction.sprite import Sprite, SpriteFile


class SpritePreviewMode(Enum):
    FIT = 0
    STRETCH = 1


class SpritePreviewController:
    def __init__(self, label_preview_title: QLabel,
                 label_preview_pixmap: QLabel,
                 frame_preview_parent: QFrame,
                 scrollbar_preview: QScrollBar,
                 radio_button_fit: QRadioButton,
                 radio_button_stretch: QRadioButton):
        self.label_preview_title = label_preview_title
        self.label_preview_pixmap = label_preview_pixmap
        self.frame_preview_parent = frame_preview_parent
        self.scrollbar_preview = scrollbar_preview
        self.radio_button_fit = radio_button_fit
        self.radio_button_stretch = radio_button_stretch

        self.sprites: Optional[List[Sprite]] = None
        self.palette: Optional[PaletteFile] = None
        self.selected_sprite = 0
        self.sprite_preview_mode = SpritePreviewMode.FIT

    def setup_view(self):
        self.scrollbar_preview.valueChanged.connect(self.on_scrollbar_preview_value_changed)
        self.radio_button_fit.toggled.connect(self.on_radio_button_clicked)
        self.radio_button_stretch.toggled.connect(self.on_radio_button_clicked)

    def on_scrollbar_preview_value_changed(self, value):
        self.selected_sprite = value
        self.update_view()

    def on_radio_button_clicked(self):
        fit = self.radio_button_fit.isChecked()
        self.sprite_preview_mode = SpritePreviewMode.FIT if fit else SpritePreviewMode.STRETCH
        self.update_view()

    def update_view(self):
        if self.sprites is not None and self.palette is not None:
            image = self.get_selected_image()

            self.set_preview_image(image)
            self.label_preview_title.setText(f"Sprite {self.selected_sprite + 1} Preview")
        else:
            self.label_preview_title.setText("Sprite ? Preview:")

    def get_selected_image(self):
        sprite = self.sprites[self.selected_sprite]
        image = sprite.create_image(self.palette)
        return image

    def set_preview_image(self, image: Image):
        self.prepare_preview_label_size(image)

        pix = self.pil2pixmap(image)
        self.label_preview_pixmap.setPixmap(pix)

    def prepare_preview_label_size(self, image):
        max_width = self.frame_preview_parent.width() - 20
        max_height = self.frame_preview_parent.height() - 20

        if self.sprite_preview_mode == SpritePreviewMode.FIT:
            width, height = self.calculate_width_and_height_fit(image.width, image.height, max_width, max_height)
        else:
            width, height = self.calculate_width_and_height_stretch(image.width, image.height, max_width, max_height)

        self.label_preview_pixmap.setMaximumWidth(width)
        self.label_preview_pixmap.setMaximumHeight(height)

    def calculate_width_and_height_fit(self, image_width, image_height, container_width, container_height):
        if image_width < container_width and image_height < container_height:
            return image_width, image_height
        else:
            return self.calculate_width_and_height_stretch(image_width, image_height, container_width, container_height)

    @staticmethod
    def calculate_width_and_height_stretch(image_width, image_height, container_width, container_height):
        width = container_width
        height = container_height
        image_ratio = image_width / image_height
        label_ratio = container_width / container_height
        if image_ratio > label_ratio:  # Thin
            width = container_width
            height = width * (image_height / image_width)
        else:  # Fat
            height = container_height
            width = height * (image_width / image_height)
        return width, height

    @staticmethod
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

    def update_files(self, sprite_file_loader: FileLoader, palette_file_loader: FileLoader):
        if sprite_file_loader.loaded and palette_file_loader.loaded:
            sprite_file, palette_file = self.extract_sprite_and_palette(sprite_file_loader, palette_file_loader)

            self.load_sprite_and_palette(sprite_file, palette_file)
            self.reset_scrollbar()

    @staticmethod
    def extract_sprite_and_palette(sprite_file_loader: FileLoader, palette_file_loader: FileLoader):
        with open(sprite_file_loader.path, 'rb') as sprite_file_handle, \
                open(palette_file_loader.path, 'rb') as palette_file_handle:
            sprite_file = SpriteFile(sprite_file_handle)
            palette_file = PaletteFile(palette_file_handle)

            return sprite_file, palette_file

    def load_sprite_and_palette(self, sprite_file: SpriteFile, palette_file: PaletteFile):
        self.sprites = sprite_file.get_all_sprites()
        self.palette = palette_file
        self.selected_sprite = 0

    def reset_scrollbar(self):
        self.scrollbar_preview.setValue(0)
        self.scrollbar_preview.setMaximum(len(self.sprites) - 1)
