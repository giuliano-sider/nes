import os
import sys
import unittest

sys.path += os.pardir
from nes_cpu_test_utils import CreateTestCpu, execute_instruction
from instructions import JSR, JMP_INDIRECT
from memory_mapper import MEMORY_SIZE

class TestTrickyCases(unittest.TestCase):

    def test_that_jsr_pushes_addr_of_next_instruction_minus_one_onto_stack(self):
        cpu = CreateTestCpu()
        expected_PC_stack_value = (cpu.PC() + 2) % MEMORY_SIZE

        execute_instruction(cpu, opcode=JSR, op2_lo_byte=0xDC, op2_hi_byte=0xDC)

        stored_PC_lo = cpu.memory[(cpu.SP() + 1) % 256]
        stored_PC_hi = cpu.memory[(cpu.SP() + 2) % 256]
        stored_PC = stored_PC_lo + (stored_PC_hi << 8)
        self.assertEqual(stored_PC, expected_PC_stack_value)

    # TODO: def test_stack_page_wraparound_when_pushing_PC_with_a_jsr(self):

    def test_that_jmp_indirect_addr_wrapsaround_in_the_same_page(self):
        cpu = CreateTestCpu()
        cpu.set_PC(0x200)
        cpu.memory[0x1FF] = 0x34
        cpu.memory[0x200] = 0x56 # wrong high byte
        cpu.memory[0x100] = 0x12 # correct high byte

        execute_instruction(cpu, opcode=JMP_INDIRECT, op2_lo_byte=0xFF, op2_hi_byte=0x01)

        self.assertEqual(cpu.PC(), 0x1234)

if __name__ == '__main__':
    unittest.main()
