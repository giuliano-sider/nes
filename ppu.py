# TODO: Define a way to install dependencies via the Makefile in a way that doesn't break across platforms (use Docker???).
import numpy as np
import math

# Dimensions of the NES screen that we render.
SCREEN_HEIGHT = 240
SCREEN_WIDTH = 256

NAME_TABLE_0_ADDRESS = 0x2000
ATTRIBUTE_TABLE_0_ADDRESS = 0x23c0
IMAGE_PALETTE_ADDRESS = 0x3f00

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


class Sprite():

    def __init__(self, x=0, y=0, tile_index=0, palette_index=0, double_sprite=False, horizontal_flip=False, vertical_flip=False, behind_background=False):
        self.x = x
        self.y = y
        self.tile_index = tile_index
        self.palette_index = palette_index
        self.double_sprite = double_sprite
        self.horizontal_flip = horizontal_flip
        self.vertical_flip = vertical_flip
        self.behind_background = behind_background

    @staticmethod
    def from_attribute_bytes(bytes, double_sprite=False):
        """Return a sprite constructed from its 4 attribute bytes: (y-1), tile index, attribute flags, (x-1),
           or a double sprite (8x16) from 8 attribute bytes."""
        assert len(bytes) == 4 and double_sprite is False or len(bytes) == 8 and double_sprite is True

        raise NotImplementedError()

    def to_attribute_bytes(self):
        """Return a bytearray of 4 or 8 bytes constructed from the given sprite."""

        raise NotImplementedError()




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
        # FOR EACH TILE IN THE NAME TABLE 0

        for i in range(0, 0 + 960):
            tile_index = self.memory[i]
            palette_group_index = self.get_palette_group_index_from_name_table_index(NAME_TABLE_0_ADDRESS + i)
            tile_pattern = self.get_tile_from_index(tile_index, palette_group_index)
            row = int(i/32)
            column = i % 32
            for r in range(0, 8):
                for c in range(0, 8):
                    frame[row + r][column + c] = tile_pattern[r][c]
        return frame

    def get_palette_group_index_from_name_table_index(self, index):
        return 0

    @staticmethod
    def get_attribute_set_index_from_name_table_index(index):
        attribute_struct_size_x = 8
        quad_x = math.floor((index % 32)/4)
        quad_y = math.floor(index/128)
        return attribute_struct_size_x * quad_y + quad_x

    def get_palette_set_index(self, attribute_set_index, name_table_index):
        square_x = math.floor((name_table_index % 4)/2)
        square_y = math.floor(name_table_index/64)
        attr_internal_index = 2 * square_y + square_x
        attr_byte = self.memory[ATTRIBUTE_TABLE_0_ADDRESS + attribute_set_index]
        mask_0 = 0b00000011
        mask_1 = 0b00001100
        mask_2 = 0b00110000
        mask_3 = 0b11000000
        parsed_attr_byte = [
            attr_byte & mask_0,
            (attr_byte & mask_1) >> 2,
            (attr_byte & mask_2) >> 4,
            (attr_byte & mask_3) >> 6
        ]
        return parsed_attr_byte[attr_internal_index]

    def get_tile_from_index(self, tile_index, palette_group_index):
        tile_size_in_pattern_memory_in_bytes = 16
        tile_pixel_number = 64
        tile = np.zeros((8, 8))
        for pixel in range(0, tile_pixel_number):
            tile_address = tile_index * tile_size_in_pattern_memory_in_bytes
            palette_color_index = self.get_palette_color_index_for_tile_pixel(tile_address)
            nes_pixel_color = self.get_nes_color_from_palette(palette_group_index, palette_color_index)
            # rgb_pixel_color = NES_COLOR_PALETTE_TABLE_OF_RGB_VALUES[nes_pixel_color]
            i = int(pixel / 8)
            j = pixel % 8
            tile[i][j] = nes_pixel_color
        return tile

    def get_palette_color_index_for_tile_pixel(self, address):
        in_tile_offset = 8
        hi_bit_number = self.memory[address + in_tile_offset]
        lo_bit_number = self.memory[address]
        return hi_bit_number * 2 + lo_bit_number

    def get_nes_color_from_palette(self, group_index, color_index):
        palette_size = 4
        return self.memory[IMAGE_PALETTE_ADDRESS + group_index * palette_size + color_index]

    def render_sprites(self, screen):
        """Render an NTSC TV frame with sprites over a pre-rendered background (pixel values in the NES color palette)
           according to the current PPU settings and contents of PPU memory.
           @param screen : An NTSC TV frame with the NES background painted in."""
        raise NotImplementedError()
    
    def fakeRender(self):
        x = np.arange(0, 300)
        y = np.arange(0, 300)
        X, Y = np.meshgrid(x, y)
        Z = X + Y
        Z = 255*Z/Z.max()
        return Z

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
        