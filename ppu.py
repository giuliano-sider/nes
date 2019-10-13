# TODO: Define a way to install dependencies via the Makefile in a way that doesn't break across platforms (use Docker???).
import numpy as np

# Dimensions of the NES screen that we render.
SCREEN_HEIGHT = 240
SCREEN_WIDTH = 256

# Source: NES Documentation (http://nesdev.com/NESDoc.pdf), appendix F.
NES_COLOR_PALETTE_TABLE_OF_RGB_VALUES = [
    (0x75, 0x75, 0x75), # NES color 00
    (0x27, 0x1B, 0x8F), # NES color 01
    (0x00, 0x00, 0xAB), # NES color 02
    (0x47, 0x00, 0x9F), # NES color 03
    (0x8F, 0x00, 0x77), # NES color 04
    (0xAB, 0x00, 0x13), # NES color 05
    (0xA7, 0x00, 0x00), # NES color 06
    (0x7F, 0x0B, 0x00), # NES color 07
    (0x43, 0x2F, 0x00), # NES color 08
    (0x00, 0x47, 0x00), # NES color 09
    (0x00, 0x51, 0x00), # NES color 0A
    (0x00, 0x3F, 0x17), # NES color 0B
    (0x1B, 0x3F, 0x5F), # NES color 0C
    (0x00, 0x00, 0x00), # NES color 0D
    (0x00, 0x00, 0x00), # NES color 0E
    (0x00, 0x00, 0x00), # NES color 0F
    (0xBC, 0xBC, 0xBC), # NES color 10
    (0x00, 0x73, 0xEF), # NES color 11
    (0x23, 0x3B, 0xEF), # NES color 12
    (0x83, 0x00, 0xF3), # NES color 13
    (0xBF, 0x00, 0xBF), # NES color 14
    (0xE7, 0x00, 0x5B), # NES color 15
    (0xDB, 0x2B, 0x00), # NES color 16
    (0xCB, 0x4F, 0x0F), # NES color 17
    (0x8B, 0x73, 0x00), # NES color 18
    (0x00, 0x97, 0x00), # NES color 19
    (0x00, 0xAB, 0x00), # NES color 1A
    (0x00, 0x93, 0x3B), # NES color 1B
    (0x00, 0x83, 0x8B), # NES color 1C
    (0x00, 0x00, 0x00), # NES color 1D
    (0x00, 0x00, 0x00), # NES color 1E
    (0x00, 0x00, 0x00), # NES color 1F
    (0xFF, 0xFF, 0xFF), # NES color 20
    (0x3F, 0xBF, 0xFF), # NES color 21
    (0x5F, 0x97, 0xFF), # NES color 22
    (0xA7, 0x8B, 0xFD), # NES color 23
    (0xF7, 0x7B, 0xFF), # NES color 24
    (0xFF, 0x77, 0xB7), # NES color 25
    (0xFF, 0x77, 0x63), # NES color 26
    (0xFF, 0x9B, 0x3B), # NES color 27
    (0xF3, 0xBF, 0x3F), # NES color 28
    (0x83, 0xD3, 0x13), # NES color 29
    (0x4F, 0xDF, 0x4B), # NES color 2A
    (0x58, 0xF8, 0x98), # NES color 2B
    (0x00, 0xEB, 0xDB), # NES color 2C
    (0x00, 0x00, 0x00), # NES color 2D
    (0x00, 0x00, 0x00), # NES color 2E
    (0x00, 0x00, 0x00), # NES color 2F
    (0xFF, 0xFF, 0xFF), # NES color 30
    (0xAB, 0xE7, 0xFF), # NES color 31
    (0xC7, 0xD7, 0xFF), # NES color 32
    (0xD7, 0xCB, 0xFF), # NES color 33
    (0xFF, 0xC7, 0xFF), # NES color 34
    (0xFF, 0xC7, 0xDB), # NES color 35
    (0xFF, 0xBF, 0xB3), # NES color 36
    (0xFF, 0xDB, 0xAB), # NES color 37
    (0xFF, 0xE7, 0xA3), # NES color 38
    (0xE3, 0xFF, 0xA3), # NES color 39
    (0xAB, 0xF3, 0xBF), # NES color 3A
    (0xB3, 0xFF, 0xCF), # NES color 3B
    (0x9F, 0xFF, 0xF3), # NES color 3C
    (0x00, 0x00, 0x00), # NES color 3D
    (0x00, 0x00, 0x00), # NES color 3E
    (0x00, 0x00, 0x00)  # NES color 3F  
]


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

    def render_background(self):
        """Return an NTSC TV frame with the NES background (pixel values in the NES color palette)
           according to the current PPU settings and contents of PPU memory."""
        frame = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH))

        raise NotImplementedError()

    def render_sprites(self, screen):
        """Render an NTSC TV frame with sprites over a pre-rendered background (pixel values in the NES color palette)
           according to the current PPU settings and contents of PPU memory.
           @param screen : An NTSC TV frame with the NES background painted in."""
        raise NotImplementedError()

    def render(self):
        """Return an NTSC TV frame with background and sprites (with pixel values in the NES color palette)
           according to the current PPU settings and contents of PPU memory."""
        frame = self.render_background()
        frame = self.render_sprites(frame)
        
        raise NotImplementedError()

    @staticmethod
    def nes_color_palette_to_rgb(screen):
        """Return an NTSC TV frame with RGB color values.
           @param screen : An NTSC TV frame with pixel values in the NES color palette."""
        height, width = screen.shape[0], screen.shape[1]
        rgb_screen = np.zeros((height, width, 3))
        for y in range(height):
            for x in range(width):
                rgb_screen[y, x] = NES_COLOR_PALETTE_TABLE_OF_RGB_VALUES[screen[y, x]]
        return rgb_screen
        