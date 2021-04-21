import time


class Cache:
    def __init__(self, blocks):
        self.blocks = blocks

    def find_address(self, addr):
        time.sleep(2)
        for block in self.blocks:
            if block.addr == addr:
                return [True, block.state]
        return [False, -1]

    def set_state(self, addr, state):
        time.sleep(3)
        for i in range(len(self.blocks)):
            if self.blocks[i].addr == addr:
                self.blocks[i].state = state
                break

    def get_information(self):
        info = []
        for block in self.blocks:
            info.append(block.get_block_information())
        return info
