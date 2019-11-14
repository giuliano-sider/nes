from memory_mapper cimport MemoryMapper


cdef enum:
    # Tile constants
    TILE_SIZE = 8
    TILES_PER_ROW = 32

    NAME_TABLE_0_ADDRESS = 0x2000
    ATTRIBUTE_TABLE_0_ADDRESS = 0x23c0
    IMAGE_PALETTE_ADDRESS = 0x3f00

    PALETTE_PATTERN_0 = 0x0000

    # Pattern table constants.
    PATTERN_TABLE_BASE_ADDR = 0x0000
    PATTERN_TABLE_SIZE = 0x1000
    PATTERN_TABLE_BYTES_PER_TILE = 16
    PATTERN_TABLE_BYTES_PER_BITPLANE = 8
    NUM_TILES_IN_PATTERN_TABLE = 256

    # Palette constants.
    PALETTE_BASE_ADDR = 0x3F00
    SPRITE_PALETTE_BASE_ADDR = 0x3F10
    SPRITE_PALETTE_0 = 0x3F10
    SPRITE_PALETTE_1 = 0x3F14
    SPRITE_PALETTE_2 = 0x3F18
    SPRITE_PALETTE_3 = 0x3F1C

    NUM_BYTES_PER_PALETTE = 4
    NUM_BACKGROUND_PALETTES = 4
    NUM_SPRITE_PALETTES = 4
    PPU_PALETTE_SIZE = NUM_BYTES_PER_PALETTE * (NUM_BACKGROUND_PALETTES + NUM_SPRITE_PALETTES)

    TRANSPARENT = 0 # Universal background color and sprite transparency.
    GRAY_COLUMN = 0x30 # First column of the NES system palette containing only gray colors.

    # Sprite memory constants.
    NUM_SPRITES_IN_OAM = 64
    BYTES_PER_SPRITE = 4
    NUM_BYTES_IN_OAM = NUM_SPRITES_IN_OAM * BYTES_PER_SPRITE

    SPRITE_Y_OFFSET = 0
    SPRITE_TILE_INDEX_OFFSET = 1
    SPRITE_ATTRIBUTE_OFFSET = 2
    SPRITE_X_OFFSET = 3

    # Sprite attribute constants.
    SPRITE_FLIPPED_VERTICALLY = 0b10000000
    SPRITE_FLIPPED_HORIZONTALLY = 0b01000000
    SPRITE_BEHIND_BACKGROUND = 0b00100000

    MAX_VISIBLE_X = 255
    MAX_VISIBLE_Y = 239
    INVISIBLE_SPRITE = MAX_VISIBLE_Y + 1

    # PPU register constants.
    PPUCTRL = 0x2000
    PPUMASK = 0x2001
    PPUSTATUS = 0x2002
    OAMADDR = 0x2003
    OAMDATA = 0x2004
    PPUSCROLL = 0x2005
    PPUADDR = 0x2006
    PPUDATA = 0x2007

    # PPUCTRL constants.
    NMI_ENABLED = 0b10000000
    PPU_MASTER_SLAVE_SELECT = 0b01000000 # Unused
    EXTRA_LARGE_SPRITE = 0b00100000
    BACKGROUND_PATTERN_TABLE_SELECTOR = 0b00010000
    SPRITE_PATTERN_TABLE_SELECTOR = 0b00001000
    PPUADDR_AUTOINCREMENT_OF_32 = 0b00000100
    BASE_NAMETABLE_SELECTOR = 0b00000011 # Unimplemented

    # PPUMASK constants.
    BLUE_EMPHASIS = 0b10000000 # Unimplemented
    GREEN_EMPHASIS = 0b01000000 # Unimplemented
    RED_EMPHASIS = 0b00100000 # Unimplemented
    SHOW_SPRITES = 0b00010000
    SHOW_BACKGROUND = 0b00001000
    SHOW_SPRITES_IN_LEFTMOST_TILES = 0b00000100 # Unimplemented
    SHOW_BACKGROUND_IN_LEFTMOST_TILES = 0b00000010 # Unimplemented
    SHOW_GRAYSCALE = 0b00000001

    # PPUSTATUS constants.
    VBLANK_FLAG = 0b10000000
    SPRITE_0_HIT = 0b01000000 # Unimplemented
    SPRITE_OVERFLOW = 0b00100000 # Unimplemented
    PPUSTATUS_BLANK_BITS = 0b00011111

    # PPUSCROLL and PPUADDR constants:
    ADDRESS_LATCH_HI = 0
    ADDRESS_LATCH_LO = 1


cdef class MemoryAccessor():

    cdef MemoryMapper memory_mapper

cdef class Ppu():

    cdef MemoryMapper memory_mapper
    cdef MemoryAccessor memory

    cdef object pattern_tables

    cdef object oam

    cdef object ppu_dynamic_latch

    cdef object ppuctrl
    cdef object ppumask

    cdef object ppustatus

    cdef object vblank

    cdef object oamaddr

    cdef object ppu_address_hi_lo_latch

    cdef object scroll_x_position
    cdef object scroll_y_position

    cdef object ppuaddr

    cdef object ppudata_read_buffer

    cdef object register_writers_
    cdef object register_readers_