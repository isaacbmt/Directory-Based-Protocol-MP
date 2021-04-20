from models.cache import Cache
from models.blockL1 import BlockL1


class CacheL1(Cache):
    def __init__(self):
        self.blocks = [
            BlockL1(0, 'I', 0, 0),
            BlockL1(1, 'I', 0, 0)
        ]
        super().__init__(self.blocks)

    def set_value(self, addr, value, state):
        for i in range(len(self.blocks)):
            if self.blocks[i].addr == addr:
                self.blocks[i].state = state
                self.blocks[i].value = value
                break

    def set_new_value(self, addr, value, state):
        block_num = addr % 2
        for hierarchy in ['I', 'S', 'M']:
            if self.blocks[block_num].state == hierarchy:
                self.blocks[block_num].state = state
                self.blocks[block_num].value = value
                self.blocks[block_num].addr = addr
