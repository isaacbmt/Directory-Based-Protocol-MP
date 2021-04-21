from models.cache import Cache
from models.blockL2 import BlockL2
import time
from numpy import random


class CacheL2(Cache):
    def __init__(self):
        self.blocks = [
            BlockL2(0, 'DI', [], 0, 0),
            BlockL2(1, 'DI', [], 0, 0),
            BlockL2(2, 'DI', [], 0, 0),
            BlockL2(3, 'DI', [], 0, 0)
        ]
        super().__init__(self.blocks)

    def append_owners(self, addr, processorID):
        for i in range(len(self.blocks)):
            if self.blocks[i].addr == addr:
                self.blocks[i].owner_list.append(processorID)
                break

    def set_value(self, addr, value, state):
        for i in range(len(self.blocks)):
            if self.blocks[i].addr == addr:
                self.blocks[i].state = state
                self.blocks[i].value = value
                break

    def set_new_value(self, addr, value, state):
        for hierarchy in ['DI', 'DS', 'DM']:
            blocks_indexes = self.get_blocks_by_state(hierarchy)
            while blocks_indexes:
                rand = random.binomial(len(blocks_indexes) - 1, 0.5)
                replace_block = blocks_indexes[rand]
                blocks_indexes.pop(rand)
                if replace_block % 2 == addr % 2:
                    old_addr = self.blocks[replace_block].addr
                    old_val = self.blocks[replace_block].value
                    self.blocks[replace_block].state = state
                    self.blocks[replace_block].value = value
                    self.blocks[replace_block].addr = addr
                    if hierarchy != 'DI':
                        return [old_addr, old_val]
                    else:
                        return -1, -1

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

