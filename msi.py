from utils.utils import create_instruction, format_instruction
from models.processor import Processor
import time


class MSI:
    def __init__(self, system):
        self.system = system
        self.current_instruction = ''

    def execute_instruction(self, processorID):
        if self.system.processors[processorID].mode == 0:
            self.system.processors[processorID].executed = False
            self.current_instruction = create_instruction(processorID)
        else:
            if self.system.processors[processorID].instruction:
                if self.system.processors[processorID].instruction[0] == processorID and \
                        self.system.processors[processorID].executed:
                    self.current_instruction = self.system.processors[processorID].instruction
                else:
                    return self.finish(processorID)
            else:
                return self.finish(processorID)
        self.system.processors[processorID].executed = True
        pid, instr_type, addr, val = self.current_instruction
        self.system.processors[processorID].instruction = self.current_instruction
        print(format_instruction(self.current_instruction))
        if instr_type == 'READ':
            self.read_l2(processorID, addr)
        elif instr_type == 'WRITE':
            self.write_l2(processorID, addr, val)
        else:
            print('Estoy ejecutando un CALC')

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
            old_addr = self.system.cache_l2.set_new_value(addr, val, 'DM')
            self.flush_caches(processorID, old_addr)
            self.system.processors[processorID].lock.release()
        self.write_l1(processorID, addr, val)

    def read_l2(self, processorID, addr):
        isInCacheL2, stateL2 = self.system.cache_l2.find_address(addr)
        if isInCacheL2:
            if stateL2 == 'DS':
                print('Share')
                self.read_l1(processorID, addr, 0)
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
            old_addr = self.system.cache_l2.set_new_value(addr, val, 'DS')
            self.flush_caches(processorID, old_addr)
            self.system.processors[processorID].lock.release()
            self.read_l1(processorID, addr, val)

    def write_l1(self, processorID, addr, value):
        self.write_bus_flush(processorID, addr)
        isInCacheL1, stateL1 = self.system.processors[processorID].cacheL1.find_address(addr)
        if isInCacheL1:
            self.system.processors[processorID].cacheL1.set_value(addr, value, 'M')
            # if stateL1 == 'S':
            #     print('Share')
            #     self.system.processors[processorID].cacheL1.set_value(addr, value, 'M')
            # elif stateL1 == 'M':
            #     print('Modify')
            #     self.system.processors[processorID].cacheL1.set_value(addr, value, 'M')
            # elif stateL1 == 'I':
            #     print('Invalid')
            #     self.system.processors[processorID].cacheL1.set_value(addr, value, 'M')
            # else:
            #     print('empty')
            #     self.system.processors[processorID].cacheL1.set_value(addr, value, 'M')
        else:
            self.system.processors[processorID].cacheL1.set_new_value(addr, value, 'M')
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
            self.system.processors[processorID].cacheL1.set_new_value(addr, value, 'S')
        self.finish(processorID)

    def read_bus_flush(self, processorID, addr):
        for i in range(len(self.system.processors)):
            if self.system.processors[i].get_id() != processorID:
                isInCacheL1, stateL1 = self.system.processors[i].cacheL1.find_address(addr)
                if isInCacheL1 and stateL1 == 'M':
                    self.system.processors[i].cacheL1.set_state(addr, 'S')

    def flush_caches(self, processorID, addr):
        for i in range(len(self.system.processors)):
            if self.system.processors[i] != processorID:
                self.system.processors[i].cacheL1.set_state(addr, 'I')

    def finish(self, processorID):
        print(f'Processor: {processorID} finished an execution')
        time.sleep(3)
