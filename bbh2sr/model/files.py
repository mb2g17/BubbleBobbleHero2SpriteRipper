from typing import Optional

from extraction.palette import PaletteFile
from extraction.sprite import SpriteFile


class FileModel:
    def __init__(self):
        self._path: Optional[str] = None

    def set_path(self, new_path: Optional[str]):
        if new_path is not None and new_path != '':
            self._path = new_path

    @property
    def state_colour(self):
        return '6f6' if self.loaded else 'f66'

    @property
    def filename(self) -> str:
        return self._path.split('/')[::-1][0] if self._path is not None else ""

    @property
    def path(self) -> Optional[str]:
        return self._path

    @property
    def loaded(self) -> bool:
        return self._path is not None


class SpriteFileModel(FileModel):
    def extract_sprite_file(self):
        with open(self.path, 'rb') as sprite_file_handle:
            sprite_file = SpriteFile(sprite_file_handle)
            return sprite_file


class PaletteFileModel(FileModel):
    def extract_palette_file(self):
        with open(self.path, 'rb') as palette_file_handle:
            palette_file = PaletteFile(palette_file_handle)
            return palette_file
