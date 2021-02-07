from PyQt5.QtWidgets import QFileDialog, QWidget

from model.files import FileModel
from model.model import MainModel


class FileLoader:
    def __init__(self, model: FileModel, dialog_caption, dialog_filter):
        self.model = model
        self.dialog_caption = dialog_caption
        self.dialog_filter = dialog_filter

    def load_file(self, parent: QWidget):
        new_path = self._open_file_dialog(parent)
        self.model.set_path(new_path)

    def _open_file_dialog(self, parent: QWidget) -> str:
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            parent=parent,
            caption=self.dialog_caption,
            filter=self.dialog_filter,
            options=options)

        return file_name


class SpriteLoader(FileLoader):
    def __init__(self):
        super().__init__(MainModel.get_model().sprite_file, "Load Sprite", "Sprite Files (*.spp);;All Files (*)")


class PaletteLoader(FileLoader):
    def __init__(self):
        super().__init__(MainModel.get_model().palette_file, "Load Palette", "Palette Files (*.pal);;All Files (*)")
