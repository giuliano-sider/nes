from memory_mapper import MemoryMapper
from cpu import Cpu
from ppu import Ppu

class Nes():

    def __init__(self, iNES_file):

        self.memory_mapper = MemoryMapper(iNES_file)
        self.cpu = Cpu(self.memory_mapper)
        self.ppu = Ppu(self.memory_mapper)
        self.memory_mapper.set_cpu(self.cpu)
        self.memory_mapper.set_ppu(self.ppu)