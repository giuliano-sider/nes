# TODO: Define a way to install dependencies via the Makefile in a way that doesn't break across platforms (use Docker???).
import os
# Added in an experiment to limit the number of threads started by NumPy.
# os.environ["MKL_NUM_THREADS"] = "1" 
# os.environ["NUMEXPR_NUM_THREADS"] = "1" 
# os.environ["OMP_NUM_THREADS"] = "1" 
import numpy as np

import math
from enum import Enum
import sys

from memory_mapper cimport MemoryMapper, OAMDMA, MEMORY_SIZE, is_palette_addr
from cpu import Cpu

# Dimensions of the NES screen that we render.
SCREEN_HEIGHT = 240
SCREEN_WIDTH = 256


# Source: NES Documentation (http://nesdev.com/NESDoc.pdf), appendix F.
NES_COLOR_PALETTE_TABLE_OF_RGB_VALUES = np.array([
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
])

class NesColors(Enum):
    gray = 0x00

def is_transparent_pixel(ppu_palette_index):
    return ppu_palette_index % 4 == 0
is_transparent_pixel = np.vectorize(is_transparent_pixel)

def print_sprites(sprite_buffer, file=sys.stdout):
    for i in range(NUM_SPRITES_IN_OAM):
        y = sprite_buffer[BYTES_PER_SPRITE*i + SPRITE_Y_OFFSET] + 1
        x = sprite_buffer[BYTES_PER_SPRITE*i + SPRITE_X_OFFSET] + 1
        pattern_tile_index = sprite_buffer[BYTES_PER_SPRITE*i + SPRITE_TILE_INDEX_OFFSET]
        attributes = sprite_buffer[BYTES_PER_SPRITE*i + SPRITE_ATTRIBUTE_OFFSET]
        print('sprite {0:d}: x = {1:d}, y = {2:d}, tile index = {3:#02x}, attributes = {4:08b}'.format(i, x, y, pattern_tile_index, attributes))


cdef class MemoryAccessor():
    """Allow convenient access to the PPU memory address space."""

    def __init__(self, memory_mapper):
        self.memory_mapper = memory_mapper

    def __getitem__(self, int addr):
        return self.memory_mapper.ppu_read_byte(addr)
    def __setitem__(self, int addr, int value):
        self.memory_mapper.ppu_write_byte(addr, value)

