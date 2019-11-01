from memory_mapper import MemoryMapper
from cpu import Cpu
from ppu import Ppu
import numpy as np




class Nes():

    def given_pattern_table_in_address(self, ppu, address, tile):
        current_address = address
        for x in range(0, 8):
            bit_string = ""
            for y in range(0, 8):
                bit_string = bit_string + str(tile[x][y])
            content = int(bit_string, 2)
            ppu.memory[current_address] = content
            current_address = current_address + 1

    def given_image_palette(self, ppu, image_palette):
        palette_start_address = 0x3f00
        for i in range(0, 16):
            ppu.memory[palette_start_address + i] = image_palette[i]
        return

    def __init__(self, iNES_file, test_mode=True):
        """Initialize a new Nes instance with the name of an iNES binary file or the binary contents of such a file."""
        self.memory_mapper = MemoryMapper(iNES_file, test_mode)
        self.cpu = Cpu(self.memory_mapper)
        self.ppu = Ppu(self.memory_mapper)
        self.memory_mapper.set_cpu(self.cpu)
        self.memory_mapper.set_ppu(self.ppu)
        nes_image_palette = [0, 0x02, 0x05, 0x0A, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15] # TO BE DELETED
        self.given_image_palette(self.ppu, nes_image_palette) # TO BE DELETED
