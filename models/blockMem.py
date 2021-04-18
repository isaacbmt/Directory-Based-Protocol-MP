from models.block import Block


class BlockMem(Block):
    def __init__(self, addr, value):
        super().__init__(addr, value)

    def get_block_information(self):
        return [self.addr, self.value]
