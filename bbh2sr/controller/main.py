from threading import Thread

from PyQt5 import uic

from .files import FileLoader
from extraction.palette import PaletteFile
from extraction.sprite import SpriteFile
from .preview import SpritePreviewController


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
        self.ui.button_export_sprites.clicked.connect(self._on_button_export_sprites_clicked)

        self.sprite_preview_controller = SpritePreviewController(
            self.ui.label_preview_title,
            self.ui.label_preview_pixmap,
            self.ui.frame_preview_parent,
            self.ui.scrollbar_preview,
            self.ui.radio_button_fit,
            self.ui.radio_button_stretch)
        self.sprite_preview_controller.setup_view()

    def _update_view(self):
        # Updates path texts
        label_sprite_path_text = self.sprite_file.filename if self.sprite_file.loaded else "No sprite loaded!"
        label_palette_path_text = self.palette_file.filename if self.palette_file.loaded else "No palette loaded!"

        # Updates sprite/palette colours
        loaded_sprite = self.sprite_file.loaded
        loaded_palette = self.palette_file.loaded
        self.ui.frame_sprite.setStyleSheet(f"background-color: #{'6f6' if loaded_sprite else 'f66'}")
        self.ui.frame_palette.setStyleSheet(f"background-color: #{'6f6' if loaded_palette else 'f66'}")

        self.ui.label_sprite_path.setText(label_sprite_path_text)
        self.ui.label_palette_path.setText(label_palette_path_text)
        self.ui.button_export_sprites.setEnabled(self._files_loaded)

        self.sprite_preview_controller.update_view()

    @property
    def _files_loaded(self) -> bool:
        return self.sprite_file.loaded and self.palette_file.loaded

    def _on_button_load_sprite_clicked(self):
        self.sprite_file.load_file(self.ui)
        self.sprite_preview_controller.update_files(self.sprite_file, self.palette_file)

        self._update_view()

    def _on_button_load_palette_clicked(self):
        self.palette_file.load_file(self.ui)
        self.sprite_preview_controller.update_files(self.sprite_file, self.palette_file)

        self._update_view()

    def _on_button_export_sprites_clicked(self):
        if self.sprite_file.loaded and self.palette_file.loaded:

            self.ui.button_export_sprites.setText("Exporting sprites...")
            self.ui.button_export_sprites.setEnabled(False)

            def export_sprites():
                with open(self.sprite_file.path, 'rb') as sprite_file_handle, \
                     open(self.palette_file.path, 'rb') as palette_file_handle:
                    sprite_file = SpriteFile(sprite_file_handle)
                    palette_file = PaletteFile(palette_file_handle)

                    sprites = sprite_file.get_all_sprites()

                    for (index, sprite) in enumerate(sprites):
                        with open(f"sprite-{index}.png", 'wb') as image_file_handle:
                            sprite.save_image(image_file_handle, palette_file)

                    sprite_file_handle.close()
                    palette_file_handle.close()

                self.ui.button_export_sprites.setText("Export Sprites")
                self.ui.button_export_sprites.setEnabled(True)

            thread = Thread(target=export_sprites)
            thread.start()