cdef class Ppu():

    def get_pattern_tables_as_numpy_array(self):
        """Return a (2, 8, 256*8) array with the 2 pattern tables stored in PPU memory stacked along axis 0.
           Each pattern table has its 256 tiles stacked horizontallly."""
        pattern_tables = np.zeros((2, TILE_SIZE, NUM_TILES_IN_PATTERN_TABLE*TILE_SIZE), np.int32)
        for i in range(NUM_TILES_IN_PATTERN_TABLE):
            for y in range(TILE_SIZE):
                for x in range(TILE_SIZE):
                    pattern_tables[0, y, i*TILE_SIZE + x] = self.get_pixel_pattern(0, i, y, x)
                    pattern_tables[1, y, i*TILE_SIZE + x] = self.get_pixel_pattern(1, i, y, x)
        return pattern_tables

    def __init__(self, memory_mapper):
        """Instantiate a new PPU linked to the given cartridge memory mapper."""

        self.memory_mapper = memory_mapper
        self.memory = MemoryAccessor(memory_mapper)

        self.pattern_tables = self.get_pattern_tables_as_numpy_array()

        # TODO: Initialize registers, Object Attribute Memory, etc.
        self.oam = bytearray(NUM_BYTES_IN_OAM)

        self.ppu_dynamic_latch = 0

        self.ppuctrl = 0
        self.ppumask = 0

        self.ppustatus = 0

        self.vblank = False

        self.oamaddr = 0

        self.ppu_address_hi_lo_latch = ADDRESS_LATCH_HI

        self.scroll_x_position = 0
        self.scroll_y_position = 0

        self.ppuaddr = 0

        self.ppudata_read_buffer = 0

        self.register_writers_ = {
            PPUCTRL: self.write_ppuctrl,
            PPUMASK: self.write_ppumask,
            PPUSTATUS: self.write_ppustatus,
            OAMADDR: self.write_oamaddr,
            OAMDATA: self.write_oamdata,
            PPUSCROLL: self.write_ppuscroll,
            PPUADDR: self.write_ppuaddr,
            PPUDATA: self.write_ppudata,
            OAMDMA: self.write_oamdma
        }
        self.register_readers_ = {
            PPUCTRL: self.read_ppuctrl,
            PPUMASK: self.read_ppumask,
            PPUSTATUS: self.read_ppustatus,
            OAMADDR: self.read_oamaddr,
            OAMDATA: self.read_oamdata,
            PPUSCROLL: self.read_ppuscroll,
            PPUADDR: self.read_ppuaddr,
            PPUDATA: self.read_ppudata,
            OAMDMA: self.read_oamdma
        }

    def write_ppuctrl(self, value):
        # TODO: generate vblank NMI if PPU is in vblank, PPUSTATUS.vblank is 1, and PPUCTRL.enable_nmi is being set from 0 to 1 (probably not applicable to our emulator anyway).
        value %= 256
        self.ppuctrl = value
        self.ppu_dynamic_latch = value
        print('write_ppuctrl set PPUCTRL to {0:08b}'.format(value))

    def write_ppumask(self, value):
        value %= 256
        self.ppumask = value
        self.ppu_dynamic_latch = value
        print('write_ppumask set PPUMASK to {0:08b}'.format(value))

    def write_ppustatus(self, value):
        value %= 256
        # read-only
        self.ppu_dynamic_latch = value

    def set_vblank_flag(self):
        self.ppustatus |= VBLANK_FLAG

    def clear_vblank_flag(self):
        self.ppustatus &= ~VBLANK_FLAG

    def in_vblank(self):
        return self.vblank

    def write_oamaddr(self, value):
        value %= 256
        self.oamaddr = value
        self.ppu_dynamic_latch = value
        print('write_oamaddr set OAMADDR to %s' % hex(value))

    def write_oamdata(self, value):
        value %= 256
        self.oam[self.oamaddr] = value
        print('write_oamdata set OAMDATA to %s' % hex(value))
        self.oamaddr = (self.oamaddr + 1) % NUM_BYTES_IN_OAM
        self.ppu_dynamic_latch = value

    def write_ppuscroll(self, value):
        # TODO: implement scrolling behaviors.
        value %= 256
        if self.ppu_address_hi_lo_latch == ADDRESS_LATCH_HI:
            self.scroll_x_position = value
            self.ppu_address_hi_lo_latch = ADDRESS_LATCH_LO
        else:
            self.scroll_y_position = value
            self.ppu_address_hi_lo_latch = ADDRESS_LATCH_HI
        self.ppu_dynamic_latch = value
        print('write_ppuscroll set PPUSCROLL to %s' % hex(value))

    def write_ppuaddr(self, value):
        value %= 256
        if self.ppu_address_hi_lo_latch == ADDRESS_LATCH_HI:
            self.ppuaddr = value << 8
            self.ppu_address_hi_lo_latch = ADDRESS_LATCH_LO
        else:
            self.ppuaddr |= value
            self.ppu_address_hi_lo_latch = ADDRESS_LATCH_HI
        self.ppu_dynamic_latch = value
        print('write_ppuaddr set PPUADDR to %s' % hex(value))

    def write_ppudata(self, value):
        value %= 256
        self.memory[self.ppuaddr] = value
        print('write_ppudata wrote value %s to address %s in PPU address space' % (hex(value), hex(self.ppuaddr)))
        if self.use_ppuaddr_increment_of_32() is True:
            self.ppuaddr = (self.ppuaddr + 32) % MEMORY_SIZE
        else:
            self.ppuaddr = (self.ppuaddr + 1) % MEMORY_SIZE
        self.ppu_dynamic_latch = value

    def write_oamdma(self, value):
        value %= 256
        for i in range(NUM_BYTES_IN_OAM):
            self.oam[i] = self.memory_mapper.cpu_read_byte((value << 8) + i)
        # assert self.memory_mapper.cpu_memory_[(value << 8) : ((value + 1) << 8)] == self.oam
        print('write_oamdma transferred the following sprites to sprite memory:\n')
        print_sprites(self.oam)
        self.memory_mapper.cpu().tick_clock(513)
        self.ppu_dynamic_latch = value

    def read_ppuctrl(self):
        return self.ppu_dynamic_latch # write-only
    def read_ppumask(self):
        return self.ppu_dynamic_latch # write-only
    def read_ppustatus(self):
        status_content = ((self.ppustatus & (VBLANK_FLAG | SPRITE_0_HIT | SPRITE_OVERFLOW)) | 
                          (self.ppu_dynamic_latch & PPUSTATUS_BLANK_BITS))
        self.clear_vblank_flag()
        print('read_ppustatus obtained value {0:08b}'.format(status_content))
        self.ppu_address_hi_lo_latch = ADDRESS_LATCH_HI # Resets PPU hi/lo address latch.
        self.ppu_dynamic_latch = status_content
        return status_content

    def read_oamaddr(self):
        return self.ppu_dynamic_latch # write-only
    def read_oamdata(self):
        oamvalue = self.oam[self.oamaddr]
        if not self.in_vblank() and not self.in_forced_blanking():
            self.oamaddr = (self.oamaddr + 1) % NUM_BYTES_IN_OAM
        self.ppu_dynamic_latch = oamvalue
        return oamvalue

    def read_ppuscroll(self):
        return self.ppu_dynamic_latch # write-only
    def read_ppuaddr(self):
        return self.ppu_dynamic_latch # write-only
    def read_ppudata(self):
        data = self.memory[self.ppuaddr]
        self.ppu_dynamic_latch = data # TODO: find justification for this.
        if is_palette_addr(self.ppuaddr):
            # The NES dev wiki at http://wiki.nesdev.com/w/index.php/PPU_registers
            # doesn't explain this behavior well. But it becomes clearer from this post at
            # https://forums.nesdev.com/viewtopic.php?f=3&t=18627
            self.ppudata_read_buffer = self.memory[self.memory_mapper.ppu_unmirrored_address(self.ppuaddr) - 0x1000]
            retval = data
        else:
            retval = self.ppudata_read_buffer
            self.ppudata_read_buffer = data
        if self.use_ppuaddr_increment_of_32() is True:
            self.ppuaddr = (self.ppuaddr + 32) % MEMORY_SIZE
        else:
            self.ppuaddr = (self.ppuaddr + 1) % MEMORY_SIZE
        return retval
    def read_oamdma(self):
        return self.ppu_dynamic_latch # write-only

    def write_register(self, register, value):
        self.register_writers_[register](value)

    def read_register(self, register):
        return self.register_readers_[register]()

    def render_background_alt(self):
        """Return an NTSC TV frame with the NES background (pixel values in the NES color palette)
           according to the current PPU settings and contents of PPU memory."""
        cdef int tile_row, tile_col, tile_index, pattern_tile_index, palette_group_index
        frame = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH), dtype=np.int32)
        palette = self.get_ppu_palette_as_lookup_table()

        # TODO: Allow other name tables and attribute tables to be used as well.
        # FOR EACH TILE IN THE NAME TABLE 0 (30 tile rows and 32 tile columns)
        for tile_row in range(30):
            for tile_col in range(32):
                tile_index = TILES_PER_ROW*tile_row + tile_col
                pattern_tile_index = self.memory[NAME_TABLE_0_ADDRESS + tile_index]
                tile = self.get_pattern_tile(self.background_pattern_table(), pattern_tile_index)
                palette_group_index = self.get_background_palette(ATTRIBUTE_TABLE_0_ADDRESS, tile_index)
                tile = tile + (palette_group_index << 2)
                tile = self.apply_palette(tile, palette)
                # tile = self.get_tile_by_name_table_index(tile_index)
                frame[TILE_SIZE*tile_row : TILE_SIZE*(tile_row + 1), TILE_SIZE*tile_col : TILE_SIZE*(tile_col + 1)] = tile

        return frame

    def get_pattern_tile(self, pattern_table, tile_index):
        """Return an array with the 2-bit pattern values for a particular tile of one of
           the pattern tables.
           @param pattern_table : 0 for the "left" or 1 for the "right" pattern table
           @param tile_idx : Index of a tile within a pattern table."""
        return self.pattern_tables[pattern_table, :, TILE_SIZE * tile_index : TILE_SIZE * (tile_index + 1)]
        # tile = np.zeros((TILE_SIZE, TILE_SIZE), dtype=np.int32)
        # for y in range(TILE_SIZE):
        #     for x in range(TILE_SIZE):
        #         tile[y, x] = self.get_pixel_pattern(pattern_table, tile_index, y, x)
        # return tile

    def get_background_palette(self, attribute_table_base_addr, tile_index):
        """Obtain the background palette index from the attribute tables for a given tile.
           @param attribute_table_base_addr : Base address of the attribute table where the palette bits are located.
           @param tile_index : Index of a tile within a nametable."""
        tile_row = tile_index // TILES_PER_ROW
        tile_col = tile_index % TILES_PER_ROW
        tile_group_row = tile_row // 4
        tile_group_col = tile_col // 4
        tile_group_index = tile_group_row*8 + tile_group_col
        # Map (tile_row % 4, tile_col % 4) to shift amount within the tile group bitmap in the attribute table:
        shift = {
            (0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 0,
            (0, 2): 2, (0, 3): 2, (1, 2): 2, (1, 3): 2,
            (2, 0): 4, (2, 1): 4, (3, 0): 4, (3, 1): 4,
            (2, 2): 6, (2, 3): 6, (3, 2): 6, (3, 3): 6,
        }
        bitmap_shift_amount = shift[(tile_row % 4, tile_col % 4)]
        palette_bits_selector = 0b11 << bitmap_shift_amount
        return (self.memory[attribute_table_base_addr + tile_group_index] & palette_bits_selector) >> bitmap_shift_amount


    def render_background(self):
        """Return an NTSC TV frame with the NES background (pixel values in the NES color palette)
           according to the current PPU settings and contents of PPU memory."""
        frame = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH), dtype=np.int32)
        # FOR EACH TILE IN THE NAME TABLE 0
        return frame

    def get_tile_by_name_table_index(self, index):
        attr_index = self.get_attribute_set_index_from_name_table_index(index)
        palette_set_index = self.get_palette_set_index(attr_index, index)
        tile_pattern = self.get_tile_pattern_from_name_table_index(index)
        nes_tile = self.convert_tile_pattern_into_nes_color(tile_pattern, palette_set_index)
        return nes_tile

    @staticmethod
    def get_attribute_set_index_from_name_table_index(index):
        attribute_struct_size_x = 8
        quad_x = math.floor((index % 32)/4)
        quad_y = math.floor(index/128)
        return attribute_struct_size_x * quad_y + quad_x

    def get_palette_set_index(self, attribute_set_index, name_table_index):
        square_x = math.floor((name_table_index % 4)/2)
        square_y = math.floor(name_table_index/64) % 2
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

    @staticmethod
    def convert_nes_color_to_rgb(nes_color):
        return NES_COLOR_PALETTE_TABLE_OF_RGB_VALUES[nes_color]

    def convert_nes_tile_pattern_to_rgb(self, tile, pattern_set):
        rgb_tile = np.zeros((8, 8, 3))
        for i in range(0, 8):
            for j in range(0, 8):
                nes_color = self.get_nes_color_from_palette(pattern_set, tile[i][j])
                rgb_color = self.convert_nes_color_to_rgb(nes_color)
                rgb_tile[i][j][0] = rgb_color[0]
                rgb_tile[i][j][1] = rgb_color[1]
                rgb_tile[i][j][2] = rgb_color[2]
        return rgb_tile

    def convert_tile_pattern_into_nes_color(self, tile, pattern_set):
        nes_tile = np.zeros((8, 8))
        for i in range(0, 8):
            for j in range(0, 8):
                nes_tile[i][j] = self.get_nes_color_from_palette(pattern_set, tile[i][j])
        return nes_tile



    def get_tile_pattern_from_name_table_index(self, name_table_index):
        tile = np.zeros((8, 8))
        tile_lo_address = PALETTE_PATTERN_0 + name_table_index * 16
        tile_hi_address = tile_lo_address + 8
        masks = [0b00000001, 0b00000010, 0b00000100, 0b00001000, 0b00010000, 0b00100000, 0b01000000, 0b10000000]
        for x in range(0, 8):
            content_lo = self.memory[tile_lo_address + x]
            content_hi = self.memory[tile_hi_address + x]
            string_bit = ""
            for y in range(0, 8):

                bit_lo = int((content_lo & masks[y]) >> y)
                string_bit = string_bit + str(bit_lo)
                bit_hi = int((content_hi & masks[y]) >> y)
                tile[x][7 - y] = int(2 * bit_hi + bit_lo)
        return tile.astype(int)




    def get_sprite_tile(self, sprite_idx):
        """Return an 8x8 or 8x16 tile with a rendering of a sprite. Colors are expressed in the PPU palette.
           Sprites that are partly off screen get clipped.
           Return none for sprites that are entirely off screen."""
        if self.using_8x16_sprites() is False:
            tile = self.get_pattern_tile(self.sprite_pattern_table(), self.get_sprite_tile_idx(sprite_idx))
            tile = (1 << 4) + (self.get_sprite_palette_attribute(sprite_idx) << 2) + tile
        else:
            sprite_pattern_table = self.get_sprite_tile_idx(sprite_idx) & 0x1
            sprite_tile_idx = self.get_sprite_tile_idx(sprite_idx) & 0xFE

            top_tile = self.get_pattern_tile(sprite_pattern_table, sprite_tile_idx)
            bottom_tile = self.get_pattern_tile(sprite_pattern_table, sprite_tile_idx + 1)
            tile = ((1 << 4) +
                    (self.get_sprite_palette_attribute(sprite_idx) << 2) +
                    np.concatenate((top_tile, bottom_tile), axis=0))

        if self.is_sprite_flipped_vertically(sprite_idx):
            tile = np.flip(tile, axis=0)
        if self.is_sprite_flipped_horizontally(sprite_idx):
            tile = np.flip(tile, axis=1)

        # Return sprite tile clipped to the viewing area.
        x_lo, x_hi, y_lo, y_hi = self.get_sprite_bounding_box(sprite_idx)
        if x_lo >= x_hi or y_lo >= y_hi:
            return None
        else:
            return tile[0 : y_hi - y_lo, 0 : x_hi - x_lo]


    def apply_ppu_palette(self, img):
        """Take an image with colors in the PPU palette and use the palettes
           to change the img in place to convert it to colors in the NES system palette.
           @param img : A 2D image with colors which are indices in the PPU palette.
           @return : The same 2D image changed in place to have colors in the NES system palette.
        """
        height, width = img.shape[0], img.shape[1]
        for y in range(height):
            for x in range(width):
                img[y, x] = self.memory[PALETTE_BASE_ADDR + img[y, x]]
        return img

    def apply_palette(self, img, palette):
        return palette[img]
        # height, width = img.shape[0], img.shape[1]
        # output_img = np.zeros((height, width), dtype=np.int32)
        # for y in range(height):
        #     for x in range(width):
        #         output_img[y, x] = palette[img[y, x]]
        # return output_img

    def get_ppu_palette_as_lookup_table(self):
        palette = np.zeros((PPU_PALETTE_SIZE,), dtype=np.int32)
        for i in range(0, PPU_PALETTE_SIZE):
            palette[i] = self.memory[PALETTE_BASE_ADDR + i]
        return palette

    def use_ppuaddr_increment_of_32(self):
        """Return true if and only if the PPUCTRL flag for autoincrement of PPUADDR by 32 is set (else PPUADDR uses an autoincrement of 1)."""
        return bool(self.ppuctrl & PPUADDR_AUTOINCREMENT_OF_32)

    def nmi_enabled(self):
        """Return true if and only if the PPUCTRL NMI enabled flag is set."""
        return bool(self.ppuctrl & NMI_ENABLED)

    def using_8x16_sprites(self):
        """Return true if and only if the PPUCTRL 8x16 sprite flag is on."""
        return bool(self.ppuctrl & EXTRA_LARGE_SPRITE)

    def begin_vblank(self):
        """Begin vblank period."""
        self.vblank = True
        self.set_vblank_flag()
        if self.nmi_enabled():
            self.memory_mapper.cpu().trigger_NMI('start of vblank')

    def end_vblank(self):
        """Finish vblank period."""
        self.vblank = False
        self.clear_vblank_flag()

    def in_forced_blanking(self):
        """Return whether the PPU is in forced blanking mode."""
        return True if not self.sprite_rendering_enabled() and not self.background_rendering_enabled() else False

    def sprite_rendering_enabled(self):
        """Return true if and only if the PPUMASK sprite rendering flag is on."""
        return bool(self.ppumask & SHOW_SPRITES)

    def background_rendering_enabled(self):
        """Return true if and only if the PPUMASK background rendering flag in on."""
        return bool(self.ppumask & SHOW_BACKGROUND)

    def grayscale_flag(self):
        """Return true if and only if the PPUMASK grayscale flag is on."""
        return bool(self.ppumask & SHOW_GRAYSCALE)

    def sprite_pattern_table(self):
        """Return the value of the sprite pattern table selector from PPUCTRL."""
        return int(bool(self.ppuctrl & SPRITE_PATTERN_TABLE_SELECTOR))

    def background_pattern_table(self):
        """Return the value of the sprite pattern table selector from PPUCTRL."""
        return int(bool(self.ppuctrl & BACKGROUND_PATTERN_TABLE_SELECTOR))

    def is_sprite_flipped_vertically(self, sprite_idx):
        """Return true if and only the given sprite has its vertical_flip flag set to 1."""
        return bool(self.oam[BYTES_PER_SPRITE*sprite_idx + SPRITE_ATTRIBUTE_OFFSET] & SPRITE_FLIPPED_VERTICALLY)

    def is_sprite_flipped_horizontally(self, sprite_idx):
        """Return true if and only the given sprite has its horizontal_flip flag set to 1."""
        return bool(self.oam[BYTES_PER_SPRITE*sprite_idx + SPRITE_ATTRIBUTE_OFFSET] & SPRITE_FLIPPED_HORIZONTALLY)

    def is_sprite_behind_background(self, sprite_idx):
        """Return true if and only the given sprite has its behind_background flag set to 1."""
        return bool(self.oam[BYTES_PER_SPRITE*sprite_idx + SPRITE_ATTRIBUTE_OFFSET] & SPRITE_BEHIND_BACKGROUND)

    def get_sprite_x(self, sprite_idx):
        """Return the x coordinate of the given sprite."""
        return self.oam[BYTES_PER_SPRITE*sprite_idx + SPRITE_X_OFFSET] + 1

    def get_sprite_y(self, sprite_idx):
        """Return the y coordinate of the given sprite."""
        return self.oam[BYTES_PER_SPRITE*sprite_idx + SPRITE_Y_OFFSET] + 1

    def get_sprite_tile_idx(self, sprite_idx):
        """Return the tile index value stored in the sprite attribute memory
           for the given sprite. This includes the lowest order bit in the case
           of 8x16 sprites."""
        return self.oam[BYTES_PER_SPRITE*sprite_idx + SPRITE_TILE_INDEX_OFFSET]

    def get_sprite_palette_attribute(self, sprite_idx):
        """Return the index of the palette selected for the given sprite."""
        return self.oam[BYTES_PER_SPRITE*sprite_idx + SPRITE_ATTRIBUTE_OFFSET] & 0b11

    def get_sprite_bounding_box(self, sprite_idx):
        """Return a bounding box of the form (x_lo, x_hi, y_lo, y_hi) for the given sprite.
           The values of x_hi and y_hi are clipped to the visible region of the screen."""
        x_lo = self.get_sprite_x(sprite_idx)
        x_hi = x_lo + (8 if self.using_8x16_sprites() is False else 16)
        y_lo = self.get_sprite_y(sprite_idx)
        y_hi = y_lo + (8 if self.using_8x16_sprites() is False else 16)

        return x_lo, min(x_hi, MAX_VISIBLE_X + 1), y_lo, min(y_hi, MAX_VISIBLE_Y + 1)

    def get_pixel_pattern(self, pattern_table, tile_idx, tile_y, tile_x):
        """Return the 2-bit pattern value for a particular pixel in a tile of one of
           the pattern tables.
           @param pattern_table : 0 for the "left" or 1 for the "right" pattern table
           @param tile_idx : Index of a tile within a pattern table.
           @param tile_y : y coordinate of the pixel within the tile
           @param tile_x : x coordinate of the pixel within the tile"""
        bit_0_addr = PATTERN_TABLE_BASE_ADDR + PATTERN_TABLE_SIZE*pattern_table + PATTERN_TABLE_BYTES_PER_TILE*tile_idx + tile_y
        bit_1_addr = PATTERN_TABLE_BASE_ADDR + PATTERN_TABLE_SIZE*pattern_table + PATTERN_TABLE_BYTES_PER_TILE*tile_idx + PATTERN_TABLE_BYTES_PER_BITPLANE + tile_y
        bit_0 = int(bool(self.memory[bit_0_addr] & (1 << (7 - tile_x))))
        bit_1 = int(bool(self.memory[bit_1_addr] & (1 << (7 - tile_x))))
        return bit_0 + (bit_1 << 1)

    def render_sprites(self, background):
        """Render an NTSC TV frame with sprites over a pre-rendered background (pixel values in the NES system palette)
           according to the current PPU settings and contents of PPU memory.
           @param background : An NTSC TV frame with the NES background painted in."""
        # TODO: Add max 8 sprites per scanline limitation?
        palette = self.get_ppu_palette_as_lookup_table()
        screen = background.copy()
        for i in reversed(range(0, NUM_SPRITES_IN_OAM)):
            sprite_img = self.get_sprite_tile(i)
            if sprite_img is None:
                continue
            x_lo, x_hi, y_lo, y_hi = self.get_sprite_bounding_box(i)
            if self.is_sprite_behind_background(i):
                screen[y_lo : y_hi, x_lo : x_hi] = background[y_lo : y_hi, x_lo : x_hi]
            else:
                screen[y_lo : y_hi, x_lo : x_hi] = np.where(
                    sprite_img % 4 == 0, # is_transparent_pixel(sprite_img), 
                    screen[y_lo : y_hi, x_lo : x_hi],
                    self.apply_palette(sprite_img, palette))

        return screen

    def fakeRender(self):
        x = np.arange(0, 300)
        y = np.arange(0, 300)
        X, Y = np.meshgrid(x, y)
        Z = X + Y
        Z = 255*Z/Z.max()
        return Z

    @staticmethod
    def nes_color_palette_to_rgb(screen, convert_to_grayscale=False):
        """Return an NTSC TV frame with RGB color values.
           @param screen : An NTSC TV frame with pixel values in the NES system palette."""
        # height, width = screen.shape[0], screen.shape[1]
        # rgb_screen = np.zeros((height, width, 3), dtype=np.int32)
        if convert_to_grayscale is True:
            screen = screen & GRAY_COLUMN
        return NES_COLOR_PALETTE_TABLE_OF_RGB_VALUES[screen]
        # for y in range(height):
        #     for x in range(width):
        #         rgb_screen[y, x] = NES_COLOR_PALETTE_TABLE_OF_RGB_VALUES[screen[y, x]]
        # return rgb_screen

    def render(self):
        """Return an NTSC TV frame with background and sprites (with pixel values in the NES color palette)
           according to the current PPU settings and contents of PPU memory."""
        frame = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH), dtype=np.int32)
        if self.background_rendering_enabled():
            frame = self.render_background_alt()
        if self.sprite_rendering_enabled():
            frame = self.render_sprites(frame)

        return self.nes_color_palette_to_rgb(frame, self.grayscale_flag())

