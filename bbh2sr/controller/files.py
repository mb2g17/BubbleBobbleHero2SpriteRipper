from typing import Optional

from PyQt5.QtWidgets import QFileDialog, QWidget


class FileLoader:
    def __init__(self, dialog_caption, dialog_filter):
        self.dialog_caption = dialog_caption
        self.dialog_filter = dialog_filter

        self.path: Optional[str] = None

    def load_file(self, parent: QWidget):
        new_path = self._open_file_dialog(parent)

        if new_path is not None:
            self.path = new_path

    def _open_file_dialog(self, parent: QWidget) -> Optional[str]:
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            parent=parent,
            caption=self.dialog_caption,
            filter=self.dialog_filter,
            options=options)

        return None if file_name == "" else file_name

    @property
    def filename(self) -> str:
        return self.path.split('/')[::-1][0] if self.path is not None else ""

    @property
    def loaded(self) -> bool:
        return self.path is not None
