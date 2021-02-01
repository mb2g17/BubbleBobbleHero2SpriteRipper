from PyQt5 import uic

from .files import FileLoader


class MainController:
    def __init__(self):
        self.sprite_file: FileLoader = FileLoader("Load Sprite", "Sprite Files (*.spp);;All Files (*)")
        self.palette_file: FileLoader = FileLoader("Load Palette", "Palette Files (*.pal);;All Files (*)")

        self._load_view()
        self._setup_view()
        self._update_view()

    def show(self):
        self.ui.show()

    def _load_view(self):
        self.ui = uic.loadUi("templates/main.ui")

    def _setup_view(self):
        self.ui.button_load_sprite.clicked.connect(self._on_button_load_sprite_clicked)
        self.ui.button_load_palette.clicked.connect(self._on_button_load_palette_clicked)

    def _update_view(self):
        label_sprite_path_text = self.sprite_file.filename if self.sprite_file.loaded else "No sprite loaded!"
        label_palette_path_text = self.palette_file.filename if self.palette_file.loaded else "No palette loaded!"

        self.ui.label_sprite_path.setText(label_sprite_path_text)
        self.ui.label_palette_path.setText(label_palette_path_text)

    def _on_button_load_sprite_clicked(self):
        self.sprite_file.load_file(self.ui)
        self._update_view()

    def _on_button_load_palette_clicked(self):
        self.palette_file.load_file(self.ui)
        self._update_view()
