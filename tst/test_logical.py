import os
import sys
import unittest

sys.path += os.pardir
from nes_cpu_test_utils import CreateTestCpu, execute_instruction
from instructions import BIT_ZEROPAGE, BIT_ABSOLUTE

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




if __name__ == '__main__':
    unittest.main()




