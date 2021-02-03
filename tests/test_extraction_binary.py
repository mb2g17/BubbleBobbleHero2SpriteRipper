import unittest

from bbh2sr.extraction.binary import BinaryBlock


class TestExtractionBinary(unittest.TestCase):
    def test_binary_block_get_byte(self):
        block = BinaryBlock(bytes([0x13]))
        byte = block.get_byte(0)
        self.assertEqual(byte, 19)


if __name__ == '__main__':
    unittest.main()
