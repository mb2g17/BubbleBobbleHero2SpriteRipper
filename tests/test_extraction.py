import unittest

from bbh2sr.extraction.binary import BinaryBlock


class TestExtractionBinary(unittest.TestCase):
    def setUp(self):
        byte_arr = bytes([0x12, 0x13, 0x14, 0x15, 0x16, 0x17])
        self.block = BinaryBlock(byte_arr)

    def test_binary_block_get_byte(self):
        byte = self.block.get_byte(1)
        self.assertEqual(byte, 19)

    def test_binary_block_get_bytes(self):
        byte_arr = self.block.get_bytes(1, 4)
        self.assertEqual(byte_arr, [19, 20, 21])

    def test_binary_block_get_short(self):
        short = self.block.get_short(1)
        self.assertEqual(short, 5139)

    def test_binary_block_get_shorts(self):
        shorts = self.block.get_shorts(0, 4)
        self.assertEqual(shorts, [4882, 5396])


if __name__ == '__main__':
    unittest.main()
