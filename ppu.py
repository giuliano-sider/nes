# TODO: Define a way to install dependencies via the Makefile in a way that doesn't break across platforms (use Docker???).
# import numpy as np

SCREEN_HEIGHT = 240
SCREEN_WIDTH = 256

class MemoryAccessor():
    """Allow convenient access to the PPU memory address space."""

    def __init__(self, memory_mapper):
        self.memory_mapper = memory_mapper

    def __getitem__(self, addr):
        return self.memory_mapper.ppu_read_byte(addr)
    def __setitem__(self, addr, value):
        self.memory_mapper.ppu_write_byte(addr, value)

class Ppu():

    def __init__(self, memory_mapper):
        """Instantiate a new PPU linked to the given cartridge memory mapper."""

        self.memory_mapper = memory_mapper
        self.memory = MemoryAccessor(memory_mapper)

        # TODO: Initialize registers, Object Attribute Memory, etc.


    def render(self):
        """Render an NTSC TV frame for display according to the current PPU settings and the contents of PPU memory."""
        # TODO: Render background and sprites.
        
        #return np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH))
        raise NotImplementedError()
        