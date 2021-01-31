import numpy as np
from PIL import Image

from .binary import BinaryFile


class SpriteFile(BinaryFile):
    def __init__(self, path):
        super().__init__(path)

    def get_all_sprites(self):
        return [self.get_sprite(i) for i in range(1, self.no_of_sprites() + 1)]

    def get_sprite(self, sprite_no):
        bytes = self.get_sprite_bytes(sprite_no)
        width = self.get_sprite_width(sprite_no)
        height = self.get_sprite_height(sprite_no)
        return Sprite(bytes, width, height)

    def get_sprite_bytes(self, sprite_no):
        sprite_width = self.get_sprite_width(sprite_no)
        sprite_height = self.get_sprite_height(sprite_no)

        start_index = 2 + 4 * self.no_of_sprites()

        if sprite_no > 0:
            for i in range(0, sprite_no):
                sprite_i_width = self.get_sprite_width(i)
                sprite_i_height = self.get_sprite_height(i)
                start_index += sprite_i_width * sprite_i_height

        end_index = start_index + sprite_width * sprite_height

        return self.get_bytes(start_index, end_index)

    def get_sprite_width(self, sprite_no):
        return self.get_short(4 * sprite_no + 2)

    def get_sprite_height(self, sprite_no):
        return self.get_short(4 * sprite_no + 4)

    def no_of_sprites(self):
        return self.get_short(0)


class Sprite:
    def __init__(self, bytes, width, height):
        self.bytes = bytes
        self.width = width
        self.height = height

    def create_image(self, palette_file):
        img = Image.new(mode="RGBA", size=(self.width, self.height), color=(255, 255, 255, 1))
        img_array = np.array(img)

        bytes_matrix = np.array(self.bytes)
        bytes_matrix.shape = (self.height, self.width)

        for y in range(0, self.height):
            for x in range(0, self.width):
                colour = bytes_matrix[y, x]
                [r, g, b] = palette_file.get_pixel(colour)
                a = 0 if colour == 0 else 255
                img_array[y, x] = [r, g, b, a]

        return Image.fromarray(img_array)

    def save_image(self, image_path, palette_file):
        img = self.create_image(palette_file)
        img.save(image_path)
