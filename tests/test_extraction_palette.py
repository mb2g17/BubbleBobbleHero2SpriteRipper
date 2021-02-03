import unittest
from io import BytesIO

from extraction.palette import PaletteFile


class TestPaletteFile(unittest.TestCase):
    def setUp(self):
        byte_arr = bytes([0x0, 0x0, 0x0, 0x0,
                          0xaa, 0xbb, 0xcc, 0x00,
                          0xFF, 0xFF, 0xFF])
        byte_io = BytesIO()
        byte_io.write(byte_arr)
        byte_io.seek(0)

        self.palette_file = PaletteFile(byte_io)
        byte_io.close()

    def test_palette_file_get_pixel_1(self):
        pixel = self.palette_file.get_pixel(0)
        self.assertEqual(pixel, [0, 0, 0])

    def test_palette_file_get_pixel_2(self):
        pixel = self.palette_file.get_pixel(1)
        self.assertEqual(pixel, [204, 187, 170])

    def test_palette_file_get_pixel_3(self):
        pixel = self.palette_file.get_pixel(2)
        self.assertEqual(pixel, [255, 255, 255])


if __name__ == '__main__':
    unittest.main()
