import os
import shutil
from threading import Thread

from PyQt5.QtWidgets import QPushButton

from extraction.palette import PaletteFile
from extraction.sprite import SpriteFile
from model.model import MainModel


class ActionsController:
    @staticmethod
    def export_sprites(button: QPushButton):
        model = MainModel.get_model()

        if model.sprite_file.loaded and model.palette_file.loaded:

            button.setText("Exporting sprites...")
            button.setEnabled(False)

            folder_name = MainModel.get_model().sprite_file.filename.split('.')[0]
            if os.path.isdir(folder_name):
                shutil.rmtree(f"./{folder_name}")
            os.makedirs(folder_name)

            def export_sprites():
                with open(model.sprite_file.path, 'rb') as sprite_file_handle, \
                        open(model.palette_file.path, 'rb') as palette_file_handle:
                    sprite_file = SpriteFile(sprite_file_handle)
                    palette_file = PaletteFile(palette_file_handle)

                    sprites = sprite_file.get_all_sprites()

                    for (index, sprite) in enumerate(sprites):
                        with open(f"./{folder_name}/sprite-{index}.png", 'wb') as image_file_handle:
                            sprite.save_image(image_file_handle, palette_file)

                    sprite_file_handle.close()
                    palette_file_handle.close()

                button.setText("Export Sprites")
                button.setEnabled(True)

            thread = Thread(target=export_sprites)
            thread.start()
