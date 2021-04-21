import time
from models.cacheL2 import CacheL2
from models.memory import Memory
from threading import Lock
from msi import MSI, Processor
import logging


class System:
    def __init__(self, cache_l2: CacheL2, memory: Memory, lock: Lock):
        self.lock = lock
        self.processors = [Processor(0, lock, self.exe_instruction, [], 0, []),
                           Processor(1, lock, self.exe_instruction, [], 0, []),
                           Processor(2, lock, self.exe_instruction, [], 0, []),
                           Processor(3, lock, self.exe_instruction, [], 0, [])]
        self.cache_l2 = cache_l2
        self.pause = True
        self.run_mode = 'step'
        self.memory = memory
        self.msi = MSI(self)
        self.counter = 0
        self.chosen_cpu = None
        self.run_while = True

    def start(self):
        for i in range(len(self.processors)):
            self.processors[i].start()

    def change_mode(self, mode, state):
        for i in range(len(self.processors)):
            # self.processors[i].lock.acquire()
            self.processors[i].mode = mode
            if mode == 0:
                self.processors[i].executed = state
            elif self.processors[i].get_id() != self.chosen_cpu:
                self.processors[i].executed = state

            # self.processors[i].lock.release()

    def end(self):
        self.run_while = False

    def pause_processors(self, id):
        self.processors[id].step = True

    def resume_stop_button(self, mode, run_mode, state):
        self.counter = 0
        self.pause = not self.pause
        self.run_mode = run_mode
        self.change_mode(mode, state)

    def resume_stop(self):
        self.pause = True

    def exe_instruction(self, id):
        logging.debug('Using thread')
        while self.run_while:
            if not self.pause:
                self.msi.execute_instruction(id)
            else:
                time.sleep(1)
