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

    def given_palette_is_loaded_at_index(self, ppu, image_palette):
        palette_start_address = 0x3f00
        for i in range(0, 4):
            ppu.memory[palette_start_address + i] = image_palette[i]
        return

    @staticmethod
    def given_image_palette(ppu, image_palette):
        palette_start_address = 0x3f00
        for i in range(0, 16):
            ppu.memory[palette_start_address + i] = image_palette[i]
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

    def given_pattern_table_in_address(self, ppu,  address, tile):
        current_address = address
        for x in range(0, 8):
            bit_string = ""
            for y in range(0, 8):
                bit_string = bit_string + str(tile[x][y])
            content = int(bit_string, 2)
            ppu.memory[current_address] = content
            current_address = current_address + 1


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

        zero_array = [0x75, 0x75, 0x75]
        one_array = [0x27, 0x1b, 0x8f]
        two_array = [0x00, 0x00, 0xab]
        three_array = [0x47, 0x00, 0x9f]
        expected_tile = np.array([
            [zero_array, zero_array, zero_array, zero_array, two_array, three_array, three_array, three_array],
            [zero_array, zero_array, zero_array, zero_array, one_array, two_array, two_array, two_array],
            [three_array, zero_array, zero_array, zero_array, one_array, two_array, two_array, two_array],
            [zero_array, three_array, zero_array, zero_array, one_array, one_array, two_array, two_array],
            [one_array, zero_array, three_array, zero_array, zero_array, one_array, two_array, two_array],
            [zero_array, three_array, zero_array, three_array, zero_array, one_array, one_array, two_array],
            [zero_array, zero_array, three_array, zero_array, three_array, zero_array, one_array, one_array],
            [zero_array, three_array, zero_array, three_array, zero_array, three_array, zero_array, one_array]
        ])

        current_result = ppu.render_background()
        # self.assertEqual(current_result, expected_tile)

    def test_if_gets_the_right_attribute_set_index(self):
        ppu = CreateTestPpu()

        name_table_index = 0
        expected_attr_set_index = 0
        current_attr_set_index = ppu.get_attribute_set_index_from_name_table_index(name_table_index)
        self.assertEqual(expected_attr_set_index, current_attr_set_index)

        name_table_index = 2
        expected_attr_set_index = 0
        current_attr_set_index = ppu.get_attribute_set_index_from_name_table_index(name_table_index)
        self.assertEqual(expected_attr_set_index, current_attr_set_index)

        name_table_index = 32
        expected_attr_set_index = 0
        current_attr_set_index = ppu.get_attribute_set_index_from_name_table_index(name_table_index)
        self.assertEqual(expected_attr_set_index, current_attr_set_index)

        name_table_index = 36
        expected_attr_set_index = 1
        current_attr_set_index = ppu.get_attribute_set_index_from_name_table_index(name_table_index)
        self.assertEqual(expected_attr_set_index, current_attr_set_index)

        name_table_index = 128
        expected_attr_set_index = 8
        current_attr_set_index = ppu.get_attribute_set_index_from_name_table_index(name_table_index)
        self.assertEqual(expected_attr_set_index, current_attr_set_index)

        name_table_index = 104
        expected_attr_set_index = 2
        current_attr_set_index = ppu.get_attribute_set_index_from_name_table_index(name_table_index)
        self.assertEqual(expected_attr_set_index, current_attr_set_index)

    def test_if_get_right_palette_set(self):
        attribute_table = []
        attribute_set_0 = 0x1B  # 00 - 01 - 10 - 11
        attribute_set_1 = 0xF2  # 11 - 11 - 00 - 10
        default_attribute_set = 0x00

        attribute_table.append(attribute_set_0)
        attribute_table.append(attribute_set_1)
        for i in range(0, 62):
            attribute_table.append(default_attribute_set)

        ppu = CreateTestPpu()

        self.given_attribute_table_is(ppu, attribute_table)

        name_table_index = 36
        attr_set_index = ppu.get_attribute_set_index_from_name_table_index(name_table_index)
        current_palette_index = ppu.get_palette_set_index(attr_set_index, name_table_index)
        expected_palette_index = 0b10
        self.assertEqual(expected_palette_index, current_palette_index)

        name_table_index = 70
        attr_set_index = ppu.get_attribute_set_index_from_name_table_index(name_table_index)
        current_palette_index = ppu.get_palette_set_index(attr_set_index, name_table_index)
        expected_palette_index = 0b11
        self.assertEqual(expected_palette_index, current_palette_index)

        name_table_index = 3
        attr_set_index = ppu.get_attribute_set_index_from_name_table_index(name_table_index)
        current_palette_index = ppu.get_palette_set_index(attr_set_index, name_table_index)
        expected_palette_index = 0b10
        self.assertEqual(expected_palette_index, current_palette_index)

        name_table_index = 101
        attr_set_index = ppu.get_attribute_set_index_from_name_table_index(name_table_index)
        current_palette_index = ppu.get_palette_set_index(attr_set_index, name_table_index)
        expected_palette_index = 0b11
        self.assertEqual(expected_palette_index, current_palette_index)

        name_table_index = 98
        attr_set_index = ppu.get_attribute_set_index_from_name_table_index(name_table_index)
        current_palette_index = ppu.get_palette_set_index(attr_set_index, name_table_index)
        expected_palette_index = 0b00
        self.assertEqual(expected_palette_index, current_palette_index)

    def test_if_gets_tile_pattern_from_name_table_index(self):
        tile_pattern_lo_bit = np.array([
            [0, 0, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 1, 1, 0, 0],
            [1, 0, 1, 0, 0, 1, 0, 0],
            [0, 1, 0, 1, 0, 1, 1, 0],
            [0, 0, 1, 0, 1, 0, 1, 1],
            [0, 1, 0, 1, 0, 1, 0, 1]
        ])

        tile_pattern_hi_bit = np.array([
            [0, 0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 1, 1, 1],
            [0, 1, 0, 0, 0, 0, 1, 1],
            [0, 0, 1, 0, 0, 0, 1, 1],
            [0, 1, 0, 1, 0, 0, 0, 1],
            [0, 0, 1, 0, 1, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 0, 0]
        ])

        expected_tile = np.array([
            [0, 0, 0, 0, 2, 3, 3, 3],
            [0, 0, 0, 0, 1, 2, 2, 2],
            [3, 0, 0, 0, 1, 2, 2, 2],
            [0, 3, 0, 0, 1, 1, 2, 2],
            [1, 0, 3, 0, 0, 1, 2, 2],
            [0, 3, 0, 3, 0, 1, 1, 2],
            [0, 0, 3, 0, 3, 0, 1, 1],
            [0, 3, 0, 3, 0, 3, 0, 1]
        ])

        ppu = CreateTestPpu()

        self.given_pattern_table_in_address(ppu, 0x0000, tile_pattern_lo_bit)
        self.given_pattern_table_in_address(ppu, 0x0008, tile_pattern_hi_bit)
        name_table_index = 0
        tile = ppu.get_tile_pattern_from_name_table_index(name_table_index)
        for x in range(0, 8):
            for y in range(0, 8):
                self.assertEqual(tile[x][y], expected_tile[x][y])

        self.given_pattern_table_in_address(ppu, 0x0010, tile_pattern_lo_bit)
        self.given_pattern_table_in_address(ppu, 0x0018, tile_pattern_hi_bit)
        name_table_index = 1
        tile = ppu.get_tile_pattern_from_name_table_index(name_table_index)
        for x in range(0, 8):
            for y in range(0, 8):
                self.assertEqual(tile[x][y], expected_tile[x][y])

        self.given_pattern_table_in_address(ppu, 0x0050, tile_pattern_lo_bit)
        self.given_pattern_table_in_address(ppu, 0x0058, tile_pattern_hi_bit)
        name_table_index = 5
        tile = ppu.get_tile_pattern_from_name_table_index(name_table_index)
        for x in range(0, 8):
            for y in range(0, 8):
                self.assertEqual(tile[x][y], expected_tile[x][y])

    def test_if_gets_the_right_nes_color_given_palette_set_and_pattern(self):
        nes_image_palette = [0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15]
        ppu = CreateTestPpu()
        self.given_image_palette(ppu, nes_image_palette)

        palette_set_index = 0
        tile_pattern_value = 0
        nes_color = ppu.get_nes_color_from_palette(palette_set_index, tile_pattern_value)
        expected_nes_color = 0
        self.assertEqual(nes_color, expected_nes_color)

        palette_set_index = 1
        tile_pattern_value = 0
        nes_color = ppu.get_nes_color_from_palette(palette_set_index, tile_pattern_value)
        expected_nes_color = 0
        self.assertEqual(nes_color, expected_nes_color)

        palette_set_index = 0
        tile_pattern_value = 3
        nes_color = ppu.get_nes_color_from_palette(palette_set_index, tile_pattern_value)
        expected_nes_color = 3
        self.assertEqual(nes_color, expected_nes_color)

        palette_set_index = 2
        tile_pattern_value = 2
        nes_color = ppu.get_nes_color_from_palette(palette_set_index, tile_pattern_value)
        expected_nes_color = 10
        self.assertEqual(nes_color, expected_nes_color)

    def test_nes_to_rgb_conversion(self):
        ppu = CreateTestPpu()

        nes_color = 0
        expected_rgb_color = (0x75, 0x75, 0x75)
        rgb_color = ppu.convert_nes_color_to_rgb(nes_color)
        self.assertEqual(rgb_color, expected_rgb_color)

        nes_color = 0x13
        expected_rgb_color = (0x83, 0x00, 0xF3)
        rgb_color = ppu.convert_nes_color_to_rgb(nes_color)
        self.assertEqual(rgb_color, expected_rgb_color)

        nes_color = 0x2a
        expected_rgb_color = (0x4f, 0xdf, 0x4b)
        rgb_color = ppu.convert_nes_color_to_rgb(nes_color)
        self.assertEqual(rgb_color, expected_rgb_color)

    def test_creation_of_rgb_tile_pattern(self):
        ppu = CreateTestPpu()
        nes_tile = np.array([
            [0, 0, 0, 0, 2, 3, 3, 3],
            [0, 0, 0, 0, 1, 2, 2, 2],
            [3, 0, 0, 0, 1, 2, 2, 2],
            [0, 3, 0, 0, 1, 1, 2, 2],
            [1, 0, 3, 0, 0, 1, 2, 2],
            [0, 3, 0, 3, 0, 1, 1, 2],
            [0, 0, 3, 0, 3, 0, 1, 1],
            [0, 3, 0, 3, 0, 3, 0, 1]
        ])
        nes_image_palette = [0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15]
        self.given_image_palette(ppu, nes_image_palette)

        palette_set = 0
        zero_array = [0x75, 0x75, 0x75]
        one_array = [0x27, 0x1b, 0x8f]
        two_array = [0x00, 0x00, 0xab]
        three_array = [0x47, 0x00, 0x9f]
        expected_tile = np.array([
            [zero_array, zero_array, zero_array, zero_array, two_array, three_array, three_array, three_array],
            [zero_array, zero_array, zero_array, zero_array, one_array, two_array, two_array, two_array],
            [three_array, zero_array, zero_array, zero_array, one_array, two_array, two_array, two_array],
            [zero_array, three_array, zero_array, zero_array, one_array, one_array, two_array, two_array],
            [one_array, zero_array, three_array, zero_array, zero_array, one_array, two_array, two_array],
            [zero_array, three_array, zero_array, three_array, zero_array, one_array, one_array, two_array],
            [zero_array, zero_array, three_array, zero_array, three_array, zero_array, one_array, one_array],
            [zero_array, three_array, zero_array, three_array, zero_array, three_array, zero_array, one_array]
        ])
        current_tile = ppu.convert_nes_tile_pattern_to_rgb(nes_tile, palette_set)
        for i in range(0, 8):
            for j in range(0, 8):
                for channel in range(0, 3):
                    self.assertEqual(current_tile[i][j][channel], expected_tile[i][j][channel])

    def test_get_tile_by_name_table_index(self):
        ppu = CreateTestPpu()

        tile_pattern_lo_bit = np.array([
            [0, 0, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 1, 1, 0, 0],
            [1, 0, 1, 0, 0, 1, 0, 0],
            [0, 1, 0, 1, 0, 1, 1, 0],
            [0, 0, 1, 0, 1, 0, 1, 1],
            [0, 1, 0, 1, 0, 1, 0, 1]
        ])

        tile_pattern_hi_bit = np.array([
            [0, 0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 1, 1, 1],
            [0, 1, 0, 0, 0, 0, 1, 1],
            [0, 0, 1, 0, 0, 0, 1, 1],
            [0, 1, 0, 1, 0, 0, 0, 1],
            [0, 0, 1, 0, 1, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 0, 0]
        ])

        nes_image_palette = [0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15]
        self.given_image_palette(ppu, nes_image_palette)
        self.given_pattern_table_in_address(ppu, 0x0000, tile_pattern_lo_bit)
        self.given_pattern_table_in_address(ppu, 0x0008, tile_pattern_hi_bit)
        expected_tile = np.array([
            [0, 0, 0, 0, 2, 3, 3, 3],
            [0, 0, 0, 0, 1, 2, 2, 2],
            [3, 0, 0, 0, 1, 2, 2, 2],
            [0, 3, 0, 0, 1, 1, 2, 2],
            [1, 0, 3, 0, 0, 1, 2, 2],
            [0, 3, 0, 3, 0, 1, 1, 2],
            [0, 0, 3, 0, 3, 0, 1, 1],
            [0, 3, 0, 3, 0, 3, 0, 1]
        ])
        current_tile = ppu.get_tile_by_name_table_index(0)

        for i in range(0, 8):
            for j in range(0, 8):
                self.assertEqual(current_tile[i][j], expected_tile[i][j])

    def test_name_table_mirroring(self):
        ppu = CreateTestCpu()
        start_name_table_address = 0x2000
        start_mirror_address = 0x3000

        for i in range(0, 0x1000):
            ppu.memory[start_name_table_address + i] = start_name_table_address + i
            self.assertEqual(ppu.memory[start_name_table_address + i], ppu.memory[start_mirror_address + i])