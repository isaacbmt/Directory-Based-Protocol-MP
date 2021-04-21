from models.blockMem import BlockMem
from models.cache import Cache
import time


class Memory(Cache):
    def __init__(self):
        self.blocks = [
            BlockMem(0, 0),
            BlockMem(1, 0),
            BlockMem(2, 0),
            BlockMem(3, 0),
            BlockMem(4, 0),
            BlockMem(5, 0),
            BlockMem(6, 0),
            BlockMem(7, 0)
        ]
        super().__init__(self.blocks)

    def get_val(self, addr):
        time.sleep(0.5)
        for block in self.blocks:
            if addr == block.addr:
                return block.value

    def set_value(self, addr, value):
        time.sleep(0.6)
        for i in range(len(self.blocks)):
            if self.blocks[i].addr == addr:
                self.blocks[i].value = value
                break
