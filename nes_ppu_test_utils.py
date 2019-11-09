from ppu import Ppu, NUM_SPRITES_IN_OAM, BYTES_PER_SPRITE, INVISIBLE_SPRITE, SPRITE_Y_OFFSET, SPRITE_X_OFFSET, SPRITE_ATTRIBUTE_OFFSET, SPRITE_TILE_INDEX_OFFSET, PALETTE_BASE_ADDR, SPRITE_PALETTE_BASE_ADDR, NUM_BACKGROUND_PALETTES, NUM_SPRITE_PALETTES, NUM_BYTES_PER_PALETTE
from memory_mapper import MemoryMapper

import os
# Added in an experiment to limit the number of threads started by NumPy.
# os.environ["MKL_NUM_THREADS"] = "1" 
# os.environ["NUMEXPR_NUM_THREADS"] = "1" 
# os.environ["OMP_NUM_THREADS"] = "1" 
import numpy as np

DEFAULT_iNES_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test_utils', 'acopalices.bin')

# Acopalices game related constants.

BIG_ROACH_TOP_LEFT_PATTERN = np.array([
    [0, 0, 0, 0, 2, 3, 3, 3],
    [0, 0, 0, 0, 1, 2, 2, 2],
    [3, 0, 0, 0, 1, 2, 2, 2],
    [0, 3, 0, 0, 1, 1, 2, 2],
    [3, 0, 3, 0, 0, 1, 2, 2],
    [0, 3, 0, 3, 0, 1, 1, 2],
    [0, 0, 3, 0, 3, 0, 1, 1],
    [0, 3, 0, 3, 0, 3, 0, 1]
])
BIG_ROACH_TOP_LEFT_PATTERN_TILE_INDEX = 0

def CreateTestPpu(iNES_file=DEFAULT_iNES_FILE):
    """Return a valid ppu for testing purposes. Any valid iNES file name or valid sequence of bytes read from such a file will work."""
    return Ppu(MemoryMapper(iNES_file))

def insert_background_palette(ppu, nes_image_palette):
    for i in range(0, min(NUM_BACKGROUND_PALETTES*NUM_BYTES_PER_PALETTE, len(nes_image_palette))):
        ppu.memory[PALETTE_BASE_ADDR + i] = nes_image_palette[i]

def insert_sprite_palette(ppu, nes_image_palette):
    for i in range(0, min(NUM_SPRITE_PALETTES*NUM_BYTES_PER_PALETTE, len(nes_image_palette))):
        ppu.memory[SPRITE_PALETTE_BASE_ADDR + i] = nes_image_palette[i]

def hide_all_sprites(ppu):
    for i in range(0, NUM_SPRITES_IN_OAM):
        ppu.oam[BYTES_PER_SPRITE*i + SPRITE_Y_OFFSET] = INVISIBLE_SPRITE

def insert_sprite(ppu, sprite_index, y, x, tile_index, palette_index):
    ppu.oam[BYTES_PER_SPRITE*sprite_index + SPRITE_Y_OFFSET] = y - 1
    ppu.oam[BYTES_PER_SPRITE*sprite_index + SPRITE_X_OFFSET] = x - 1
    ppu.oam[BYTES_PER_SPRITE*sprite_index + SPRITE_TILE_INDEX_OFFSET] = tile_index
    ppu.oam[BYTES_PER_SPRITE*sprite_index + SPRITE_ATTRIBUTE_OFFSET] = palette_index