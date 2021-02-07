from PIL import Image
from PyQt5.QtWidgets import QLabel, QFrame, QScrollBar, QRadioButton

from controller.preview.preview_funcs import calculate_width_and_height_fit, calculate_width_and_height_stretch, \
    pil2pixmap
from model.model import MainModel
from model.preview import SpritePreviewMode


class SpritePreviewController:
    def __init__(self, label_preview_pixmap: QLabel, label_preview_title: QLabel, frame_preview_parent: QFrame):
        self.label_preview_pixmap = label_preview_pixmap
        self.label_preview_title = label_preview_title
        self.frame_preview_parent = frame_preview_parent

    def update_view(self):
        if self.sprite_preview_model.sprites is not None and self.sprite_preview_model.palette is not None:
            image = self.sprite_preview_model.get_selected_image()

            self._set_preview_image(image)
            self.label_preview_title.setText(f"Sprite {self.sprite_preview_model.selected_sprite + 1} Preview")
        else:
            self.label_preview_title.setText("Sprite ? Preview:")

    def _set_preview_image(self, image: Image):
        self._prepare_preview_label_size(image)

        pix = pil2pixmap(image)
        self.label_preview_pixmap.setPixmap(pix)

    def _prepare_preview_label_size(self, image):
        max_width = self.frame_preview_parent.width()
        max_height = self.frame_preview_parent.height()

        if self.sprite_preview_model.sprite_preview_mode == SpritePreviewMode.FIT:
            width, height = calculate_width_and_height_fit(image.width, image.height, max_width, max_height)
        else:
            width, height = calculate_width_and_height_stretch(image.width, image.height, max_width, max_height)

        self.label_preview_pixmap.setMaximumWidth(width)
        self.label_preview_pixmap.setMaximumHeight(height)

    def reset_scrollbar(self, scrollbar_preview: QScrollBar):
        scrollbar_preview.setValue(self.sprite_preview_model.selected_sprite)

        if self.sprite_preview_model.sprites is not None:
            scrollbar_preview.setMaximum(len(self.sprite_preview_model.sprites) - 1)

    @property
    def sprite_preview_model(self):
        return MainModel.get_model().sprite_preview
