import os
import sys
import unittest

sys.path += os.pardir
from nes_cpu_test_utils import CreateTestCpu, execute_instruction
from instructions import (ADC_IMMEDIATE, ADC_ZEROPAGE, ADC_ZEROPAGEX, ADC_ABSOLUTE, ADC_ABSOLUTE_X, ADC_ABSOLUTE_Y, ADC_INDIRECT_X, ADC_INDIRECT_Y )


class TestArithmetic(unittest.TestCase):

    def test_adc_immediate_simple_addition_with_no_flag_setting(self):
        cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x00)


        # ADC #$10
        execute_instruction(cpu, opcode=ADC_IMMEDIATE, op2_lo_byte=0x10)

        self.assertEqual(cpu.A(), 0x10)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.overflow(), 0)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 0)

    def test_adc_zeropage(self):
        cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x00)
        cpu.memory[0x10] = 0x01

        execute_instruction(cpu, opcode=ADC_ZEROPAGE, op2_lo_byte=0x10)

        self.assertEqual(cpu.A(), 0x01)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.overflow(), 0)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 0)

    def test_adc_zeropageX(self):
        cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x00)
        cpu.set_X(0xFF)
        cpu.memory[0x00] = 0x01
        cpu.memory[0x100] = 0x02


        execute_instruction(cpu, opcode=ADC_ZEROPAGEX, op2_lo_byte=0x01)

        self.assertEqual(cpu.A(), 0x01)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.overflow(), 0)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 0)

    def test_adc_absolute(self):
        cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x00)
        cpu.memory[0x1100] = 0x02


        execute_instruction(cpu, opcode=ADC_ABSOLUTE, op2_lo_byte=0x00,  op2_hi_byte=0x11)

        self.assertEqual(cpu.A(), 0x02)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.overflow(), 0)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 0)

    def test_adc_absolute_x(self):
        cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x00)
        cpu.set_X(0x01)
        cpu.memory[0x1101] = 0x02


        execute_instruction(cpu, opcode=ADC_ABSOLUTE_X , op2_lo_byte=0x00,  op2_hi_byte=0x11)

        self.assertEqual(cpu.A(), 0x02)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.overflow(), 0)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 0)

    def test_adc_absolute_y(self):
        cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x00)
        cpu.set_Y(0x01)
        cpu.memory[0x1101] = 0x02


        execute_instruction(cpu, opcode=ADC_ABSOLUTE_Y , op2_lo_byte=0x00,  op2_hi_byte=0x11)

        self.assertEqual(cpu.A(), 0x02)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.overflow(), 0)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 0)

    def test_adc_indirect_x(self):
        cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_X(0x01)
        cpu.memory[0x02] = 0x10
        cpu.memory[0x10] = 0x02


        execute_instruction(cpu, opcode=ADC_INDIRECT_X , op2_lo_byte=0x01 )

        self.assertEqual(cpu.A(), 0x02)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.overflow(), 0)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 0)

    def test_adc_indirect_y(self):
        cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_Y(0x01)
        cpu.memory[0x02] = 0x10
        cpu.memory[0x11] = 0x02


        execute_instruction(cpu, opcode=ADC_INDIRECT_Y , op2_lo_byte=0x02 )

        self.assertEqual(cpu.A(), 0x02)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.overflow(), 0)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 0)


if __name__ == '__main__':
    unittest.main()
