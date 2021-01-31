from struct import unpack


class BinaryBlock:
    def __init__(self, block):
        self.block = block

    def get_bytes(self, start_index, end_index):
        return [self.get_byte(i) for i in range(start_index, end_index)]

    def get_byte(self, index):
        return self.block[index]

    def get_shorts(self, start_index, end_index):
        return [self.get_short(i) for i in range(start_index, end_index, 2)]

    def get_short(self, index):
        (num,) = unpack('h', bytes([self.block[index], self.block[index + 1]]))
        return num


class BinaryFile(BinaryBlock):
    def __init__(self, path):
        with open(path, mode='rb') as file:
            file_contents = file.read()
            file.close()

        super().__init__(file_contents)
