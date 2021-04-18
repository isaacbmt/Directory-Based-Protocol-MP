from models.system import System
from utils.utils import create_instruction
from models.processor import Processor
import time


class MSI:
    def __init__(self, system: System):
        self.system = system
        self.current_instruction = ''

    def executeInstruction(self, processorID):
        self.current_instruction = create_instruction(processorID)
        pid, instr_type, addr, val = self.current_instruction

        if instr_type == 'READ':
            isInCacheL2, stateL2 = self.system.cacheL2.find_address(addr)
            if isInCacheL2:
                if stateL2 == 'DS':
                    print('Share')
                    self.read(processorID, addr, 0)
                elif stateL2 == 'DM':
                    print('Modify')
                    val = self.system.cacheL2.get_val(addr)
                    self.system.memory.set_value(addr, val)
                    self.system.cacheL2.set_state(addr, 'DS')
                    self.read(processorID, addr, val)
                elif stateL2 == 'DI':
                    print('Invalid')
                    val = self.system.memory.get_val(addr)
                    self.system.cacheL2.set_value(addr, val, 'DS')
                    self.read(processorID, addr, val)
                else:
                    print('New value')
                    val = self.system.memory.get_val(addr)
                    self.system.cacheL2.set_value(addr, val, 'DS')

        elif instr_type == 'WRITE':
            isInCacheL2, stateL2 = self.system.cacheL2.find_address(addr)
            if isInCacheL2:
                if stateL2 == 'DS':
                    print('ds')
                    self.system.cacheL2.set_value(addr, val, 'DM')
                elif stateL2 == 'DM':
                    print('dm')
                    self.system.cacheL2.set_state(addr, 'DM')
                elif stateL2 == 'DI':
                    print('di')
                    self.system.cacheL2.set_value(addr, val, 'DM')
                else:
                    print('else')
                    self.system.cacheL2.set_value(addr, val, 'DM')

    def write(self, processorID, addr, value):
        self.write_bus_flush(processorID, addr)
        isInCacheL1, stateL1 = self.system.processors[processorID].cacheL1.find_address(addr)
        if isInCacheL1:
            if stateL1 == 'S':
                print('Share')
                self.system.processors[processorID].cacheL1.set_value(addr, value, 'M')
            elif stateL1 == 'M':
                print('Modify')
                self.system.processors[processorID].cacheL1.set_value(addr, value, 'M')
            elif stateL1 == 'I':
                print('Invalid')
                self.system.processors[processorID].cacheL1.set_value(addr, value, 'M')
            else:
                print('empty')
                self.system.processors[processorID].cacheL1.set_value(addr, value, 'M')

    def write_bus_flush(self, processorID, addr):
        for i in range(len(self.system.processors)):
            if self.system.processors[i].get_id() != processorID:
                isInCacheL1, stateL1 = self.system.processors[i].cacheL1.find_address(addr)
                if isInCacheL1 and stateL1 == 'S':
                    self.system.processors[i].cacheL1.set_state(addr, 'I')

    def read(self, processorID, addr, value):
        # time.sleep(1)
        self.read_bus_flush(processorID, addr)
        isInCacheL1, stateL1 = self.system.processors[processorID].cacheL1.find_address(addr)
        if isInCacheL1:
            if stateL1 == 'S':
                print('queda igual')
                self.system.processors[processorID].cacheL1.set_state(addr, 'S')
            elif stateL1 == 'M':
                self.system.processors[processorID].cacheL1.set_state(addr, 'M')
            elif stateL1 == 'I':
                self.system.processors[processorID].cacheL1.set_value(addr, value, 'S')
            else:
                self.system.processors[processorID].cacheL1.set_value(addr, value, 'S')

    def read_bus_flush(self, processorID, addr):
        for i in range(len(self.system.processors)):
            if self.system.processors[i].get_id() != processorID:
                isInCacheL1, stateL1 = self.system.processors[i].cacheL1.find_address(addr)
                if isInCacheL1 and stateL1 == 'M':
                    self.system.processors[i].cacheL1.set_state(addr, 'S')
