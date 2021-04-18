from models.processor import Processor
from models.cacheL2 import CacheL2
from models.memory import Memory


class System:
    def __init__(self, processors: list[Processor], cacheL2: CacheL2, memory: Memory):
        self.processors = processors
        self.cacheL2 = cacheL2
        self.memory = memory
