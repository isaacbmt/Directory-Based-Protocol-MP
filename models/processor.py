# from multiprocessing import Process, Lock, freeze_support
from threading import Thread, Lock
from models.cacheL1 import CacheL1


class Processor(Thread):
    def __init__(self, id, lock: Lock, target, instruction, mode):
        super().__init__()
        self.lock = lock
        self.id = id
        self.cacheL1 = CacheL1()
        self.target = target
        self.instruction = instruction
        self.executed = False
        self.mode = mode
        self.step = False


    def run(self):
        # self.lock.acquire()
        self.target(self.id)
        print(f'P{self.id}:\n {self.cacheL1.get_information()[0]}\n {self.cacheL1.get_information()[1]}', '\n')
        # self.lock.release()

    def get_id(self):
        return self.id
