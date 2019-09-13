import os
import sys
import unittest

sys.path += os.pardir
from nes_cpu_test_utils import CreateTestCpu, execute_instruction
from instructions import LDA_IMMEDIATE, LDA_ZEROPAGE, LDA_ABSOLUTE

class TestLoadStore(unittest.TestCase):

    def test_if_register_a_receives_immediate(self):
        cpu = CreateTestCpu('../bin/brk')
        cpu.clear_carry()
        cpu.set_A(0x03)

        execute_instruction(cpu, opcode=LDA_IMMEDIATE, op2_lo_byte=0x01)
        self.assertEqual(cpu.A(), 0x01)

    def test_if_negative_flag_is_cleared_if_operand_is_between_x00_and_x7f_for_lda_immediate(self):
        cpu = CreateTestCpu('../bin/brk')
        cpu.clear_carry()
        cpu.set_A(0x03)

        execute_instruction(cpu, opcode=LDA_IMMEDIATE, op2_lo_byte=0x01)
        expected_value = 0
        self.assertEqual(expected_value, cpu.negative())

    def test_if_negative_flag_is_not_cleared_if_operand_is_greater_than_x7f_for_lda_immediate(self):
        cpu = CreateTestCpu('../bin/brk')
        cpu.clear_carry()
        cpu.set_A(0x03)

        execute_instruction(cpu, opcode=LDA_IMMEDIATE, op2_lo_byte=0x88)
        expected_value = 1
        self.assertEqual(expected_value, cpu.negative())

    def test_if_zero_flag_is_set_when_operand_is_zero_for_lda_immediate(self):
        cpu = CreateTestCpu('../bin/brk')
        cpu.clear_carry()
        cpu.set_A(0x03)

        execute_instruction(cpu, opcode=LDA_IMMEDIATE, op2_lo_byte=0x00)
        expected_value = 1
        self.assertEqual(expected_value, cpu.zero())

    def test_if_zero_flag_is_not_set_when_operand_is_not_zero_for_lda_immediate(self):
        cpu = CreateTestCpu('../bin/brk')
        cpu.clear_carry()
        cpu.set_A(0x03)

        execute_instruction(cpu, opcode=LDA_IMMEDIATE, op2_lo_byte=0x01)
        expected_value = 0
        self.assertEqual(expected_value, cpu.zero())

    def test_zero_page_lda_for_operand_smaller_or_equals_0xff(self):
        cpu = CreateTestCpu('../bin/brk')
        cpu.clear_carry()
        cpu.set_A(0x03)

        execute_instruction(cpu, opcode=LDA_ZEROPAGE, op2_lo_byte=0xFF)
        expected_value = 0xFF
        self.assertEqual(expected_value, cpu.A())

    # def test_zero_page_lda_for_operand_smaller_or_equals_0xff(self):
    #     cpu = CreateTestCpu('../bin/brk')
    #     cpu.clear_carry()
    #     cpu.set_A(0x03)
    #
    #     execute_instruction(cpu, opcode=LDA_ZEROPAGE, op2_lo_byte=0x100)
    #     #Assert it throws error



if __name__ == '__main__':
    unittest.main()




