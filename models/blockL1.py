from models.block import Block


class BlockL1(Block):
    def __init__(self, block_number, state, addr, value):
        super().__init__(addr, value)
        self.block_number = block_number
        self.state = state

    def get_block_number(self):
        return self.block_number

    def get_state(self):
        return self.state

    def get_block_information(self):
        return [self.block_number, self.state, self.addr, self.value]
