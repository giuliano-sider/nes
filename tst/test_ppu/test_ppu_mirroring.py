import unittest
from nes_ppu_test_utils import CreateTestPpu


class TestLoad(unittest.TestCase):
    def test_ppu_mirroring_for_addresses_greater_than_4000(self):
        base_address = 0x0000
        index_system_palette = 0x01

        ppu = CreateTestPpu()
        ppu.memory[base_address] = index_system_palette

        self.assertEqual(ppu.memory[base_address + 0x4000], index_system_palette)
        self.assertEqual(ppu.memory[base_address + 0x8000], index_system_palette)
        self.assertEqual(ppu.memory[base_address + 0xC000], index_system_palette)