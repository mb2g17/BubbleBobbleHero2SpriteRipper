from __future__ import annotations

from typing import Optional

from model.files import SpriteFileModel, PaletteFileModel
from model.preview import SpritePreviewModel


class MainModel:
    __instance: Optional[MainModel] = None

    def __init__(self):
        self.sprite_file = SpriteFileModel()
        self.palette_file = PaletteFileModel()
        self.sprite_preview = SpritePreviewModel()

        self.init_singleton()

    def init_singleton(self):
        if MainModel.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            MainModel.__instance = self

    @staticmethod
    def get_model():
        if MainModel.__instance is None:
            MainModel.__instance = MainModel()

        return MainModel.__instance

    def update_sprite_preview_model(self):
        if self.sprite_file.loaded and self.palette_file.loaded:
            sprite_file = self.sprite_file.extract_sprite_file()
            palette_file = self.palette_file.extract_palette_file()

            self.sprite_preview.sprites = sprite_file.get_all_sprites()
            self.sprite_preview.palette = palette_file
            self.sprite_preview.selected_sprite = 0
