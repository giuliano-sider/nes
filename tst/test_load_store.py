import os
import sys
import unittest

sys.path += os.pardir
from nes_cpu_test_utils import CreateTestCpu, execute_instruction
from instructions import LDA_IMMEDIATE, LDA_ZEROPAGE, LDA_ABSOLUTE, LDA_INDIRECT_Y, LDA_INDIRECT_X

class TestLoadStore(unittest.TestCase):

    def setUp(self):
        self.cpu = CreateTestCpu()
        self.cpu.clear_carry()
        self.cpu.clear_zero()

    def test_if_register_a_receives_immediate(self):
        self.cpu.set_A(0x03)

        execute_instruction(self.cpu, opcode=LDA_IMMEDIATE, op2_lo_byte=0x01)
        self.assertEqual(self.cpu.A(), 0x01)

    def test_if_negative_flag_is_cleared_if_operand_is_between_x00_and_x7f_for_lda_immediate(self):
        self.cpu.set_A(0x03)

        execute_instruction(self.cpu, opcode=LDA_IMMEDIATE, op2_lo_byte=0x01)
        expected_value = 0
        self.assertEqual(expected_value, self.cpu.negative())

    def test_if_negative_flag_is_not_cleared_if_operand_is_greater_than_x7f_for_lda_immediate(self):
        self.cpu.set_A(0x03)

        execute_instruction(self.cpu, opcode=LDA_IMMEDIATE, op2_lo_byte=0x88)
        expected_value = 1
        self.assertEqual(expected_value, self.cpu.negative())

    def test_if_zero_flag_is_set_when_operand_is_zero_for_lda_immediate(self):
        self.cpu.set_A(0x03)

        execute_instruction(self.cpu, opcode=LDA_IMMEDIATE, op2_lo_byte=0x00)
        expected_value = 1
        self.assertEqual(expected_value, self.cpu.zero())

    def test_if_zero_flag_is_not_set_when_operand_is_not_zero_for_lda_immediate(self):
        self.cpu.set_A(0x03)

        execute_instruction(self.cpu, opcode=LDA_IMMEDIATE, op2_lo_byte=0x01)
        expected_value = 0
        self.assertEqual(expected_value, self.cpu.zero())

    def test_zero_page_lda_for_operand_smaller_or_equals_0xff(self):
        storage_address = 0x10
        stored_content = 0x01

        self.cpu.set_A(0x03)
        self.cpu.memory[storage_address] = stored_content

        execute_instruction(self.cpu, opcode=LDA_ZEROPAGE, op2_lo_byte=storage_address)
        expected_value = stored_content
        self.assertEqual(expected_value, self.cpu.A())

    def test_zero_page_when_content_is_zero(self):
        storage_address = 0x10
        stored_content = 0x00

        self.cpu.set_A(0x03)
        self.cpu.memory[storage_address] = stored_content

        execute_instruction(self.cpu, opcode=LDA_ZEROPAGE, op2_lo_byte=storage_address)
        expected_zero_flag_value = 1
        self.assertEqual(expected_zero_flag_value, self.cpu.zero())

    def test_zero_page_when_content_is_negative(self):
        storage_address = 0x10
        stored_content = 0x80

        self.cpu.set_A(0x03)
        self.cpu.memory[storage_address] = stored_content

        execute_instruction(self.cpu, opcode=LDA_ZEROPAGE, op2_lo_byte=storage_address)
        expected_negative_flag_value = 1
        self.assertEqual(expected_negative_flag_value, self.cpu.negative())

    def test_lda_absolute(self):
        storage_address = 0x1100
        stored_content = 0x80
        low_address_part = 0x00
        high_address_part = 0x11
        any_content = 0x03

        self.cpu.set_A(any_content)
        self.cpu.memory[storage_address] = stored_content

        execute_instruction(self.cpu, opcode=LDA_ABSOLUTE, op2_lo_byte=low_address_part, op2_hi_byte=high_address_part)
        expected_stored_value = stored_content
        self.assertEqual(expected_stored_value, self.cpu.A())

    def test_zero_flag_for_lda_absolute_instruction(self):
        storage_address = 0x1100
        stored_content = 0x00
        low_address_part = 0x00
        high_address_part = 0x11
        any_content = 0x03

        self.cpu.set_A(any_content)
        self.cpu.memory[storage_address] = stored_content

        execute_instruction(self.cpu, opcode=LDA_ABSOLUTE, op2_lo_byte=low_address_part, op2_hi_byte=high_address_part)
        expected_zero_flag = 1
        self.assertEqual(expected_zero_flag, self.cpu.zero())

    def test_negative_flag_when_lda_absolute_instruction(self):
        storage_address = 0x1100
        stored_content = 0x80
        low_address_part = 0x00
        high_address_part = 0x11
        any_content = 0x03

        self.cpu.set_A(any_content)
        self.cpu.memory[storage_address] = stored_content

        execute_instruction(self.cpu, opcode=LDA_ABSOLUTE, op2_lo_byte=low_address_part, op2_hi_byte=high_address_part)
        expected_negative_flag = 1
        self.assertEqual(expected_negative_flag, self.cpu.negative())

    def test_lda_indirect_y_without_overflow(self):
        stored_content = 0x77
        zero_page_address = 0x86

        stored_address_in_0x86 = 0x4028
        stored_address_in_0x86_low = 0x28
        stored_address_in_0x86_high = 0x40

        y_value = 0x10
        self.cpu.set_Y(y_value)

        self.cpu.memory[stored_address_in_0x86 + y_value] = stored_content
        self.cpu.memory[zero_page_address] = stored_address_in_0x86_low
        self.cpu.memory[zero_page_address + 1] = stored_address_in_0x86_high

        expected_value = stored_content

        execute_instruction(self.cpu, opcode=LDA_INDIRECT_Y, op2_lo_byte=zero_page_address)

        self.assertEqual(expected_value, self.cpu.A())

    def test_lda_indirect_y_without_overflow_lo_part(self):
        stored_content = 0x77
        zero_page_address = 0x86

        stored_address_in_0x86 = 0x40FF
        stored_address_in_0x86_low = 0xFF
        stored_address_in_0x86_high = 0x40

        y_value = 0x01
        self.cpu.set_Y(y_value)

        self.cpu.memory[stored_address_in_0x86 + y_value] = stored_content
        self.cpu.memory[zero_page_address] = stored_address_in_0x86_low
        self.cpu.memory[zero_page_address + 1] = stored_address_in_0x86_high

        expected_value = stored_content

        execute_instruction(self.cpu, opcode=LDA_INDIRECT_Y, op2_lo_byte=zero_page_address)

        self.assertEqual(expected_value, self.cpu.A())

    def test_lda_indirect_y_without_overflow_hi_part(self):
        stored_content = 0x77
        zero_page_address = 0x86

        stored_address_in_0x86 = 0xFFFF
        stored_address_in_0x86_low = 0xFF
        stored_address_in_0x86_high = 0xFF

        y_value = 0x01
        self.cpu.set_Y(y_value)

        self.cpu.memory[(stored_address_in_0x86 + y_value) % 0x10000] = stored_content
        self.cpu.memory[zero_page_address] = stored_address_in_0x86_low
        self.cpu.memory[zero_page_address + 1] = stored_address_in_0x86_high

        expected_value = stored_content

        execute_instruction(self.cpu, opcode=LDA_INDIRECT_Y, op2_lo_byte=zero_page_address)

        self.assertEqual(expected_value, self.cpu.A())

    def test_lda_indirect_y_set_flag_if_content_is_zero(self):
        stored_content = 0x00
        zero_page_address = 0x86

        stored_address_in_0x86 = 0x4028
        stored_address_in_0x86_low = 0x28
        stored_address_in_0x86_high = 0x40

        y_value = 0x10
        self.cpu.set_Y(y_value)

        self.cpu.memory[stored_address_in_0x86 + y_value] = stored_content
        self.cpu.memory[zero_page_address] = stored_address_in_0x86_low
        self.cpu.memory[zero_page_address + 1] = stored_address_in_0x86_high

        expected_value = 1

        execute_instruction(self.cpu, opcode=LDA_INDIRECT_Y, op2_lo_byte=zero_page_address)

        self.assertEqual(expected_value, self.cpu.zero())

    def test_lda_indirect_y_set_flag_if_content_is_negative(self):
        stored_content = 0x80
        zero_page_address = 0x86

        stored_address_in_0x86 = 0x4028
        stored_address_in_0x86_low = 0x28
        stored_address_in_0x86_high = 0x40

        y_value = 0x10
        self.cpu.set_Y(y_value)

        self.cpu.memory[stored_address_in_0x86 + y_value] = stored_content
        self.cpu.memory[zero_page_address] = stored_address_in_0x86_low
        self.cpu.memory[zero_page_address + 1] = stored_address_in_0x86_high

        expected_value = 1

        execute_instruction(self.cpu, opcode=LDA_INDIRECT_Y, op2_lo_byte=zero_page_address)

        self.assertEqual(expected_value, self.cpu.negative())

    def test_lda_indirect_x_add_value_to_zero_page_address(self):
        stored_content = 0x77
        zero_page_address = 0x86

        indirect_zero_page_address = 0x99
        x_value = 0x01
        resolved_address = indirect_zero_page_address + x_value

        self.cpu.set_X(x_value)
        self.cpu.memory[zero_page_address] = indirect_zero_page_address
        self.cpu.memory[resolved_address] = stored_content
        execute_instruction(self.cpu, opcode=LDA_INDIRECT_X, op2_lo_byte=zero_page_address)

        expected_value = stored_content
        self.assertEqual(expected_value, self.cpu.A())


    def test_lda_indirect_x_add_value_to_zero_page_address_when_content_is_zero(self):
        stored_content = 0x00
        zero_page_address = 0x86

        indirect_zero_page_address = 0x99
        x_value = 0x01
        resolved_address = indirect_zero_page_address + x_value

        self.cpu.set_X(x_value)
        self.cpu.memory[zero_page_address] = indirect_zero_page_address
        self.cpu.memory[resolved_address] = stored_content
        execute_instruction(self.cpu, opcode=LDA_INDIRECT_X, op2_lo_byte=zero_page_address)

        expected_value = 1
        self.assertEqual(expected_value, self.cpu.zero())

    def test_lda_indirect_x_add_value_to_zero_page_address_when_content_is_negative(self):
        stored_content = 0x80
        zero_page_address = 0x86

        indirect_zero_page_address = 0x99
        x_value = 0x01
        resolved_address = indirect_zero_page_address + x_value

        self.cpu.set_X(x_value)
        self.cpu.memory[zero_page_address] = indirect_zero_page_address
        self.cpu.memory[resolved_address] = stored_content
        execute_instruction(self.cpu, opcode=LDA_INDIRECT_X, op2_lo_byte=zero_page_address)

        expected_value = 1
        self.assertEqual(expected_value, self.cpu.negative())

    def test_lda_indirect_x_add_value_to_zero_page_address_when_resolved_address_has_carry(self):
        stored_content = 0x80
        zero_page_address = 0x86

        indirect_zero_page_address = 0xFF
        x_value = 0x01
        resolved_address = (indirect_zero_page_address + x_value) % 0x100

        self.cpu.set_X(x_value)
        self.cpu.memory[zero_page_address] = indirect_zero_page_address
        self.cpu.memory[resolved_address] = stored_content
        execute_instruction(self.cpu, opcode=LDA_INDIRECT_X, op2_lo_byte=zero_page_address)

        expected_value = stored_content
        self.assertEqual(expected_value, self.cpu.A())


    def test_lda_absolute_y_without_overflow(self):
        self.assertEqual(1, 3)
        # zero flag is zero
        # negative flag is zero

    def test_lda_absolute_y_with_overflow(self):
        self.assertEqual(1, 3)
        # zero flag is zero
        # negative flag is zero

    def test_lda_absolute_y_with_content_being_zero(self):
        self.assertEqual(1, 3)
        # zero flag is 1
        # negative flag is 0

    def test_lda_absolute_y_with_content_being_negative(self):
        self.assertEqual(1, 3)
        # zero flag is 0
        # negative flag is 1




if __name__ == '__main__':
    unittest.main()




