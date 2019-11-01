from memory_mapper import MemoryMapper
from cpu import Cpu
from ppu import Ppu, ATTRIBUTE_TABLE_0_ADDRESS
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
        
        nes_image_palette = [0, 0x02, 0x05, 0x0A, 0, 0x07, 0x14, 0x27, 0, 0x29, 0x2C, 0x0D, 0, 0x13, 0x39, 0x1B] # TO BE DELETED
        for i in range(ATTRIBUTE_TABLE_0_ADDRESS, ATTRIBUTE_TABLE_0_ADDRESS + 64):
            self.ppu.memory[i] = 0b11100100
        self.given_image_palette(self.ppu, nes_image_palette) # TO BE DELETED
