import os
import sys
import unittest
from nes_cpu_test_utils import CreateTestCpu, execute_instruction
from instructions import STA_INDIRECT_X


class TestStore(unittest.TestCase):

    def setUp(self):
        self.cpu = CreateTestCpu()
        self.cpu.clear_carry()
        self.cpu.clear_zero()

    def test_sta_indirect_x(self):
        initial_pc = self.cpu.PC()
        x_value = 0x01
        value_to_be_stored = 0x10
        zero_page_address = 0x01

        self.cpu.set_X(x_value)
        self.cpu.set_A(value_to_be_stored)
        execute_instruction(self.cpu, opcode=STA_INDIRECT_X, op2_lo_byte=zero_page_address)

        expected_address = zero_page_address + x_value
        expected_pc = initial_pc + 2

        self.assertEqual(self.cpu.memory[expected_address], value_to_be_stored)
        self.assertEqual(self.cpu.PC(), expected_pc)

    def test_sta_indirect_x_with_overflow(self):
        initial_pc = self.cpu.PC()
        x_value = 0x01
        value_to_be_stored = 0x10
        zero_page_address = 0xFF
        resolved_address = 0x00

        self.cpu.set_X(x_value)
        self.cpu.set_A(value_to_be_stored)
        execute_instruction(self.cpu, opcode=STA_INDIRECT_X, op2_lo_byte=zero_page_address)

        expected_pc = initial_pc + 2

        self.assertEqual(self.cpu.memory[resolved_address], value_to_be_stored)
        self.assertEqual(self.cpu.PC(), expected_pc)

if __name__ == '__main__':
    unittest.main()