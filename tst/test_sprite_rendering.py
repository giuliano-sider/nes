import os
import sys
import unittest

sys.path += os.path.join(os.pardir, os.pardir)
from ppu import PPUCTRL, NUM_BYTES_PER_PALETTE, BYTES_PER_SPRITE, SPRITE_Y_OFFSET, SPRITE_X_OFFSET, SPRITE_ATTRIBUTE_OFFSET, SPRITE_TILE_INDEX_OFFSET, NUM_SPRITES_IN_OAM, SPRITE_PALETTE_BASE_ADDR, SCREEN_HEIGHT, SCREEN_WIDTH
from nes_ppu_test_utils import CreateTestPpu, BIG_ROACH_TOP_LEFT_PATTERN, BIG_ROACH_TOP_LEFT_PATTERN_TILE_INDEX
from nes_cpu_test_utils import CreateTestCpu
import numpy as np


class TestSpriteRendering(unittest.TestCase):

    def test_get_pixel_pattern(self):
        ppu = CreateTestPpu()

        for y in range(8):
            for x in range(8):
                self.assertEqual(
                    ppu.get_pixel_pattern(0, BIG_ROACH_TOP_LEFT_PATTERN_TILE_INDEX, y, x),
                    BIG_ROACH_TOP_LEFT_PATTERN[y, x])

    def test_get_sprite_tile(self):
        ppu = CreateTestPpu()
        ppu.ppuctrl = 0 # 8x8 sprites and sprite pattern table at 0
        sprite_idx = 0
        sprite_palette = 3
        # Sprite attributes
        ppu.oam[BYTES_PER_SPRITE*sprite_idx + SPRITE_Y_OFFSET] = 100 # y = 101
        ppu.oam[BYTES_PER_SPRITE*sprite_idx + SPRITE_TILE_INDEX_OFFSET] = BIG_ROACH_TOP_LEFT_PATTERN_TILE_INDEX
        ppu.oam[BYTES_PER_SPRITE*sprite_idx + SPRITE_ATTRIBUTE_OFFSET] = sprite_palette # Sprite palette 3, no flip
        ppu.oam[BYTES_PER_SPRITE*sprite_idx + SPRITE_X_OFFSET] = 100 # x = 101

        big_roach_top_left_tile = ppu.get_sprite_tile(sprite_idx)

        for y in range(8):
            for x in range(8):
                self.assertEqual(big_roach_top_left_tile[y, x], 
                                 BIG_ROACH_TOP_LEFT_PATTERN[y, x] + 0x10 + NUM_BYTES_PER_PALETTE*sprite_palette)

    def test_render_sprites_single_sprite(self):
        ppu = CreateTestPpu()
        sprite_idx = 0
        sprite_palette = 3
        ppu.oam[BYTES_PER_SPRITE*sprite_idx + SPRITE_Y_OFFSET] = 100 # y = 101
        ppu.oam[BYTES_PER_SPRITE*sprite_idx + SPRITE_TILE_INDEX_OFFSET] = BIG_ROACH_TOP_LEFT_PATTERN_TILE_INDEX
        ppu.oam[BYTES_PER_SPRITE*sprite_idx + SPRITE_ATTRIBUTE_OFFSET] = sprite_palette # no flip, not behind background
        ppu.oam[BYTES_PER_SPRITE*sprite_idx + SPRITE_X_OFFSET] = 100 # x = 101
        for sprite_idx in range(1, NUM_SPRITES_IN_OAM):
            ppu.oam[BYTES_PER_SPRITE*sprite_idx + SPRITE_Y_OFFSET] = 0xFF # off-screen
        ppu.ppuctrl = 0 # 8x8 sprites and sprite pattern table at 0
        ppu.memory[SPRITE_PALETTE_BASE_ADDR + NUM_BYTES_PER_PALETTE*sprite_palette + 0] = 0x00
        ppu.memory[SPRITE_PALETTE_BASE_ADDR + NUM_BYTES_PER_PALETTE*sprite_palette + 1] = 0x11
        ppu.memory[SPRITE_PALETTE_BASE_ADDR + NUM_BYTES_PER_PALETTE*sprite_palette + 2] = 0x15
        ppu.memory[SPRITE_PALETTE_BASE_ADDR + NUM_BYTES_PER_PALETTE*sprite_palette + 3] = 0x1A

        screen = ppu.render_sprites(background=np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH), dtype=np.int32))

        sprite_0 = np.array([
            [0x00, 0x00, 0x00, 0x00, 0x15, 0x1A, 0x1A, 0x1A],
            [0x00, 0x00, 0x00, 0x00, 0x11, 0x15, 0x15, 0x15],
            [0x1A, 0x00, 0x00, 0x00, 0x11, 0x15, 0x15, 0x15],
            [0x00, 0x1A, 0x00, 0x00, 0x11, 0x11, 0x15, 0x15],
            [0x1A, 0x00, 0x1A, 0x00, 0x00, 0x11, 0x15, 0x15],
            [0x00, 0x1A, 0x00, 0x1A, 0x00, 0x11, 0x11, 0x15],
            [0x00, 0x00, 0x1A, 0x00, 0x1A, 0x00, 0x11, 0x11],
            [0x00, 0x1A, 0x00, 0x1A, 0x00, 0x1A, 0x00, 0x11]
        ])
        expected_screen = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH), dtype=np.int32)
        expected_screen[101:109, 101:109] = sprite_0

        self.assertTrue(np.all(screen == expected_screen))



if __name__ == '__main__':
    unittest.main()