import os
import sys
import unittest

sys.path += os.pardir
from nes_cpu_test_utils import CreateTestCpu, execute_instruction
from instructions import *

class TestLogicalInstructions(unittest.TestCase):

    def test_if_BIT_sets_status_flags(self):
        cpu = CreateTestCpu()
        cpu.set_A(0)
        cpu.set_P(0)
        cpu.memory[0x01] = 0b11000000

        execute_instruction(cpu, opcode=BIT_ZEROPAGE, op2_lo_byte=0x01)

        self.assertEqual(cpu.negative(), 1)
        self.assertEqual(cpu.overflow(), 1)
        self.assertEqual(cpu.zero(), 1)

    def test_if_BIT_absolute_sets_status_flags(self):
        cpu = CreateTestCpu()
        cpu.set_A(0)
        cpu.set_P(0)
        cpu.memory[0x0101] = 0b11000000

        execute_instruction(cpu, opcode=BIT_ABSOLUTE, op2_lo_byte=0x01, op2_hi_byte=0x01)

        self.assertEqual(cpu.negative(), 1)
        self.assertEqual(cpu.overflow(), 1)
        self.assertEqual(cpu.zero(), 1)

    def test_AND_immediate(self):
        cpu = CreateTestCpu()
        cpu.set_A(           0b00010001)
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=AND_IMMEDIATE, op2_lo_byte=0b00010000)

        self.assertEqual(cpu.A(), 0b00010000)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)

    def test_AND_zeropage(self):
        cpu = CreateTestCpu()
        cpu.set_A(           0b00010001)
        cpu.memory[0x11] = 0b00010000
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=AND_ZERO_PAGE, op2_lo_byte=0x11)

        self.assertEqual(cpu.A(), 0b00010000)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)

    def test_AND_zeropage_x(self):
        cpu = CreateTestCpu()
        cpu.set_A(           0b00010001)
        cpu.set_X(0x20)
        cpu.memory[0x31] = 0b00010000
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=AND_ZERO_PAGE_X, op2_lo_byte=0x11)

        self.assertEqual(cpu.A(), 0b00010000)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)

    def test_AND_absolute(self):
        cpu = CreateTestCpu()
        cpu.set_A(           0b00010001)
        cpu.memory[0x0111] = 0b00010000
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=AND_ABSOLUTE, op2_lo_byte=0x11, op2_hi_byte=0x01)

        self.assertEqual(cpu.A(), 0b00010000)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)

    def test_AND_absolute_x(self):
        cpu = CreateTestCpu()
        cpu.set_A(           0b00010001)
        cpu.set_X(0x10)
        cpu.memory[0x0121] = 0b00010000
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=AND_ABSOLUTE_X, op2_lo_byte=0x11, op2_hi_byte=0x01)

        self.assertEqual(cpu.A(), 0b00010000)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)

    def test_AND_absolute_y(self):
        cpu = CreateTestCpu()
        cpu.set_A(           0b00010001)
        cpu.set_Y(0x10)
        cpu.memory[0x0121] = 0b00010000
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=AND_ABSOLUTE_Y, op2_lo_byte=0x11, op2_hi_byte=0x01)

        self.assertEqual(cpu.A(), 0b00010000)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)

    def test_AND_indirect_x(self):
        cpu = CreateTestCpu()
        cpu.set_A(           0b00010001)
        cpu.set_X(0x20)
        cpu.memory[0x30] = 0x34
        cpu.memory[0x31] = 0x12
        cpu.memory[0x1234] = 0b00010000
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=AND_INDIRECT_X, op2_lo_byte=0x10)

        self.assertEqual(cpu.A(), 0b00010000)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)

    def test_AND_indirect_y(self):
        cpu = CreateTestCpu()
        cpu.set_A(                  0b00010001)
        cpu.set_Y(0x20)
        cpu.memory[0x10] = 0x34
        cpu.memory[0x11] = 0x12
        cpu.memory[0x1234 + 0x20] = 0b00010000
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=AND_INDIRECT_Y, op2_lo_byte=0x10)

        self.assertEqual(cpu.A(), 0b00010000)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)

    def test_ORA_absolute(self):
        cpu = CreateTestCpu()
        cpu.set_A(           0b00010001)
        cpu.memory[0x1011] = 0b00010000
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=ORA_ABSOLUTE, op2_lo_byte=0x11, op2_hi_byte=0x10)

        self.assertEqual(cpu.A(), 0b00010001)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)

    def test_ORA_immediate(self):
        cpu = CreateTestCpu()
        cpu.set_A(           0b00010001)
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=ORA_IMMEDIATE, op2_lo_byte=0b00110000)

        self.assertEqual(cpu.A(), 0b00110001)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)

    def test_ORA_zeropage(self):
        cpu = CreateTestCpu()
        cpu.set_A(           0b00010001)
        cpu.memory[0x11] =   0b00110000
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=ORA_ZERO_PAGE, op2_lo_byte=0x11)

        self.assertEqual(cpu.A(), 0b00110001)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)

    def test_ORA_zeropage_x(self):
        cpu = CreateTestCpu()
        cpu.set_A(           0b00010001)
        cpu.set_X(0x20)
        cpu.memory[0x31] =   0b00110000
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=ORA_ZERO_PAGE_X, op2_lo_byte=0x11)

        self.assertEqual(cpu.A(), 0b00110001)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)

    def test_ORA_absolute_x(self):
        cpu = CreateTestCpu()
        cpu.set_A(           0b00010001)
        cpu.set_X(0x10)
        cpu.memory[0x1021] = 0b00010000
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=ORA_ABSOLUTE_X, op2_lo_byte=0x11, op2_hi_byte=0x10)

        self.assertEqual(cpu.A(), 0b00010001)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)

    def test_ORA_absolute_y(self):
        cpu = CreateTestCpu()
        cpu.set_A(           0b00010001)
        cpu.set_Y(0x10)
        cpu.memory[0x1021] = 0b00010000
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=ORA_ABSOLUTE_Y, op2_lo_byte=0x11, op2_hi_byte=0x10)

        self.assertEqual(cpu.A(), 0b00010001)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)

    def test_ORA_indirect_x(self):
        cpu = CreateTestCpu()
        cpu.set_A(           0b00010001)
        cpu.set_X(0x20)
        cpu.memory[0x30] = 0x34
        cpu.memory[0x31] = 0x12
        cpu.memory[0x1234] = 0b00010000
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=ORA_INDIRECT_X, op2_lo_byte=0x10)

        self.assertEqual(cpu.A(), 0b00010001)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)

    def test_ORA_indirect_y(self):
        cpu = CreateTestCpu()
        cpu.set_A(                  0b00010001)
        cpu.set_Y(0x20)
        cpu.memory[0x10] = 0x34
        cpu.memory[0x11] = 0x12
        cpu.memory[0x1234 + 0x20] = 0b00010000
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=ORA_INDIRECT_Y, op2_lo_byte=0x10)

        self.assertEqual(cpu.A(), 0b00010001)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)


    def test_EOR_absolute(self):
        cpu = CreateTestCpu()
        cpu.set_A(           0b00010001)
        cpu.memory[0x1011] = 0b00010000
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=EOR_ABSOLUTE, op2_lo_byte=0x11, op2_hi_byte=0x10)

        self.assertEqual(cpu.A(), 0b00000001)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)

    def test_EOR_immediate(self):
        cpu = CreateTestCpu()
        cpu.set_A(           0b00010001)
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=EOR_IMMEDIATE, op2_lo_byte=0b00110000)

        self.assertEqual(cpu.A(), 0b00100001)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)

    def test_EOR_zeropage(self):
        cpu = CreateTestCpu()
        cpu.set_A(           0b00010001)
        cpu.memory[0x11] =   0b00110000
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=EOR_ZERO_PAGE, op2_lo_byte=0x11)

        self.assertEqual(cpu.A(), 0b00100001)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)

    def test_EOR_zeropage_x(self):
        cpu = CreateTestCpu()
        cpu.set_A(           0b00010001)
        cpu.set_X(0x20)
        cpu.memory[0x31] =   0b00110000
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=EOR_ZERO_PAGE_X, op2_lo_byte=0x11)

        self.assertEqual(cpu.A(), 0b00100001)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)

    def test_EOR_absolute_x(self):
        cpu = CreateTestCpu()
        cpu.set_A(           0b00010001)
        cpu.set_X(0x10)
        cpu.memory[0x1021] = 0b00110000
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=EOR_ABSOLUTE_X, op2_lo_byte=0x11, op2_hi_byte=0x10)

        self.assertEqual(cpu.A(), 0b00100001)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)

    def test_EOR_absolute_y(self):
        cpu = CreateTestCpu()
        cpu.set_A(           0b00010001)
        cpu.set_Y(0x10)
        cpu.memory[0x1021] = 0b00110000
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=EOR_ABSOLUTE_Y, op2_lo_byte=0x11, op2_hi_byte=0x10)

        self.assertEqual(cpu.A(), 0b00100001)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)

    def test_EOR_indirect_x(self):
        cpu = CreateTestCpu()
        cpu.set_A(           0b00010001)
        cpu.set_X(0x20)
        cpu.memory[0x30] = 0x34
        cpu.memory[0x31] = 0x12
        cpu.memory[0x1234] = 0b00110000
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=EOR_INDIRECT_X, op2_lo_byte=0x10)

        self.assertEqual(cpu.A(), 0b00100001)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)

    def test_EOR_indirect_y(self):
        cpu = CreateTestCpu()
        cpu.set_A(                  0b00010001)
        cpu.set_Y(0x20)
        cpu.memory[0x10] = 0x34
        cpu.memory[0x11] = 0x12
        cpu.memory[0x1234 + 0x20] = 0b00110000
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=EOR_INDIRECT_Y, op2_lo_byte=0x10)

        self.assertEqual(cpu.A(), 0b00100001)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)


    def test_ASL_absolute(self):
        cpu = CreateTestCpu()
        cpu.memory[0x1F1E] = 0b11010101
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=ASL_ABSOLUTE, op2_lo_byte=0x1E, op2_hi_byte=0x1F)

        self.assertEqual(cpu.memory[0x1F1E], 0b10101010)
        self.assertEqual(cpu.negative(), 1)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 1)

    def test_LSR_absolute(self):
        cpu = CreateTestCpu()
        cpu.memory[0x1F1E] = 0b11010101
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=LSR_ABSOLUTE, op2_lo_byte=0x1E, op2_hi_byte=0x1F)

        self.assertEqual(cpu.memory[0x1F1E], 0b01101010)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 1)

    def test_ROL_absolute(self):
        cpu = CreateTestCpu()
        cpu.memory[0x1F1E] = 0b11010101
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=ROL_ABSOLUTE, op2_lo_byte=0x1E, op2_hi_byte=0x1F)

        self.assertEqual(cpu.memory[0x1F1E], 0b10101011)
        self.assertEqual(cpu.negative(), 1)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 1)

    def test_ROR_absolute(self):
        cpu = CreateTestCpu()
        cpu.memory[0x1F1E] = 0b11010101
        cpu.set_P(0xFF)

        execute_instruction(cpu, opcode=ROR_ABSOLUTE, op2_lo_byte=0x1E, op2_hi_byte=0x1F)

        self.assertEqual(cpu.memory[0x1F1E], 0b11101010)
        self.assertEqual(cpu.negative(), 1)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 1)

if __name__ == '__main__':
    unittest.main()




