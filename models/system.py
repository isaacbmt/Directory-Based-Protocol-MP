import time

from models.processor import Processor
from models.cacheL2 import CacheL2
from models.memory import Memory
from threading import Lock
from msi import MSI
import logging


class System:
    def __init__(self, cache_l2: CacheL2, memory: Memory, lock: Lock):
        self.lock = lock
        self.processors = [Processor(0, lock, self.exe_instruction, [], 0),
                           Processor(1, lock, self.exe_instruction, [], 0),
                           Processor(2, lock, self.exe_instruction, [], 0),
                           Processor(3, lock, self.exe_instruction, [], 0)]
        self.cache_l2 = cache_l2
        self.memory = memory
        self.msi = MSI(self)

    def start(self):
        for i in range(len(self.processors)):
            self.processors[i].start()

    def change_mode(self, mode):
        for i in range(len(self.processors)):
            self.processors[i].lock.acquire()
            self.processors[i].mode = mode
            self.processors[i].lock.release()

    def exe_instruction(self, id):
        logging.debug('Using thread')
        # while True:
        self.msi.execute_instruction(id)

        print(f'mem: { self.memory.get_information() }')
        print(f'L2: { self.cache_l2.get_information() }')
        # for proc in self.processors:
        #     print(f'P{proc.get_id()}: {proc.cacheL1.get_information()}')
        time.sleep(2)
