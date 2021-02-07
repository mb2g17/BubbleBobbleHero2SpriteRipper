import os
import webbrowser

from PyQt5 import uic, QtGui

from model.model import MainModel
from model.preview import SpritePreviewMode
from .actions import ActionsController
from .files import FileLoader, SpriteLoader, PaletteLoader
from controller.preview.preview import SpritePreviewController


class MainController:
    def __init__(self):
        model = MainModel.get_model()

        # Sets up file subcontrollers
        self.sprite_file: FileLoader = SpriteLoader()
        self.palette_file: FileLoader = PaletteLoader()

        # Sets up action subcontroller
        self.actions_controller = ActionsController()

        self._load_view()
        self._setup_view()
        self._update_view()

    def show(self):
        self.ui.show()

    def _load_view(self):
        self.ui = uic.loadUi("assets/templates/main.ui")

    def _setup_view(self):
        self.ui.button_load_sprite.clicked.connect(self._on_button_load_sprite_clicked)
        self.ui.button_load_palette.clicked.connect(self._on_button_load_palette_clicked)
        self.ui.button_export_sprites.clicked.connect(self._on_button_export_sprites_clicked)

        self.ui.scrollbar_preview.valueChanged.connect(self._on_scrollbar_preview_value_changed)
        self.ui.radio_button_fit.toggled.connect(self._on_radio_button_clicked)
        self.ui.radio_button_stretch.toggled.connect(self._on_radio_button_clicked)

        # Sets up sprite preview subcontroller
        self.sprite_preview_controller = SpritePreviewController(self.ui.label_preview_pixmap,
                                                                 self.ui.label_preview_title,
                                                                 self.ui.frame_preview_parent)

    def _update_view(self):
        model = MainModel.get_model()

        # Updates path texts
        label_sprite_path_text = model.sprite_file.filename if model.sprite_file.loaded else "No sprite loaded!"
        label_palette_path_text = model.palette_file.filename if model.palette_file.loaded else "No palette loaded!"

        self.ui.label_sprite_path.setText(label_sprite_path_text)
        self.ui.label_palette_path.setText(label_palette_path_text)

        # Updates sprite/palette colours
        self.ui.frame_sprite.setStyleSheet(f"background-color: #{model.sprite_file.state_colour}")
        self.ui.frame_palette.setStyleSheet(f"background-color: #{model.palette_file.state_colour}")

        # Updates export sprites button
        files_loaded = MainModel.get_model().sprite_file.loaded and MainModel.get_model().palette_file.loaded
        self.ui.button_export_sprites.setEnabled(files_loaded)

        self.sprite_preview_controller.update_view()

    def _on_button_load_sprite_clicked(self):
        self.sprite_file.load_file(self.ui)

        MainModel.get_model().update_sprite_preview_model()
        self.sprite_preview_controller.reset_scrollbar(self.ui.scrollbar_preview)

        self._update_view()

    def _on_button_load_palette_clicked(self):
        self.palette_file.load_file(self.ui)

        MainModel.get_model().update_sprite_preview_model()
        self.sprite_preview_controller.reset_scrollbar(self.ui.scrollbar_preview)

        self._update_view()

    def _on_button_export_sprites_clicked(self):
        self.actions_controller.export_sprites(self.ui.button_export_sprites)

        folder_name = MainModel.get_model().sprite_file.filename.split('.')[0]
        webbrowser.open(f"{folder_name}")

    def _on_scrollbar_preview_value_changed(self, value):
        MainModel.get_model().sprite_preview.selected_sprite = value
        self.sprite_preview_controller.update_view()

    def _on_radio_button_clicked(self):
        fit = self.ui.radio_button_fit.isChecked()
        MainModel.get_model().sprite_preview.sprite_preview_mode = SpritePreviewMode.FIT if fit else SpritePreviewMode.STRETCH
        self.sprite_preview_controller.update_view()
