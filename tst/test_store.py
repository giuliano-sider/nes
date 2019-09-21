import os
import sys
import unittest
from nes_cpu_test_utils import CreateTestCpu, execute_instruction
from instructions import STA_INDIRECT_X, STA_ZEROPAGE, STA_ABSOLUTE, STA_INDIRECT_Y, STA_ZEROPAGE_X


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
        lo_stored_address = 0x00
        hi_stored_address = 0x02
        resolved_address = lo_stored_address + (hi_stored_address << 8)

        self.cpu.memory[zero_page_address + x_value] = lo_stored_address
        self.cpu.memory[zero_page_address + x_value + 1] = hi_stored_address

        self.cpu.set_X(x_value)
        self.cpu.set_A(value_to_be_stored)
        execute_instruction(self.cpu, opcode=STA_INDIRECT_X, op2_lo_byte=zero_page_address)

        expected_pc = initial_pc + 2

        self.assertEqual(self.cpu.memory[resolved_address], value_to_be_stored)
        self.assertEqual(self.cpu.PC(), expected_pc)

    def test_sta_indirect_x_with_overflow(self):
        initial_pc = self.cpu.PC()
        x_value = 0x01
        value_to_be_stored = 0x10
        zero_page_address = 0xFF
        lo_stored_address = 0x00
        hi_stored_address = 0x02
        resolved_address = lo_stored_address + (hi_stored_address << 8)

        self.cpu.memory[(zero_page_address + x_value) % 256] = lo_stored_address
        self.cpu.memory[(zero_page_address + x_value + 1) % 256] = hi_stored_address

        self.cpu.set_X(x_value)
        self.cpu.set_A(value_to_be_stored)
        execute_instruction(self.cpu, opcode=STA_INDIRECT_X, op2_lo_byte=zero_page_address)

        expected_pc = initial_pc + 2

        self.assertEqual(self.cpu.memory[resolved_address], value_to_be_stored)
        self.assertEqual(self.cpu.PC(), expected_pc)

    def test_sta_zeropage(self):
        initial_pc = self.cpu.PC()
        value_to_be_stored = 0x10
        zero_page_address = 0x01

        self.cpu.set_A(value_to_be_stored)
        execute_instruction(self.cpu, opcode=STA_ZEROPAGE, op2_lo_byte=zero_page_address)
        expected_pc = initial_pc + 2

        self.assertEqual(self.cpu.PC(), expected_pc)
        self.assertEqual(self.cpu.memory[zero_page_address], value_to_be_stored)

    def test_sta_absolute(self):
        initial_pc = self.cpu.PC()
        value_to_be_stored = 0x10
        lo_absolute_address = 0x01
        hi_absolute_address = 0xFF
        resolved_address = lo_absolute_address + (hi_absolute_address << 8)

        self.cpu.set_A(value_to_be_stored)

        execute_instruction(
            self.cpu,
            opcode=STA_ABSOLUTE,
            op2_lo_byte=lo_absolute_address,
            op2_hi_byte=hi_absolute_address
        )

        expected_pc = initial_pc + 3

        self.assertEqual(self.cpu.PC(), expected_pc)
        self.assertEqual(self.cpu.memory[resolved_address], value_to_be_stored)

    def test_sta_indirect_y(self):
        initial_pc = self.cpu.PC()
        zero_page_address = 0x10
        resolved_address = 0x0101
        value_to_be_stored = 0x10
        y_value = 0x01

        self.cpu.memory[zero_page_address] = 0x00
        self.cpu.memory[zero_page_address + 1] = 0x01
        self.cpu.set_A(value_to_be_stored)
        self.cpu.set_Y(y_value)

        execute_instruction(
            self.cpu,
            opcode=STA_INDIRECT_Y,
            op2_lo_byte=zero_page_address,
        )

        expected_pc = initial_pc + 2

        self.assertEqual(self.cpu.PC(), expected_pc)
        self.assertEqual(self.cpu.memory[resolved_address], value_to_be_stored)

    def test_sta_indirect_y_with_overflow(self):
        initial_pc = self.cpu.PC()
        zero_page_address = 0x10
        resolved_address = 0x0000
        value_to_be_stored = 0x10
        y_value = 0x01

        self.cpu.memory[zero_page_address] = 0xFF
        self.cpu.memory[zero_page_address + 1] = 0xFF
        self.cpu.set_A(value_to_be_stored)
        self.cpu.set_Y(y_value)

        execute_instruction(
            self.cpu,
            opcode=STA_INDIRECT_Y,
            op2_lo_byte=zero_page_address,
        )

        expected_pc = initial_pc + 2

        self.assertEqual(self.cpu.PC(), expected_pc)
        self.assertEqual(self.cpu.memory[resolved_address], value_to_be_stored)

    def test_sta_zero_page_x(self):
        initial_pc = self.cpu.PC()
        x_value = 0x01
        value_to_be_stored = 0x10
        zero_page_address = 0x01

        self.cpu.set_X(x_value)
        self.cpu.set_A(value_to_be_stored)
        execute_instruction(self.cpu, opcode=STA_ZEROPAGE_X, op2_lo_byte=zero_page_address)

        expected_address = zero_page_address + x_value
        expected_pc = initial_pc + 2

        self.assertEqual(self.cpu.memory[expected_address], value_to_be_stored)
        self.assertEqual(self.cpu.PC(), expected_pc)

    def test_sta_zero_page_x_with_overflow(self):
        initial_pc = self.cpu.PC()
        x_value = 0x01
        value_to_be_stored = 0x10
        zero_page_address = 0xFF
        resolved_address = 0x00

        self.cpu.set_X(x_value)
        self.cpu.set_A(value_to_be_stored)
        execute_instruction(self.cpu, opcode=STA_ZEROPAGE_X, op2_lo_byte=zero_page_address)

        expected_pc = initial_pc + 2

        self.assertEqual(self.cpu.memory[resolved_address], value_to_be_stored)
        self.assertEqual(self.cpu.PC(), expected_pc)

if __name__ == '__main__':
    unittest.main()