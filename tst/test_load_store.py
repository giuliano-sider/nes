import os
import sys
import unittest
from nes_cpu_test_utils import CreateTestCpu, execute_instruction
from instructions import LDA_IMMEDIATE, LDA_ZEROPAGE, LDA_ABSOLUTE, LDA_INDIRECT_Y, LDA_INDIRECT_X, LDA_ABSOLUTE_Y
from instructions import LDA_ABSOLUTE_X, LDA_ZEROPAGE_X, LDX_IMMEDIATE, LDX_ZEROPAGE, LDX_ABSOLUTE, LDY_ABSOLUTE
from instructions import LDY_ZEROPAGE, LDX_ZEROPAGE_Y, LDY_IMMEDIATE, LDY_ZEROPAGE_X, LDY_ABSOLUTE_X

sys.path += os.pardir


class TestLoadStore(unittest.TestCase):

    def setUp(self):
        self.cpu = CreateTestCpu()
        self.cpu.clear_carry()
        self.cpu.clear_zero()

    def test_if_register_a_receives_immediate(self):
        initial_pc = self.cpu.PC()

        execute_instruction(self.cpu, opcode=LDA_IMMEDIATE, op2_lo_byte=0x01)
        expected_pc = initial_pc + 2

        self.assertEqual(self.cpu.A(), 0x01)
        self.assertEqual(self.cpu.PC(), expected_pc)

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

    def test_zero_page_lda(self):
        storage_address = 0x10
        stored_content = 0x01
        initial_pc = self.cpu.PC()

        self.cpu.set_A(0x03)
        self.cpu.memory[storage_address] = stored_content

        execute_instruction(self.cpu, opcode=LDA_ZEROPAGE, op2_lo_byte=storage_address)

        expected_pc = initial_pc + 2
        expected_value = stored_content
        self.assertEqual(expected_value, self.cpu.A())
        self.assertEqual(expected_pc, self.cpu.PC())

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
        initial_pc = self.cpu.PC()

        self.cpu.memory[storage_address] = stored_content

        execute_instruction(self.cpu, opcode=LDA_ABSOLUTE, op2_lo_byte=low_address_part, op2_hi_byte=high_address_part)
        expected_pc = initial_pc + 3
        expected_stored_value = stored_content
        self.assertEqual(expected_stored_value, self.cpu.A())
        self.assertEqual(expected_pc, self.cpu.PC())

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
        initial_pc = self.cpu.PC()

        stored_address_in_0x86 = 0x4028
        stored_address_in_0x86_low = 0x28
        stored_address_in_0x86_high = 0x40

        y_value = 0x10
        self.cpu.set_Y(y_value)

        self.cpu.memory[stored_address_in_0x86 + y_value] = stored_content
        self.cpu.memory[zero_page_address] = stored_address_in_0x86_low
        self.cpu.memory[zero_page_address + 1] = stored_address_in_0x86_high

        expected_value = stored_content
        expected_pc = initial_pc + 2

        execute_instruction(self.cpu, opcode=LDA_INDIRECT_Y, op2_lo_byte=zero_page_address)

        self.assertEqual(expected_value, self.cpu.A())
        self.assertEqual(expected_pc, self.cpu.PC())

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
        initial_pc = self.cpu.PC()

        indirect_zero_page_address = 0x99
        x_value = 0x01
        resolved_address = indirect_zero_page_address + x_value

        self.cpu.set_X(x_value)
        self.cpu.memory[zero_page_address] = indirect_zero_page_address
        self.cpu.memory[resolved_address] = stored_content
        execute_instruction(self.cpu, opcode=LDA_INDIRECT_X, op2_lo_byte=zero_page_address)

        expected_value = stored_content
        expected_pc = initial_pc + 2

        self.assertEqual(expected_value, self.cpu.A())
        self.assertEqual(expected_pc, self.cpu.PC())


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
        stored_content = 0x01
        absolute_address = 0x4028
        absolute_address_low = 0x28
        absolute_address_high = 0x40
        y_value = 0x10
        initial_pc = self.cpu.PC()

        resolved_address = absolute_address + y_value

        self.cpu.set_Y(y_value)
        self.cpu.memory[resolved_address] = stored_content

        execute_instruction(self.cpu,
                            opcode=LDA_ABSOLUTE_Y,
                            op2_lo_byte=absolute_address_low,
                            op2_hi_byte=absolute_address_high)

        expected_value = stored_content
        expected_zero_flag = 0
        expected_negative_flag = 0
        expected_pc = initial_pc + 3
        self.assertEqual(expected_value, self.cpu.A())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())
        self.assertEqual(expected_pc, self.cpu.PC())

    def test_lda_absolute_y_with_overflow(self):
        stored_content = 0x01
        absolute_address_low = 0xFF
        absolute_address_high = 0xFF
        y_value = 0x01

        resolved_address = 0x0000

        self.cpu.set_Y(y_value)
        self.cpu.memory[resolved_address] = stored_content

        execute_instruction(self.cpu,
                            opcode=LDA_ABSOLUTE_Y,
                            op2_lo_byte=absolute_address_low,
                            op2_hi_byte=absolute_address_high)

        expected_value = stored_content
        expected_zero_flag = 0
        expected_negative_flag = 0
        self.assertEqual(expected_value, self.cpu.A())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())

    def test_lda_absolute_y_with_content_being_zero(self):
        stored_content = 0x00
        absolute_address = 0x4028
        absolute_address_low = 0x28
        absolute_address_high = 0x40
        y_value = 0x10

        resolved_address = absolute_address + y_value

        self.cpu.set_Y(y_value)
        self.cpu.memory[resolved_address] = stored_content

        execute_instruction(self.cpu,
                            opcode=LDA_ABSOLUTE_Y,
                            op2_lo_byte=absolute_address_low,
                            op2_hi_byte=absolute_address_high)

        expected_value = stored_content
        expected_zero_flag = 1
        expected_negative_flag = 0
        self.assertEqual(expected_value, self.cpu.A())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())

    def test_lda_absolute_y_with_content_being_negative(self):
        stored_content = 0x80
        absolute_address = 0x4028
        absolute_address_low = 0x28
        absolute_address_high = 0x40
        y_value = 0x10

        resolved_address = absolute_address + y_value

        self.cpu.set_Y(y_value)
        self.cpu.memory[resolved_address] = stored_content

        execute_instruction(self.cpu,
                            opcode=LDA_ABSOLUTE_Y,
                            op2_lo_byte=absolute_address_low,
                            op2_hi_byte=absolute_address_high)

        expected_value = stored_content
        expected_zero_flag = 0
        expected_negative_flag = 1
        self.assertEqual(expected_value, self.cpu.A())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())

    def test_lda_absolute_x_without_overflow(self):
        stored_content = 0x01
        absolute_address = 0x4028
        absolute_address_low = 0x28
        absolute_address_high = 0x40
        x_value = 0x10
        initial_pc = self.cpu.PC()

        resolved_address = absolute_address + x_value

        self.cpu.set_X(x_value)
        self.cpu.memory[resolved_address] = stored_content

        execute_instruction(self.cpu,
                            opcode=LDA_ABSOLUTE_X,
                            op2_lo_byte=absolute_address_low,
                            op2_hi_byte=absolute_address_high)

        expected_value = stored_content
        expected_zero_flag = 0
        expected_negative_flag = 0
        expected_pc = initial_pc + 3
        self.assertEqual(expected_value, self.cpu.A())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())
        self.assertEqual(expected_pc, self.cpu.PC())

    def test_lda_absolute_x_with_overflow(self):
        stored_content = 0x01
        absolute_address_low = 0xFF
        absolute_address_high = 0xFF
        x_value = 0x01

        resolved_address = 0x0000

        self.cpu.set_X(x_value)
        self.cpu.memory[resolved_address] = stored_content

        execute_instruction(self.cpu,
                            opcode=LDA_ABSOLUTE_X,
                            op2_lo_byte=absolute_address_low,
                            op2_hi_byte=absolute_address_high)

        expected_value = stored_content
        expected_zero_flag = 0
        expected_negative_flag = 0
        self.assertEqual(expected_value, self.cpu.A())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())

    def test_lda_absolute_x_with_content_being_zero(self):
        stored_content = 0x00
        absolute_address = 0x4028
        absolute_address_low = 0x28
        absolute_address_high = 0x40
        x_value = 0x10

        resolved_address = absolute_address + x_value

        self.cpu.set_X(x_value)
        self.cpu.memory[resolved_address] = stored_content

        execute_instruction(self.cpu,
                            opcode=LDA_ABSOLUTE_X,
                            op2_lo_byte=absolute_address_low,
                            op2_hi_byte=absolute_address_high)

        expected_value = stored_content
        expected_zero_flag = 1
        expected_negative_flag = 0
        self.assertEqual(expected_value, self.cpu.A())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())

    def test_lda_absolute_x_with_content_being_negative(self):
        stored_content = 0x80
        absolute_address = 0x4028
        absolute_address_low = 0x28
        absolute_address_high = 0x40
        x_value = 0x10

        resolved_address = absolute_address + x_value

        self.cpu.set_X(x_value)
        self.cpu.memory[resolved_address] = stored_content

        execute_instruction(self.cpu,
                            opcode=LDA_ABSOLUTE_X,
                            op2_lo_byte=absolute_address_low,
                            op2_hi_byte=absolute_address_high)

        expected_value = stored_content
        expected_zero_flag = 0
        expected_negative_flag = 1
        self.assertEqual(expected_value, self.cpu.A())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())

    def test_zero_page_x_lda_without_overflow(self):
        storage_address = 0x10
        stored_content = 0x01
        x_value = 0x01
        initial_pc = self.cpu.PC()

        self.cpu.set_X(x_value)
        self.cpu.memory[storage_address + x_value] = stored_content

        execute_instruction(self.cpu, opcode=LDA_ZEROPAGE_X, op2_lo_byte=storage_address)
        expected_value = stored_content
        expected_pc = initial_pc + 2

        self.assertEqual(expected_value, self.cpu.A())
        self.assertEqual(expected_pc, self.cpu.PC())

    def test_zero_page_x_lda_with_overflow(self):
        storage_address = 0xFF
        stored_content = 0x10
        x_value = 0x01

        self.cpu.set_X(x_value)
        self.cpu.memory[0x00] = stored_content

        execute_instruction(self.cpu, opcode=LDA_ZEROPAGE_X, op2_lo_byte=storage_address)
        expected_value = stored_content
        self.assertEqual(expected_value, self.cpu.A())

    def test_zero_page_x_when_content_is_zero(self):
        storage_address = 0x10
        stored_content = 0x00

        self.cpu.memory[storage_address] = stored_content

        execute_instruction(self.cpu, opcode=LDA_ZEROPAGE_X, op2_lo_byte=storage_address)
        expected_zero_flag_value = 1
        self.assertEqual(expected_zero_flag_value, self.cpu.zero())

    def test_zero_page_x_when_content_is_negative(self):
        storage_address = 0x10
        stored_content = 0x80

        self.cpu.set_A(0x03)
        self.cpu.memory[storage_address] = stored_content

        execute_instruction(self.cpu, opcode=LDA_ZEROPAGE_X, op2_lo_byte=storage_address)
        expected_negative_flag_value = 1
        self.assertEqual(expected_negative_flag_value, self.cpu.negative())

    def test_if_register_x_receives_immediate(self):
        stored_content = 0x01
        execute_instruction(self.cpu, opcode=LDX_IMMEDIATE, op2_lo_byte=stored_content)
        expected_value = stored_content
        expected_negative_flag = 0
        expected_zero_flag = 0
        self.assertEqual(expected_value, self.cpu.X())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())

    def test_if_negative_is_set_if_content_is_negative(self):
        stored_content = 0x01
        execute_instruction(self.cpu, opcode=LDX_IMMEDIATE, op2_lo_byte=stored_content)
        expected_value = stored_content
        expected_negative_flag = 0
        expected_zero_flag = 0
        self.assertEqual(expected_value, self.cpu.X())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())

    def test_if_zero_is_set_if_content_is_zero(self):
        stored_content = 0x01
        execute_instruction(self.cpu, opcode=LDX_IMMEDIATE, op2_lo_byte=stored_content)
        expected_value = stored_content
        expected_negative_flag = 0
        expected_zero_flag = 0
        self.assertEqual(expected_value, self.cpu.X())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())

    def test_zero_page_ldx(self):
        storage_address = 0x10
        stored_content = 0x01
        initial_pc = self.cpu.PC()

        self.cpu.memory[storage_address] = stored_content

        execute_instruction(self.cpu, opcode=LDX_ZEROPAGE, op2_lo_byte=storage_address)
        expected_value = stored_content
        expected_negative_flag = 0
        expected_zero_flag = 0
        expected_pc = initial_pc + 2
        self.assertEqual(expected_value, self.cpu.X())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())
        self.assertEqual(expected_pc, self.cpu.PC())

    def test_ldx_zero_page_when_content_is_zero(self):
        storage_address = 0x10
        stored_content = 0x00

        self.cpu.memory[storage_address] = stored_content

        execute_instruction(self.cpu, opcode=LDX_ZEROPAGE, op2_lo_byte=storage_address)
        expected_negative_flag = 0
        expected_zero_flag = 1
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())

    def test_ldx_zero_page_when_content_is_negative(self):
        storage_address = 0x10
        stored_content = 0x80

        self.cpu.memory[storage_address] = stored_content

        execute_instruction(self.cpu, opcode=LDX_ZEROPAGE, op2_lo_byte=storage_address)
        expected_negative_flag = 1
        expected_zero_flag = 0
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())

    def test_ldx_absolute(self):
        storage_address = 0x1100
        stored_content = 0x07
        low_address_part = 0x00
        high_address_part = 0x11
        initial_pc = self.cpu.PC()

        self.cpu.memory[storage_address] = stored_content

        execute_instruction(self.cpu, opcode=LDX_ABSOLUTE, op2_lo_byte=low_address_part, op2_hi_byte=high_address_part)
        expected_value = stored_content
        expected_negative_flag = 0
        expected_zero_flag = 0
        expected_pc = initial_pc + 3

        self.assertEqual(expected_value, self.cpu.X())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())
        self.assertEqual(expected_pc, self.cpu.PC())

    def test_zero_flag_for_ldx_absolute_instruction(self):
        storage_address = 0x1100
        stored_content = 0x00
        low_address_part = 0x00
        high_address_part = 0x11
        any_content = 0x03

        self.cpu.set_A(any_content)
        self.cpu.memory[storage_address] = stored_content

        execute_instruction(self.cpu, opcode=LDX_ABSOLUTE, op2_lo_byte=low_address_part, op2_hi_byte=high_address_part)
        expected_value = stored_content
        expected_negative_flag = 0
        expected_zero_flag = 1
        self.assertEqual(expected_value, self.cpu.X())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())

    def test_negative_flag_when_ldx_absolute_instruction(self):
        storage_address = 0x1100
        stored_content = 0x80
        low_address_part = 0x00
        high_address_part = 0x11
        any_content = 0x03

        self.cpu.set_A(any_content)
        self.cpu.memory[storage_address] = stored_content

        execute_instruction(self.cpu, opcode=LDX_ABSOLUTE, op2_lo_byte=low_address_part, op2_hi_byte=high_address_part)
        expected_value = stored_content
        expected_negative_flag = 1
        expected_zero_flag = 0
        self.assertEqual(expected_value, self.cpu.X())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())

    def test_zero_page_ldy(self):
        storage_address = 0x10
        stored_content = 0x01
        initial_pc = self.cpu.PC()

        self.cpu.memory[storage_address] = stored_content

        execute_instruction(self.cpu, opcode=LDY_ZEROPAGE, op2_lo_byte=storage_address)
        expected_value = stored_content
        expected_negative_flag = 0
        expected_zero_flag = 0
        expected_pc = initial_pc + 2

        self.assertEqual(expected_value, self.cpu.Y())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())
        self.assertEqual(expected_pc, self.cpu.PC())

    def test_ldy_zero_page_when_content_is_zero(self):
        storage_address = 0x10
        stored_content = 0x00

        self.cpu.memory[storage_address] = stored_content

        execute_instruction(self.cpu, opcode=LDY_ZEROPAGE, op2_lo_byte=storage_address)
        expected_negative_flag = 0
        expected_zero_flag = 1
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())

    def test_ldy_zero_page_when_content_is_negative(self):
        storage_address = 0x10
        stored_content = 0x80

        self.cpu.memory[storage_address] = stored_content

        execute_instruction(self.cpu, opcode=LDY_ZEROPAGE, op2_lo_byte=storage_address)
        expected_negative_flag = 1
        expected_zero_flag = 0
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())

    def test_ldy_absolute(self):
        storage_address = 0x1100
        stored_content = 0x07
        low_address_part = 0x00
        high_address_part = 0x11
        initial_pc = self.cpu.PC()

        self.cpu.memory[storage_address] = stored_content

        execute_instruction(self.cpu, opcode=LDY_ABSOLUTE, op2_lo_byte=low_address_part, op2_hi_byte=high_address_part)
        expected_value = stored_content
        expected_negative_flag = 0
        expected_zero_flag = 0
        expected_pc = initial_pc + 3
        self.assertEqual(expected_value, self.cpu.Y())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())
        self.assertEqual(expected_pc, self.cpu.PC())

    def test_zero_flag_for_ldy_absolute_instruction(self):
        storage_address = 0x1100
        stored_content = 0x00
        low_address_part = 0x00
        high_address_part = 0x11
        any_content = 0x03

        self.cpu.set_A(any_content)
        self.cpu.memory[storage_address] = stored_content

        execute_instruction(self.cpu, opcode=LDY_ABSOLUTE, op2_lo_byte=low_address_part, op2_hi_byte=high_address_part)
        expected_value = stored_content
        expected_negative_flag = 0
        expected_zero_flag = 1
        self.assertEqual(expected_value, self.cpu.Y())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())

    def test_negative_flag_when_ldy_absolute_instruction(self):
        storage_address = 0x1100
        stored_content = 0x80
        low_address_part = 0x00
        high_address_part = 0x11
        any_content = 0x03

        self.cpu.set_A(any_content)
        self.cpu.memory[storage_address] = stored_content

        execute_instruction(self.cpu, opcode=LDY_ABSOLUTE, op2_lo_byte=low_address_part, op2_hi_byte=high_address_part)
        expected_value = stored_content
        expected_negative_flag = 1
        expected_zero_flag = 0
        self.assertEqual(expected_value, self.cpu.Y())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())


    def test_ldx_zero_page_y_without_overflow(self):
        storage_address = 0x10
        stored_content = 0x01
        y_value = 0x01
        initial_pc = self.cpu.PC()

        self.cpu.set_Y(y_value)
        self.cpu.memory[storage_address + y_value] = stored_content

        execute_instruction(self.cpu, opcode=LDX_ZEROPAGE_Y, op2_lo_byte=storage_address)
        expected_value = stored_content
        expected_negative_flag = 0
        expected_zero_flag = 0
        expected_pc = initial_pc + 2

        self.assertEqual(expected_value, self.cpu.X())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())
        self.assertEqual(expected_pc, self.cpu.PC())

    def test_ldx_zero_page_y_with_overflow(self):
        storage_address = 0xFF
        stored_content = 0x10
        y_value = 0x01

        self.cpu.set_Y(y_value)
        self.cpu.memory[(storage_address + y_value) % 256] = stored_content

        execute_instruction(self.cpu, opcode=LDX_ZEROPAGE_Y, op2_lo_byte=storage_address)
        expected_value = stored_content
        expected_negative_flag = 0
        expected_zero_flag = 0
        self.assertEqual(expected_value, self.cpu.X())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())

    def test_ldx_zero_page_y_when_content_is_zero(self):
        storage_address = 0x10
        stored_content = 0x00
        y_value = 0x01

        self.cpu.set_Y(y_value)
        self.cpu.memory[storage_address + y_value] = stored_content

        execute_instruction(self.cpu, opcode=LDX_ZEROPAGE_Y, op2_lo_byte=storage_address)
        expected_negative_flag = 0
        expected_zero_flag = 1
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())

    def test_ldx_zero_page_y_when_content_is_negative(self):
        storage_address = 0x10
        stored_content = 0x80
        y_value = 0x01

        self.cpu.set_Y(y_value)
        self.cpu.memory[storage_address + y_value] = stored_content

        execute_instruction(self.cpu, opcode=LDX_ZEROPAGE_Y, op2_lo_byte=storage_address)
        expected_value = stored_content
        expected_negative_flag = 1
        expected_zero_flag = 0
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())

    def test_if_register_y_receives_immediate(self):
        stored_content = 0x01
        execute_instruction(self.cpu, opcode=LDY_IMMEDIATE, op2_lo_byte=stored_content)
        expected_value = stored_content
        expected_negative_flag = 0
        expected_zero_flag = 0
        self.assertEqual(expected_value, self.cpu.Y())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())

    def test_ldy_immediate_sets_negative_if_content_is_negative(self):
        stored_content = 0x01
        execute_instruction(self.cpu, opcode=LDY_IMMEDIATE, op2_lo_byte=stored_content)
        expected_value = stored_content
        expected_negative_flag = 0
        expected_zero_flag = 0
        self.assertEqual(expected_value, self.cpu.Y())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())

    def test_ldy_immediate_sets_zero_if_content_is_zero(self):
        stored_content = 0x01
        execute_instruction(self.cpu, opcode=LDY_IMMEDIATE, op2_lo_byte=stored_content)
        expected_value = stored_content
        expected_negative_flag = 0
        expected_zero_flag = 0
        self.assertEqual(expected_value, self.cpu.Y())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())

    def test_ldy_zero_page_x_without_overflow(self):
        storage_address = 0x10
        stored_content = 0x01
        x_value = 0x01
        initial_pc = self.cpu.PC()

        self.cpu.set_X(x_value)
        self.cpu.memory[storage_address + x_value] = stored_content

        execute_instruction(self.cpu, opcode=LDY_ZEROPAGE_X, op2_lo_byte=storage_address)
        expected_value = stored_content
        expected_pc = initial_pc + 2

        self.assertEqual(expected_value, self.cpu.Y())
        self.assertEqual(expected_pc, self.cpu.PC())

    def test_ldy_zero_page_x_with_overflow(self):
        storage_address = 0xFF
        stored_content = 0x10
        x_value = 0x01

        self.cpu.set_X(x_value)
        self.cpu.memory[0x00] = stored_content

        execute_instruction(self.cpu, opcode=LDY_ZEROPAGE_X, op2_lo_byte=storage_address)
        expected_value = stored_content
        self.assertEqual(expected_value, self.cpu.Y())

    def test_ldy_zero_page_x_when_content_is_zero(self):
        storage_address = 0x10
        stored_content = 0x00

        self.cpu.memory[storage_address] = stored_content

        execute_instruction(self.cpu, opcode=LDY_ZEROPAGE_X, op2_lo_byte=storage_address)
        expected_zero_flag_value = 1
        self.assertEqual(expected_zero_flag_value, self.cpu.zero())

    def test_ldy_zero_page_x_when_content_is_negative(self):
        storage_address = 0x10
        stored_content = 0x80

        self.cpu.memory[storage_address] = stored_content

        execute_instruction(self.cpu, opcode=LDY_ZEROPAGE_X, op2_lo_byte=storage_address)
        expected_negative_flag_value = 1
        self.assertEqual(expected_negative_flag_value, self.cpu.negative())

    def test_ldy_absolute_x_without_overflow(self):
        stored_content = 0x01
        absolute_address = 0x4028
        absolute_address_low = 0x28
        absolute_address_high = 0x40
        x_value = 0x10
        initial_pc = self.cpu.PC()

        resolved_address = absolute_address + x_value

        self.cpu.set_X(x_value)
        self.cpu.memory[resolved_address] = stored_content

        execute_instruction(self.cpu,
                            opcode=LDY_ABSOLUTE_X,
                            op2_lo_byte=absolute_address_low,
                            op2_hi_byte=absolute_address_high)

        expected_value = stored_content
        expected_zero_flag = 0
        expected_negative_flag = 0
        expected_pc = initial_pc + 3
        self.assertEqual(expected_value, self.cpu.Y())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())
        self.assertEqual(expected_pc, self.cpu.PC())

    def test_ldy_absolute_x_with_overflow(self):
        stored_content = 0x01
        absolute_address_low = 0xFF
        absolute_address_high = 0xFF
        x_value = 0x01

        resolved_address = 0x0000

        self.cpu.set_X(x_value)
        self.cpu.memory[resolved_address] = stored_content

        execute_instruction(self.cpu,
                            opcode=LDY_ABSOLUTE_X,
                            op2_lo_byte=absolute_address_low,
                            op2_hi_byte=absolute_address_high)

        expected_value = stored_content
        expected_zero_flag = 0
        expected_negative_flag = 0
        self.assertEqual(expected_value, self.cpu.Y())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())

    def test_ldy_absolute_x_with_content_being_zero(self):
        stored_content = 0x00
        absolute_address = 0x4028
        absolute_address_low = 0x28
        absolute_address_high = 0x40
        x_value = 0x10

        resolved_address = absolute_address + x_value

        self.cpu.set_X(x_value)
        self.cpu.memory[resolved_address] = stored_content

        execute_instruction(self.cpu,
                            opcode=LDY_ABSOLUTE_X,
                            op2_lo_byte=absolute_address_low,
                            op2_hi_byte=absolute_address_high)

        expected_value = stored_content
        expected_zero_flag = 1
        expected_negative_flag = 0
        self.assertEqual(expected_value, self.cpu.Y())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())

    def test_ldy_absolute_x_with_content_being_negative(self):
        stored_content = 0x80
        absolute_address = 0x4028
        absolute_address_low = 0x28
        absolute_address_high = 0x40
        x_value = 0x10

        resolved_address = absolute_address + x_value

        self.cpu.set_X(x_value)
        self.cpu.memory[resolved_address] = stored_content

        execute_instruction(self.cpu,
                            opcode=LDY_ABSOLUTE_X,
                            op2_lo_byte=absolute_address_low,
                            op2_hi_byte=absolute_address_high)

        expected_value = stored_content
        expected_zero_flag = 0
        expected_negative_flag = 1
        self.assertEqual(expected_value, self.cpu.Y())
        self.assertEqual(expected_zero_flag, self.cpu.zero())
        self.assertEqual(expected_negative_flag, self.cpu.negative())

if __name__ == '__main__':
    unittest.main()




