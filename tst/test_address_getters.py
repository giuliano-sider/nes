import os
import sys
import unittest

sys.path += os.pardir
from nes_cpu_test_utils import CreateTestCpu, insert_instruction
from instructions import LDA_INDIRECT_X, LDA_INDIRECT_Y
from Instructions.address_getters import get_indirect_x, get_indirect_y

class TestLogicalInstructions(unittest.TestCase):

    def test_get_indirect_x_no_wraparound(self):
        cpu = CreateTestCpu()
        cpu.set_X(0xFE)
        # correct address is here
        cpu.memory[0xFE] = 0x10
        cpu.memory[0xFF] = 0x20
        cpu.memory[0x2010] = 0xAE
        # wrong address is here
        cpu.memory[0x00] = 0x12
        cpu.memory[0x01] = 0x34
        cpu.memory[0x3412] = 0xAF
        # LDA (0x01, X)
        insert_instruction(cpu, cpu.PC(), opcode=LDA_INDIRECT_X, op2_lo_byte=0x00)

        self.assertEqual(get_indirect_x(cpu), 0xAE)

    def test_get_indirect_x_wraparound_x(self):
        cpu = CreateTestCpu()
        cpu.set_X(0xFF)
        # correct address is here
        cpu.memory[0x00] = 0x00
        cpu.memory[0x01] = 0x20
        cpu.memory[0x2000] = 0xAE
        # wrong address is here
        cpu.memory[0x100] = 0x12
        cpu.memory[0x101] = 0x34
        cpu.memory[0x3412] = 0xAF
        # LDA (0x01, X)
        insert_instruction(cpu, cpu.PC(), opcode=LDA_INDIRECT_X, op2_lo_byte=0x01)

        self.assertEqual(get_indirect_x(cpu), 0xAE)

    def test_get_indirect_x_wraparound_indirect_address(self):
        cpu = CreateTestCpu()
        cpu.set_X(0xFE)
        # correct address is here
        cpu.memory[0xFF] = 0x00
        cpu.memory[0x00] = 0x20
        cpu.memory[0x2000] = 0xAE
        # wrong address is here
        cpu.memory[0x100] = 0x12
        cpu.memory[0x1200] = 0xAF
        # LDA (0x01, X)
        insert_instruction(cpu, cpu.PC(), opcode=LDA_INDIRECT_X, op2_lo_byte=0x01)

        self.assertEqual(get_indirect_x(cpu), 0xAE)


    def test_get_indirect_y_no_wraparound(self):
        cpu = CreateTestCpu()
        cpu.set_Y(0xFE)
        # correct value is here
        cpu.memory[0x00] = 0x00
        cpu.memory[0x01] = 0x20
        cpu.memory[0x2000 + 0xFE] = 0xAE
        # wrong value is here
        cpu.memory[0x2000] = 0xAF
        # LDA (0x00), Y
        insert_instruction(cpu, cpu.PC(), opcode=LDA_INDIRECT_Y, op2_lo_byte=0x00)

        self.assertEqual(get_indirect_y(cpu), 0xAE)

    def test_get_indirect_y_wraparound_y(self):
        cpu = CreateTestCpu()
        cpu.set_Y(0xFF)
        # correct value is here
        cpu.memory[0x00] = 0x01
        cpu.memory[0x01] = 0x20
        cpu.memory[0x2100] = 0xAE
        # wrong value is here
        cpu.memory[0x2000] = 0xAF
        # LDA (0x00), Y
        insert_instruction(cpu, cpu.PC(), opcode=LDA_INDIRECT_Y, op2_lo_byte=0x00)

        self.assertEqual(get_indirect_y(cpu), 0xAE)

    def test_get_indirect_y_wraparound_indirect_address(self):
        cpu = CreateTestCpu()
        cpu.set_Y(0xFE)
        # correct value is here
        cpu.memory[0xFF] = 0x00
        cpu.memory[0x00] = 0x20
        cpu.memory[0x2000 + 0xFE] = 0xAE
        # wrong value is here
        cpu.memory[0x100] = 0x12
        cpu.memory[0x1200 + 0xFE] = 0xAF
        # LDA (0xFF), Y
        insert_instruction(cpu, cpu.PC(), opcode=LDA_INDIRECT_Y, op2_lo_byte=0xFF)

        self.assertEqual(get_indirect_y(cpu), 0xAE)


if __name__ == '__main__':
    unittest.main()




