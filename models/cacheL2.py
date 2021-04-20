from models.cache import Cache
from models.blockL2 import BlockL2
from numpy import random


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
        for hierarchy in [0, 'DI', 'DS', 'DM']:
            blocks_indexes = self.get_blocks_by_state(hierarchy)
            if blocks_indexes:
                while blocks_indexes:
                    rand = random.binomial(len(blocks_indexes) - 1, 0.5)
                    replace_block = blocks_indexes[rand]
                    blocks_indexes.pop(rand)
                    if replace_block % 2 == addr % 2:
                        self.blocks[replace_block].state = state
                        self.blocks[replace_block].value = value
                        self.blocks[replace_block].addr = addr
                        break

    def get_blocks_by_state(self, state):
        indexes = []
        for i in range(len(self.blocks)):
            if self.blocks[i].state == state:
                indexes.append(i)
        return indexes

    def get_val(self, addr):
        for block in self.blocks:
            if addr == block.addr:
                return block.value

