from models.cache import Cache
from models.blockL2 import BlockL2


class CacheL2(Cache):
    def __init__(self):
        self.blocks = [
            BlockL2(0, 0, [], 0, 0),
            BlockL2(1, 0, [], 0, 0),
            BlockL2(2, 0, [], 0, 0),
            BlockL2(3, 0, [], 0, 0)
        ]
        super().__init__(self.blocks)

    def set_value(self, addr, value, state):
        for i in range(len(self.blocks)):
            if self.blocks[i].addr == addr:
                self.blocks[i].state = state
                self.blocks[i].value = value
                break

    def set_new_value(self, addr, value, state):
        for hierarchy in ['DI', 'DS', 'DM']:
            for i in range(len(self.blocks)):
                if self.blocks[i].state == hierarchy:
                    if self.blocks[i].block_number % 2 == addr % 2:
                        self.blocks[i].state = state
                        self.blocks[i].value = value
                        self.blocks[i].addr = addr
                    else:
                        self.blocks[i].state = state
                        self.blocks[i].value = value
                        self.blocks[i].addr = addr

    def get_val(self, addr):
        for block in self.blocks:
            if addr == block.addr:
                return block.value

