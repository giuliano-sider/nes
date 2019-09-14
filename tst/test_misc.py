import os
import sys
import unittest

sys.path += os.pardir
from nes_cpu_test_utils import CreateTestCpu, execute_instruction
from instructions import CLC

class TestMiscInstructions(unittest.TestCase):

    def test_CLC(self):
        cpu = CreateTestCpu()
        cpu.set_carry()

        execute_instruction(cpu, opcode=CLC)

        self.assertEqual(cpu.carry(), 0)




if __name__ == '__main__':
    unittest.main()




