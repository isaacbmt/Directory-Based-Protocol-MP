from models.cache import Cache
from models.blockL1 import BlockL1


class CacheL1(Cache):
    def __init__(self):
        self.blocks = [
            BlockL1(0, 0, 0, 0),
            BlockL1(1, 0, 0, 0)
        ]
        super().__init__(self.blocks)

    def set_value(self, addr, value, state):
        for i in range(len(self.blocks)):
            if self.blocks[i].addr == addr:
                self.blocks[i].state = state
                self.blocks[i].value = value
                break

    def set_new_value(self, addr, value):
        if addr % 2 == 0:
            self.blocks[0].state = 'S'
            self.blocks[0].value = value
            self.blocks[0].addr = addr
        else:
            self.blocks[1].state = 'S'
            self.blocks[1].value = value
            self.blocks[1].addr = addr
