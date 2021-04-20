from models.block import Block


class BlockL2(Block):
    def __init__(self, block_number, state, owner_list, addr, value):
        super().__init__(addr, value)
        self.block_number = block_number
        self.state = state
        self.owner_list = owner_list

    def get_block_number(self):
        return self.block_number

    def get_state(self):
        return self.state

    def get_owner_list(self):
        return self.owner_list

    def get_block_information(self):
        return [self.block_number, self.state, str(self.owner_list), bin(self.addr), hex(self.value)]
