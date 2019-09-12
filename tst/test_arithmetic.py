import os
import sys
import unittest

sys.path += os.pardir
from nes_cpu_test_utils import CreateTestCpu, execute_instruction
from instructions import ADC_ZEROPAGE

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
        print('teste', cpu.memory[0x10])

        execute_instruction(cpu, opcode=ADC_ZEROPAGE, op2_lo_byte=0x10)

        self.assertEqual(cpu.A(), 0x01)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.overflow(), 0)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 0)

if __name__ == '__main__':
    unittest.main()
