import unittest
from nes_ppu_test_utils import CreateTestPpu
from nes_cpu_test_utils import CreateTestCpu
import numpy as np


class TestLoad(unittest.TestCase):

    # def test_if_tile_0_is_loaded_in_pattern_table(self):
    #     # GIVEN .chr file (acopalices.bin)
    #     # WHEN I compile it
    #     # THEN I can find the pattern of the tile between addresses $0000 and $0007
    #
    # def test_if_background_palette_is_loaded_inside_image_palette_area(self):
    #     # GIVEN .bin, with chr imported, and image pattern described
    #     # WHEN I compile it
    #     # THEN I can access the palette between $3F00-$3F0F

    def given_a_tile_is_stored_at(self, ppu, tile, start_address):
        hi_bit_address = start_address + 8
        lo_bit_address = start_address
        for x in range(0, tile.shape[0]):
            for y in range(0, tile.shape[1]):
                if tile[x][y] == 0:
                    ppu.memory[lo_bit_address + x] = 0
                    ppu.memory[hi_bit_address + x] = 0
                if tile[x][y] == 1:
                    ppu.memory[lo_bit_address + x] = 1
                    ppu.memory[hi_bit_address + x] = 0
                if tile[x][y] == 2:
                    ppu.memory[lo_bit_address + x] = 0
                    ppu.memory[hi_bit_address + x] = 1
                if tile[x][y] == 3:
                    ppu.memory[lo_bit_address + x] = 1
                    ppu.memory[hi_bit_address + x] = 1
        return

    def given_palette_is_loaded_at_index(self, ppu, color_array):
        palette_start_address = 0x3f00
        for i in range(0, 4):
            ppu.memory[palette_start_address + i] = color_array[i]
        return


    def given_attribute_table_is(self, ppu, attribute_table):
        address = 0x23c0
        attribute_table_size = 64
        for i in range(0, attribute_table_size):
            ppu.memory[address + i] = attribute_table[i]
        return

    def given_name_table_points_to_tile(self, ppu, name_table_address):
        tile_index = 0x0000
        ppu.memory[name_table_address] = tile_index
        return

    def test_if_tile_0_is_rendered_as_background(self):
        tile_pattern = np.array([
            [0, 0, 0, 0, 2, 3, 3, 3],
            [0, 0, 0, 0, 1, 2, 2, 2],
            [3, 0, 0, 0, 1, 2, 2, 2],
            [0, 3, 0, 0, 1, 1, 2, 2],
            [3, 0, 3, 0, 0, 1, 2, 2],
            [0, 3, 0, 3, 0, 1, 1, 2],
            [0, 0, 3, 0, 3, 0, 1, 1],
            [0, 3, 0, 3, 0, 3, 0, 1]
        ])
        first_tile_address = 0x0000
        image_palette = [0x14, 0x31, 0x00, 0x2c]
        zeroed_attribute_table = [0] * 64
        first_name_table_address = 0x2000

        ppu = CreateTestPpu()

        self.given_a_tile_is_stored_at(ppu, tile_pattern, first_tile_address)
        self.given_palette_is_loaded_at_index(ppu, image_palette)
        self.given_attribute_table_is(ppu, zeroed_attribute_table)
        self.given_name_table_points_to_tile(ppu, first_name_table_address)

        # current_result = ppu.render_background()
        # expected_result = []
        #
        # self.assertEqual(current_result, expected_result)
