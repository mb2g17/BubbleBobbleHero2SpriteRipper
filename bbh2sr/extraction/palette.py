from .binary import BinaryFile


class PaletteFile(BinaryFile):
    def get_pixel(self, index):
        start_index = 4 * index
        end_index = 4 * index + 3
        [b, g, r] = self.get_bytes(start_index, end_index)
        return [r, g, b]
