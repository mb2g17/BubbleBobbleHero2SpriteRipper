import unittest
from io import BytesIO

from bbh2sr.extraction.palette import PaletteFile
from bbh2sr.extraction.sprite import SpriteFile


class TestSpriteFile(unittest.TestCase):
    def setUp(self):
        self.set_up_palette()
        self.set_up_sprites()

    def set_up_palette(self):
        byte_arr = bytes([0x0, 0x0, 0x0, 0x0,  # Black
                          0xaa, 0xbb, 0xcc, 0x00,  # Colour
                          0xFF, 0xFF, 0xFF  # White
                          ])
        byte_io = BytesIO()
        byte_io.write(byte_arr)
        byte_io.seek(0)

        self.palette_file = PaletteFile(byte_io)
        byte_io.close()

    def set_up_sprites(self):
        byte_arr = bytes([0x3, 0x0,  # Three sprites
                          0x2, 0x0, 0x2, 0x0,  # 1) 2x2
                          0x1, 0x0, 0x3, 0x0,  # 2) 1x3
                          0x1, 0x0, 0x1, 0x0,  # 3) 1x1
                          0x0, 0x1, 0x2, 0x1,  # 1) multi-coloured
                          0x2, 0x2, 0x2,  # 2) all white
                          0x0  # 3) all black
                          ])
        byte_io = BytesIO()
        byte_io.write(byte_arr)
        byte_io.seek(0)

        self.sprite_file = SpriteFile(byte_io)
        byte_io.close()

    def test_sprite_file_no_of_sprites(self):
        no_of_sprites = self.sprite_file.no_of_sprites()
        self.assertEqual(no_of_sprites, 3)

    def test_sprite_file_sprite_1_width(self):
        sprite_1_width = self.sprite_file.get_sprite_width(0)
        self.assertEqual(sprite_1_width, 2)

    def test_sprite_file_sprite_1_height(self):
        sprite_1_height = self.sprite_file.get_sprite_height(0)
        self.assertEqual(sprite_1_height, 2)

    def test_sprite_file_sprite_1_bytes(self):
        sprite_1_bytes = self.sprite_file.get_sprite_bytes(0)
        self.assertEqual(sprite_1_bytes, [0, 1, 2, 1])

    def test_sprite_file_sprite_2_width(self):
        sprite_2_width = self.sprite_file.get_sprite_width(1)
        self.assertEqual(sprite_2_width, 1)

    def test_sprite_file_sprite_2_height(self):
        sprite_2_height = self.sprite_file.get_sprite_height(1)
        self.assertEqual(sprite_2_height, 3)

    def test_sprite_file_sprite_2_bytes(self):
        sprite_2_bytes = self.sprite_file.get_sprite_bytes(1)
        self.assertEqual(sprite_2_bytes, [2, 2, 2])

    def test_sprite_file_sprite_3_width(self):
        sprite_3_width = self.sprite_file.get_sprite_width(2)
        self.assertEqual(sprite_3_width, 1)

    def test_sprite_file_sprite_3_height(self):
        sprite_3_height = self.sprite_file.get_sprite_height(2)
        self.assertEqual(sprite_3_height, 1)

    def test_sprite_file_sprite_3_bytes(self):
        sprite_3_bytes = self.sprite_file.get_sprite_bytes(2)
        self.assertEqual(sprite_3_bytes, [0])

    def test_sprite_file_get_sprite_1(self):
        sprite_1 = self.sprite_file.get_sprite(0)
        self.assertEqual(sprite_1.width, 2)
        self.assertEqual(sprite_1.height, 2)
        self.assertEqual(sprite_1.bytes, [0, 1, 2, 1])

    def test_sprite_file_get_sprite_2(self):
        sprite_2 = self.sprite_file.get_sprite(1)
        self.assertEqual(sprite_2.width, 1)
        self.assertEqual(sprite_2.height, 3)
        self.assertEqual(sprite_2.bytes, [2, 2, 2])

    def test_sprite_file_get_sprite_3(self):
        sprite_3 = self.sprite_file.get_sprite(2)
        self.assertEqual(sprite_3.width, 1)
        self.assertEqual(sprite_3.height, 1)
        self.assertEqual(sprite_3.bytes, [0])


class TestSprite(unittest.TestCase):
    def setUp(self):
        self.set_up_palette()
        self.set_up_sprites()
        self.set_up_sprite()

    def set_up_palette(self):
        byte_arr = bytes([0x0, 0x0, 0x0, 0x0,  # Black
                          0xaa, 0xbb, 0xcc, 0x00,  # Colour
                          0xFF, 0xFF, 0xFF  # White
                          ])
        byte_io = BytesIO()
        byte_io.write(byte_arr)
        byte_io.seek(0)

        self.palette_file = PaletteFile(byte_io)
        byte_io.close()

    def set_up_sprites(self):
        byte_arr = bytes([0x1, 0x0,  # One sprite
                          0x2, 0x0, 0x2, 0x0,  # 2x2
                          0x0, 0x1, 0x2, 0x1,  # multi-coloured
                          ])
        byte_io = BytesIO()
        byte_io.write(byte_arr)
        byte_io.seek(0)

        self.sprite_file = SpriteFile(byte_io)
        byte_io.close()

    def set_up_sprite(self):
        self.sprite = self.sprite_file.get_sprite(0)

    def test_sprite_create_image(self):
        image = self.sprite.create_image(self.palette_file)
        self.assertEqual(image.getpixel((0, 0)), (0, 0, 0, 0))
        self.assertEqual(image.getpixel((1, 0)), (204, 187, 170, 255))
        self.assertEqual(image.getpixel((0, 1)), (255, 255, 255, 255))
        self.assertEqual(image.getpixel((1, 1)), (204, 187, 170, 255))


if __name__ == '__main__':
    unittest.main()
