# from multiprocessing import Process, Lock, freeze_support
from threading import Thread, Lock
from models.cacheL1 import CacheL1


class Processor(Thread):
    def __init__(self, id, lock: Lock, target, instruction, mode, instruction_old):
        super().__init__()
        self.lock = lock
        self.id = id
        self.cacheL1 = CacheL1()
        self.target = target
        self.instruction = instruction
        self.instruction_old = instruction_old
        self.executed = False
        self.mode = mode
        self.step = False

    def run(self):
        # self.lock.acquire()
        self.target(self.id)
        # self.lock.release()

    def get_id(self):
        return self.id
