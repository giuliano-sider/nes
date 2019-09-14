import os
import sys
import unittest

sys.path += os.pardir
from nes_cpu_test_utils import CreateTestCpu, execute_instruction
from instructions import BCS

class TestFlowControlInstructions(unittest.TestCase):

    def test_that_BCS_branches_forward_when_carry_set(self):
        cpu = CreateTestCpu()
        cpu.set_carry()
        old_PC = cpu.PC()
        branch_offset = -128
        BCS_INSTRUCTION_LENGTH = 2

        execute_instruction(cpu, opcode=BCS, op2_lo_byte=(branch_offset % 256))

        self.assertEqual(cpu.PC(), old_PC + branch_offset + BCS_INSTRUCTION_LENGTH)

    def test_that_BCS_branches_backward_when_carry_set(self):
        cpu = CreateTestCpu()
        cpu.set_carry()
        old_PC = cpu.PC()
        branch_offset = 127
        BCS_INSTRUCTION_LENGTH = 2

        execute_instruction(cpu, opcode=BCS, op2_lo_byte=(branch_offset % 256))

        self.assertEqual(cpu.PC(), old_PC + branch_offset + BCS_INSTRUCTION_LENGTH)


if __name__ == '__main__':
    unittest.main()




