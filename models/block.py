class Block:
    def __init__(self, addr, value):
        self.addr = addr
        self.value = value

    def get_address(self):
        return self.addr

    def get_value(self):
        return self.value
