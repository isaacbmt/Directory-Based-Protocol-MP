from utils.utils import create_instruction, format_instruction
from models.processor import Processor
import time


class MSI:
    def __init__(self, system):
        self.system = system
        self.current_instruction = ''

    def step_mode(self, processorID):
        self.continuous_mode(processorID)
        # self.system.resume_stop()

    def continuous_mode(self, processorID):
        if self.system.processors[processorID].mode == 0 and not self.system.processors[processorID].executed:
            print(f'ejecuto cococo: {self.system.processors[processorID].instruction}')
            self.system.processors[processorID].executed = False
            self.system.processors[processorID].instruction = create_instruction(processorID)
        else:
            print(f'ejecuto lololo: {self.system.processors[processorID].instruction}')

    def execute_instruction(self, processorID):
        self.continuous_mode(processorID)
        if self.system.processors[processorID].executed or not self.system.processors[processorID].instruction:
            return self.finish(processorID)

        pid, instr_type, addr, val = self.system.processors[processorID].instruction
        # self.system.processors[processorID].instruction = self.current_instruction
        print(f'P{processorID} ejecuta: {format_instruction(self.system.processors[processorID].instruction)}')
        if instr_type == 'READ':
            self.read_l2(processorID, addr)
        elif instr_type == 'WRITE':
            self.write_l2(processorID, addr, val)
        else:
            print('Estoy ejecutando un CALC')
            self.finish(processorID)

    def write_l2(self, processorID, addr, val):
        isInCacheL2, stateL2 = self.system.cache_l2.find_address(addr)
        print(f'before P{processorID}: {self.system.cache_l2.get_information()}')
        self.write_mem(processorID, addr)
        if isInCacheL2:
            if stateL2 == 'DS':
                print('ds')
                self.system.processors[processorID].lock.acquire()
                self.system.cache_l2.set_value(addr, val, 'DM')
                self.system.processors[processorID].lock.release()
            elif stateL2 == 'DM':
                print('dm')
                self.system.processors[processorID].lock.acquire()
                self.system.cache_l2.set_value(addr, val, 'DM')
                self.system.processors[processorID].lock.release()
            elif stateL2 == 'DI':
                print('di')
                self.system.processors[processorID].lock.acquire()
                self.system.cache_l2.set_value(addr, val, 'DM')
                self.system.processors[processorID].lock.release()
            else:
                print('else')
                self.system.processors[processorID].lock.acquire()
                self.system.cache_l2.set_value(addr, val, 'DM')
                self.system.processors[processorID].lock.release()
        else:
            self.system.processors[processorID].lock.acquire()
            old_addr, old_val = self.system.cache_l2.set_new_value(addr, val, 'DM')
            # isInCacheL2Old, stateL2Old = self.system.cache_l2.find_address(old_addr)
            # if isInCacheL2Old and stateL2Old == 'DM':
            #     self.system.cache_l2.set_state(old_addr, 'DI')
            #     self.system.memory.set_value(old_addr, old_val)
            if old_addr != -1:
                self.flush_caches(processorID, old_addr)
            self.system.processors[processorID].lock.release()
        self.write_l1(processorID, addr, val)

    def read_l2(self, processorID, addr):
        isInCacheL2, stateL2 = self.system.cache_l2.find_address(addr)
        if isInCacheL2:
            if stateL2 == 'DS':
                print('Share')
                self.system.processors[processorID].lock.acquire()
                val = self.system.cache_l2.get_val(addr)
                self.system.processors[processorID].lock.release()
                self.read_l1(processorID, addr, val)
            elif stateL2 == 'DM':
                print('Modify')
                self.system.processors[processorID].lock.acquire()
                val = self.system.cache_l2.get_val(addr)
                self.system.memory.set_value(addr, val)
                self.system.cache_l2.set_state(addr, 'DS')
                self.system.processors[processorID].lock.release()
                self.read_l1(processorID, addr, val)
            elif stateL2 == 'DI':
                print('Invalid')
                self.system.processors[processorID].lock.acquire()
                val = self.system.memory.get_val(addr)
                self.system.cache_l2.set_value(addr, val, 'DS')
                self.system.processors[processorID].lock.release()
                self.read_l1(processorID, addr, val)
            else:
                print('New value')
                self.system.processors[processorID].lock.acquire()
                val = self.system.memory.get_val(addr)
                self.system.cache_l2.set_value(addr, val, 'DS')
                self.system.processors[processorID].lock.release()
                self.read_l1(processorID, addr, val)
        else:
            self.system.processors[processorID].lock.acquire()
            val = self.system.memory.get_val(addr)
            old_addr, old_val = self.system.cache_l2.set_new_value(addr, val, 'DS')
            # isInCacheL2Old, stateL2Old = self.system.cache_l2.find_address(old_addr)
            # if isInCacheL2Old and stateL2Old == 'DM':
            #     self.system.cache_l2.set_state(old_addr, 'DI')
            #     self.system.memory.set_value(old_addr, old_val)
            if old_addr != -1:
                self.flush_caches(processorID, old_addr)
            self.flush_caches(processorID, old_addr)
            self.system.processors[processorID].lock.release()
            self.read_l1(processorID, addr, val)

    def write_l1(self, processorID, addr, value):
        self.write_bus_flush(processorID, addr)
        isInCacheL1, stateL1 = self.system.processors[processorID].cacheL1.find_address(addr)
        if isInCacheL1:
            self.system.processors[processorID].cacheL1.set_value(addr, value, 'M')
        else:
            old_addr, old_val, old_state = self.system.processors[processorID].cacheL1.set_new_value(addr, value, 'M')
            if old_state == 'M':
                self.system.memory.set_value(old_addr, old_val)
                self.system.cache_l2.set_state(old_addr, 'DI')
        self.system.lock.acquire()
        if self.system.processors[processorID].mode == 0:
            self.system.counter += 1
        self.system.lock.release()
        self.system.processors[processorID].executed = True
        self.set_owners(processorID)
        self.finish(processorID)

    def write_mem(self, processorID, addr):
        for i in range(len(self.system.processors)):
            if self.system.processors[i].get_id() != processorID:
                isInCacheL1, stateL1 = self.system.processors[i].cacheL1.find_address(addr)
                if isInCacheL1 and stateL1 == 'M':
                    val = self.system.cache_l2.get_val(addr)
                    self.system.memory.set_value(addr, val)
                    return

    def write_bus_flush(self, processorID, addr):
        for i in range(len(self.system.processors)):
            if self.system.processors[i].get_id() != processorID:
                isInCacheL1, stateL1 = self.system.processors[i].cacheL1.find_address(addr)
                if isInCacheL1 and (stateL1 == 'S' or stateL1 == 'M'):
                    self.system.processors[i].cacheL1.set_state(addr, 'I')

    def read_l1(self, processorID, addr, value):
        # time.sleep(1)
        self.read_bus_flush(processorID, addr)
        print(f'P{processorID}: direecion: {addr}')
        isInCacheL1, stateL1 = self.system.processors[processorID].cacheL1.find_address(addr)
        if isInCacheL1:
            if stateL1 == 'S':
                self.system.processors[processorID].cacheL1.set_state(addr, 'S')
            elif stateL1 == 'M':
                self.system.processors[processorID].cacheL1.set_state(addr, 'M')
            elif stateL1 == 'I':
                self.system.processors[processorID].cacheL1.set_value(addr, value, 'S')
            else:
                self.system.processors[processorID].cacheL1.set_value(addr, value, 'S')
        else:
            old_addr, old_val, old_state = self.system.processors[processorID].cacheL1.set_new_value(addr, value, 'S')
            if old_state == 'M':
                self.system.memory.set_value(old_addr, old_val)
                self.system.cache_l2.set_state(old_addr, 'DI')

        self.system.lock.acquire()
        if self.system.processors[processorID].mode == 0:
            self.system.counter += 1
        self.system.lock.release()
        self.system.processors[processorID].executed = True
        self.set_owners(processorID)
        self.finish(processorID)

    def read_bus_flush(self, processorID, addr):
        for i in range(len(self.system.processors)):
            if self.system.processors[i].get_id() != processorID:
                isInCacheL1, stateL1 = self.system.processors[i].cacheL1.find_address(addr)
                if isInCacheL1 and stateL1 == 'M':
                    self.system.processors[i].cacheL1.set_state(addr, 'S')

    def flush_caches(self, processorID, addr):
        for i in range(len(self.system.processors)):
            if self.system.processors[i].get_id() != processorID:
                self.system.processors[i].cacheL1.set_state(addr, 'I')

    def set_owners(self, processorID):
        self.system.processors[processorID].lock.acquire()
        for i in range(len(self.system.cache_l2.blocks)):
            self.system.cache_l2.blocks[i].owner_list = []
            for k in range(len(self.system.processors)):
                for j in range(len(self.system.processors[k].cacheL1.blocks)):
                    if self.system.cache_l2.blocks[i].addr == self.system.processors[k].cacheL1.blocks[j].addr and \
                            self.system.processors[k].cacheL1.blocks[j].state != 'I' and\
                            self.system.cache_l2.blocks[i].state != 'DI':
                        self.system.cache_l2.blocks[i].owner_list.append(k)
        self.system.processors[processorID].lock.release()

    def finish(self, processorID):
        print(f'Contador: {self.system.counter}, modo: {self.system.processors[processorID].mode}, '
              f'instr: {self.system.processors[processorID].instruction}')
        self.system.lock.acquire()
        chosen_var = self.system.chosen_cpu
        self.system.lock.release()
        if self.system.run_mode == 'step' \
                and chosen_var == processorID \
                and self.system.processors[processorID].mode == 1:
            print(f'P{processorID}: stooop chosen')
            self.system.resume_stop()
        elif self.system.run_mode == 'step' \
                and self.system.counter == 4 \
                and self.system.processors[processorID].mode == 0:
            print(f'P{processorID}: stooop counter')
            self.system.resume_stop()
        elif self.system.run_mode == 'continuous':
            self.system.processors[processorID].executed = False
        print(f'Processor: {processorID} finished an execution')
        time.sleep(1)
