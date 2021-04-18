from threading import Thread
from models.cacheL1 import CacheL1


class Processor(Thread):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.cacheL1 = CacheL1()

    # def run(self):

    def get_id(self):
        return self.id
