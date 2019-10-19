import os
import sys
import unittest

from nes_ppu_test_utils import CreateTestPpu


class TestLoad(unittest.TestCase):

    def test_if_background_color_is_copied_for_every_four_bytes(self):
        background_address = 0x3F00
        index_system_palette = 0x01

        ppu = CreateTestPpu()
        ppu.memory[background_address] = index_system_palette

        for address in range(0x3F00, 0x3FFF, 4):
            self.assertEqual(ppu.memory[address], index_system_palette)

    def test_ppu_color_palette_mirroring(self):
        base_address_image = 0x3F00
        background_index_system_palette_1 = 0x01
        index_system_palette_2 = 0x02
        index_system_palette_3 = 0x03
        index_system_palette_4 = 0x04
        index_system_palette_5 = 0x05
        index_system_palette_6 = 0x06
        index_system_palette_7 = 0x07
        index_system_palette_8 = 0x08
        index_system_palette_9 = 0x09
        index_system_palette_10 = 0x0A
        index_system_palette_11 = 0x0B
        index_system_palette_12 = 0x0C
        index_system_palette_13 = 0x0D

        base_address_sprite = 0x3F10
        sprite_index_system_palette_2 = 0x12
        sprite_index_system_palette_3 = 0x13
        sprite_index_system_palette_4 = 0x14
        sprite_index_system_palette_5 = 0x15
        sprite_index_system_palette_6 = 0x16
        sprite_index_system_palette_7 = 0x17
        sprite_index_system_palette_8 = 0x18
        sprite_index_system_palette_9 = 0x19
        sprite_index_system_palette_10 = 0x1A
        sprite_index_system_palette_11 = 0x1B
        sprite_index_system_palette_12 = 0x1C
        sprite_index_system_palette_13 = 0x1D

        ppu = CreateTestPpu()
        ppu.memory[base_address_image] = background_index_system_palette_1
        ppu.memory[base_address_image + 1] = index_system_palette_2
        ppu.memory[base_address_image + 2] = index_system_palette_3
        ppu.memory[base_address_image + 3] = index_system_palette_4

        ppu.memory[base_address_image + 4] = background_index_system_palette_1
        ppu.memory[base_address_image + 5] = index_system_palette_5
        ppu.memory[base_address_image + 6] = index_system_palette_6
        ppu.memory[base_address_image + 7] = index_system_palette_7

        ppu.memory[base_address_image + 8] = background_index_system_palette_1
        ppu.memory[base_address_image + 9] = index_system_palette_8
        ppu.memory[base_address_image + 10] = index_system_palette_9
        ppu.memory[base_address_image + 11] = index_system_palette_10

        ppu.memory[base_address_image + 12] = background_index_system_palette_1
        ppu.memory[base_address_image + 13] = index_system_palette_11
        ppu.memory[base_address_image + 14] = index_system_palette_12
        ppu.memory[base_address_image + 15] = index_system_palette_13

        ppu.memory[base_address_sprite] = background_index_system_palette_1
        ppu.memory[base_address_sprite + 1] = sprite_index_system_palette_2
        ppu.memory[base_address_sprite + 2] = sprite_index_system_palette_3
        ppu.memory[base_address_sprite + 3] = sprite_index_system_palette_4

        ppu.memory[base_address_sprite + 4] = background_index_system_palette_1
        ppu.memory[base_address_sprite + 5] = sprite_index_system_palette_5
        ppu.memory[base_address_sprite + 6] = sprite_index_system_palette_6
        ppu.memory[base_address_sprite + 7] = sprite_index_system_palette_7

        ppu.memory[base_address_sprite + 8] = background_index_system_palette_1
        ppu.memory[base_address_sprite + 9] = sprite_index_system_palette_8
        ppu.memory[base_address_sprite + 10] = sprite_index_system_palette_9
        ppu.memory[base_address_sprite + 11] = sprite_index_system_palette_10

        ppu.memory[base_address_sprite + 12] = background_index_system_palette_1
        ppu.memory[base_address_sprite + 13] = sprite_index_system_palette_11
        ppu.memory[base_address_sprite + 14] = sprite_index_system_palette_12
        ppu.memory[base_address_sprite + 15] = sprite_index_system_palette_13

        for address in range(0x3F00, 0x3FFF, 0x20):
            self.assertEqual(ppu.memory[address], background_index_system_palette_1)
            self.assertEqual(ppu.memory[address + 1], index_system_palette_2)
            self.assertEqual(ppu.memory[address + 2], index_system_palette_3)
            self.assertEqual(ppu.memory[address + 3], index_system_palette_4)
            self.assertEqual(ppu.memory[address + 4], background_index_system_palette_1)
            self.assertEqual(ppu.memory[address + 5], index_system_palette_5)
            self.assertEqual(ppu.memory[address + 6], index_system_palette_6)
            self.assertEqual(ppu.memory[address + 7], index_system_palette_7)
            self.assertEqual(ppu.memory[address + 8], background_index_system_palette_1)
            self.assertEqual(ppu.memory[address + 9], index_system_palette_8)
            self.assertEqual(ppu.memory[address + 10], index_system_palette_9)
            self.assertEqual(ppu.memory[address + 11], index_system_palette_10)
            self.assertEqual(ppu.memory[address + 12], background_index_system_palette_1)
            self.assertEqual(ppu.memory[address + 13], index_system_palette_11)
            self.assertEqual(ppu.memory[address + 14], index_system_palette_12)
            self.assertEqual(ppu.memory[address + 15], index_system_palette_13)

            self.assertEqual(ppu.memory[address + 16], background_index_system_palette_1)
            self.assertEqual(ppu.memory[address + 17], sprite_index_system_palette_2)
            self.assertEqual(ppu.memory[address + 18], sprite_index_system_palette_3)
            self.assertEqual(ppu.memory[address + 19], sprite_index_system_palette_4)
            self.assertEqual(ppu.memory[address + 20], background_index_system_palette_1)
            self.assertEqual(ppu.memory[address + 21], sprite_index_system_palette_5)
            self.assertEqual(ppu.memory[address + 22], sprite_index_system_palette_6)
            self.assertEqual(ppu.memory[address + 23], sprite_index_system_palette_7)
            self.assertEqual(ppu.memory[address + 24], background_index_system_palette_1)
            self.assertEqual(ppu.memory[address + 25], sprite_index_system_palette_8)
            self.assertEqual(ppu.memory[address + 26], sprite_index_system_palette_9)
            self.assertEqual(ppu.memory[address + 27], sprite_index_system_palette_10)
            self.assertEqual(ppu.memory[address + 28], background_index_system_palette_1)
            self.assertEqual(ppu.memory[address + 29], sprite_index_system_palette_11)
            self.assertEqual(ppu.memory[address + 30], sprite_index_system_palette_12)
            self.assertEqual(ppu.memory[address + 31], sprite_index_system_palette_13)