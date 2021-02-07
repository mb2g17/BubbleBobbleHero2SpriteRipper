from enum import Enum
from typing import Optional, List

from PIL import Image

from extraction.palette import PaletteFile
from extraction.sprite import Sprite


class SpritePreviewMode(Enum):
    FIT = 0
    STRETCH = 1


class SpritePreviewModel:
    def __init__(self):
        self.sprites: Optional[List[Sprite]] = None
        self.palette: Optional[PaletteFile] = None
        self.selected_sprite = 0
        self.sprite_preview_mode = SpritePreviewMode.FIT

    def get_selected_image(self) -> Image:
        sprite = self.sprites[self.selected_sprite]
        image = sprite.create_image(self.palette)
        return image
