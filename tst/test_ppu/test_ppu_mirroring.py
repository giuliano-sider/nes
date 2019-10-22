import unittest
from nes_ppu_test_utils import CreateTestPpu
from nes_cpu_test_utils import CreateTestCpu


class TestLoad(unittest.TestCase):

    def test_ppu_mirroring_for_addresses_greater_than_4000(self):
        base_address = 0x0000
        index_system_palette = 0x01

        ppu = CreateTestPpu()
        ppu.memory[base_address] = index_system_palette

        self.assertEqual(ppu.memory[base_address + 0x4000], index_system_palette)
        self.assertEqual(ppu.memory[base_address + 0x8000], index_system_palette)
        self.assertEqual(ppu.memory[base_address + 0xC000], index_system_palette)

    def test_if_cpu_mirror_ppu_content_from_2000_every_8_bytes(self):
        content_address = 0x2000
        content = 0x01
        cpu = CreateTestCpu()
        cpu.memory[content_address] = content

        for address in range(0x2000, 0x4000, 8):
            self.assertEqual(cpu.memory[address], content)

    def test_if_cpu_mirror_ppu_content_from_2000_every_8_bytes(self):
        content_address = 0x2001
        content = 0x02
        cpu = CreateTestCpu()
        cpu.memory[content_address] = content

        for address in range(0x2001, 0x4000, 8):
            self.assertEqual(cpu.memory[address], content)
