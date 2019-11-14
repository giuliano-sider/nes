import os
import sys
import unittest

sys.path += os.pardir
from nes_cpu_test_utils import CreateTestCpu, execute_instruction
from Instructions.arithmetics_instructions import *
from cpu cimport Cpu

class TestArithmetic(unittest.TestCase):

    def test_adc_immediate_simple_addition_with_no_flag_setting(self):
        cdef Cpu cpu = CreateTestCpu()
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
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x00)
        cpu.set_memory(0x10, 0x01)

        execute_instruction(cpu, opcode=ADC_ZEROPAGE, op2_lo_byte=0x10)

        self.assertEqual(cpu.A(), 0x01)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.overflow(), 0)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 0)

    def test_adc_zeropageX(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x00)
        cpu.set_X(0xFF)
        cpu.set_memory(0x00, 0x01)
        cpu.set_memory(0x100, 0x02)


        execute_instruction(cpu, opcode=ADC_ZEROPAGEX, op2_lo_byte=0x01)

        self.assertEqual(cpu.A(), 0x01)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.overflow(), 0)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 0)
        self.assertEqual(cpu.clock_ticks_since_reset, 4)

    def test_adc_absolute(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x00)
        cpu.set_memory(0x1100, 0x02)


        execute_instruction(cpu, opcode=ADC_ABSOLUTE, op2_lo_byte=0x00,  op2_hi_byte=0x11)

        self.assertEqual(cpu.A(), 0x02)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.overflow(), 0)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 0)

    def test_adc_absolute_x(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x00)
        cpu.set_X(0x01)
        cpu.set_memory(0x1101, 0x02)


        execute_instruction(cpu, opcode=ADC_ABSOLUTE_X , op2_lo_byte=0x00,  op2_hi_byte=0x11)

        self.assertEqual(cpu.A(), 0x02)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.overflow(), 0)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 0)

    def test_adc_absolute_y(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x00)
        cpu.set_Y(0x01)
        cpu.set_memory(0x1101, 0x02)


        execute_instruction(cpu, opcode=ADC_ABSOLUTE_Y , op2_lo_byte=0x00,  op2_hi_byte=0x11)

        self.assertEqual(cpu.A(), 0x02)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.overflow(), 0)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 0)

    def test_adc_indirect_x(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x00)
        cpu.set_X(0x01)
        cpu.set_memory(0x02, 0x00)
        cpu.set_memory(0x03, 0x10)
        cpu.set_memory(0x1000, 0x02)


        execute_instruction(cpu, opcode=ADC_INDIRECT_X , op2_lo_byte=0x01 )

        self.assertEqual(cpu.A(), 0x02)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.overflow(), 0)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 0)

    def test_adc_indirect_y(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x00)
        cpu.set_Y(0x01)
        cpu.set_memory(0x02, 0x00)
        cpu.set_memory(0x03, 0x10)
        cpu.set_memory(0x1001, 0x02)


        execute_instruction(cpu, opcode=ADC_INDIRECT_Y , op2_lo_byte=0x02 )

        self.assertEqual(cpu.A(), 0x02)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.overflow(), 0)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 0)

    def test_cmp_immediate(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x01)

        execute_instruction(cpu, opcode=CMP_IMMEDIATE, op2_lo_byte=0x02)

        self.assertEqual(cpu.A(), 0x01)
        self.assertEqual(cpu.negative(), 1)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 0)

    def test_cmp_zeropage_iqual(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x01)
        cpu.set_memory(0x10, 0x01)

        execute_instruction(cpu, opcode=CMP_ZEROPAGE, op2_lo_byte=0x10)

        self.assertEqual(cpu.A(), 0x01)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 1)
        self.assertEqual(cpu.carry(), 1)

    def test_cmp_zeropage_Abigger(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x01)
        cpu.set_memory(0x10, 0x00)

        execute_instruction(cpu, opcode=CMP_ZEROPAGE, op2_lo_byte=0x10)

        self.assertEqual(cpu.A(), 0x01)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 1)

    def test_cmp_zeropage_Asmaller(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x01)
        cpu.set_memory(0x10, 0x02)

        execute_instruction(cpu, opcode=CMP_ZEROPAGE, op2_lo_byte=0x10)

        self.assertEqual(cpu.A(), 0x01)
        self.assertEqual(cpu.negative(), 1)
        self.assertEqual(cpu.overflow(), 0)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 0)

    def test_cmp_zeropageX_iqual(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x01)
        cpu.set_X(0x01)
        cpu.set_memory(0x11, 0x01)

        execute_instruction(cpu, opcode=CMP_ZEROPAGE_X, op2_lo_byte=0x10)

        self.assertEqual(cpu.A(), 0x01)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 1)
        self.assertEqual(cpu.carry(), 1)

    def test_cmp_zeropageX_Abigger(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x0F)
        cpu.set_X(0x01)
        cpu.set_memory(0x11, 0x01)

        execute_instruction(cpu, opcode=CMP_ZEROPAGE_X, op2_lo_byte=0x10)

        self.assertEqual(cpu.A(), 0x0F)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 1)

    def test_cmp_zeropageX_Asmall(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x02)
        cpu.set_X(0x01)
        cpu.set_memory(0x11, 0x05)

        execute_instruction(cpu, opcode=CMP_ZEROPAGE_X, op2_lo_byte=0x10)

        self.assertEqual(cpu.A(), 0x02)
        self.assertEqual(cpu.negative(), 1)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 0)

    def test_cmp_absolute_iqual(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x01)
        cpu.set_memory(0x1100, 0x01)

        execute_instruction(cpu, opcode=CMP_ABSOLUTE, op2_lo_byte=0x00,  op2_hi_byte=0x11)

        self.assertEqual(cpu.A(), 0x01)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 1)
        self.assertEqual(cpu.carry(), 1)

    def test_cmp_absolute_Abigger(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x02)
        cpu.set_memory(0x1100, 0x01)

        execute_instruction(cpu, opcode=CMP_ABSOLUTE, op2_lo_byte=0x00,  op2_hi_byte=0x11)

        self.assertEqual(cpu.A(), 0x02)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 1)

    def test_cmp_absolute_Asmaller(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x02)
        cpu.set_memory(0x1100, 0x05)

        execute_instruction(cpu, opcode=CMP_ABSOLUTE, op2_lo_byte=0x00,  op2_hi_byte=0x11)

        self.assertEqual(cpu.A(), 0x02)
        self.assertEqual(cpu.negative(), 1)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 0)

    def test_cmp_absolutex_iqual(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x01)
        cpu.set_X(0x01)
        cpu.set_memory(0x1101, 0x01)

        execute_instruction(cpu, opcode=CMP_ABSOLUTE_X, op2_lo_byte=0x00,  op2_hi_byte=0x11)

        self.assertEqual(cpu.A(), 0x01)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 1)
        self.assertEqual(cpu.carry(), 1)

    def test_cmp_absolutex_Asmall(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x01)
        cpu.set_X(0x01)
        cpu.set_memory(0x1101, 0x02)

        execute_instruction(cpu, opcode=CMP_ABSOLUTE_X, op2_lo_byte=0x00,  op2_hi_byte=0x11)

        self.assertEqual(cpu.A(), 0x01)
        self.assertEqual(cpu.negative(), 1)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 0)

    def test_cmp_absolutey_iqual(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x01)
        cpu.set_Y(0x01)
        cpu.set_memory(0x1101, 0x01)

        execute_instruction(cpu, opcode=CMP_ABSOLUTE_Y, op2_lo_byte=0x00,  op2_hi_byte=0x11)

        self.assertEqual(cpu.A(), 0x01)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 1)
        self.assertEqual(cpu.carry(), 1)

    def test_cmp_indirect_x_iqual(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x02)
        cpu.set_X(0x01)
        cpu.set_memory(0x02, 0x00)
        cpu.set_memory(0x03, 0x10)
        cpu.set_memory(0x1000, 0x02)


        execute_instruction(cpu, opcode=CMP_INDIRECT_X , op2_lo_byte=0x01 )

        self.assertEqual(cpu.A(), 0x02)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 1)
        self.assertEqual(cpu.carry(), 1)
        self.assertEqual(cpu.clock_ticks_since_reset, 6)

    def test_cmp_indirect_x_Abig(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x04)
        cpu.set_X(0x01)
        cpu.set_memory(0x02, 0x00)
        cpu.set_memory(0x03, 0x10)
        cpu.set_memory(0x1000, 0x02)


        execute_instruction(cpu, opcode=CMP_INDIRECT_X , op2_lo_byte=0x01 )

        self.assertEqual(cpu.A(), 0x04)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 1)

    def test_cmp_indirect_x_ASmall(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x04)
        cpu.set_X(0x01)
        cpu.set_memory(0x02, 0x00)
        cpu.set_memory(0x03, 0x10)
        cpu.set_memory(0x1000, 0x05)


        execute_instruction(cpu, opcode=CMP_INDIRECT_X , op2_lo_byte=0x01 )

        self.assertEqual(cpu.A(), 0x04)
        self.assertEqual(cpu.negative(), 1)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 0)

    def test_cmp_indirect_y_iqual(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x02)
        cpu.set_Y(0x01)
        cpu.set_memory(0x02, 0x00)
        cpu.set_memory(0x03, 0x10)
        cpu.set_memory(0x1001, 0x02)


        execute_instruction(cpu, opcode=CMP_INDIRECT_Y , op2_lo_byte=0x02 )

        self.assertEqual(cpu.A(), 0x02)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 1)
        self.assertEqual(cpu.carry(), 1)

    def test_cmp_indirect_y_Abig(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x04)
        cpu.set_Y(0x01)
        cpu.set_memory(0x02, 0x00)
        cpu.set_memory(0x03, 0x10)
        cpu.set_memory(0x1001, 0x02)


        execute_instruction(cpu, opcode=CMP_INDIRECT_Y , op2_lo_byte=0x02 )

        self.assertEqual(cpu.A(), 0x04)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 1)

    def test_cmp_indirect_y_Asmall(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_A(0x04)
        cpu.set_Y(0x01)
        cpu.set_memory(0x02, 0x00)
        cpu.set_memory(0x03, 0x10)
        cpu.set_memory(0x1001, 0x07)


        execute_instruction(cpu, opcode=CMP_INDIRECT_Y , op2_lo_byte=0x02 )

        self.assertEqual(cpu.A(), 0x04)
        self.assertEqual(cpu.negative(), 1)
        self.assertEqual(cpu.zero(), 0)
        self.assertEqual(cpu.carry(), 0)

    def test_dec_zeropage(self):
      cdef Cpu cpu = CreateTestCpu()
      cpu.clear_carry()
      cpu.set_memory(0x10, 0x02)

      execute_instruction(cpu, opcode=DEC_ZEROPAGE, op2_lo_byte=0x10)

      self.assertEqual(cpu.memory(0x10) , 0x01)
      self.assertEqual(cpu.negative(), 0)
      self.assertEqual(cpu.zero(), 0)

    def test_dec_zeropage_0(self):
      cdef Cpu cpu = CreateTestCpu()
      cpu.clear_carry()
      cpu.set_memory(0x10, 0x01)

      execute_instruction(cpu, opcode=DEC_ZEROPAGE, op2_lo_byte=0x10)

      self.assertEqual(cpu.memory(0x10) , 0x00)
      self.assertEqual(cpu.negative(), 0)
      self.assertEqual(cpu.zero(), 1)

    def test_dec_zeropage_neg(self):
      cdef Cpu cpu = CreateTestCpu()
      cpu.clear_carry()
      cpu.set_memory(0x10, 0x00)

      execute_instruction(cpu, opcode=DEC_ZEROPAGE, op2_lo_byte=0x10)

      self.assertEqual(cpu.memory(0x10) , 0xFF)
      self.assertEqual(cpu.negative(), 1)
      self.assertEqual(cpu.zero(), 0)

    def test_dec_zeropage_x(self):
      cdef Cpu cpu = CreateTestCpu()
      cpu.clear_carry()
      cpu.set_X(0x01)
      cpu.set_memory(0x11, 0x02)

      execute_instruction(cpu, opcode=DEC_ZEROPAGE_X, op2_lo_byte=0x10)

      self.assertEqual(cpu.memory(0x11) , 0x01)
      self.assertEqual(cpu.negative(), 0)
      self.assertEqual(cpu.zero(), 0)

    def test_dec_absolute(self):
      cdef Cpu cpu = CreateTestCpu()
      cpu.clear_carry()
      cpu.set_memory(0x1100, 0x02)

      execute_instruction(cpu, opcode=DEC_ABSOLUTE, op2_lo_byte=0x00, op2_hi_byte=0x11)

      self.assertEqual(cpu.memory(0x1100), 0x01)
      self.assertEqual(cpu.negative(), 0)
      self.assertEqual(cpu.zero(), 0)
      self.assertEqual(cpu.carry(), 0)

    def test_dec_absolute_x(self):
      cdef Cpu cpu = CreateTestCpu()
      cpu.clear_carry()
      cpu.set_X(1);
      cpu.set_memory(0x1101, 0x02)

      execute_instruction(cpu, opcode=DEC_ABSOLUTE_X, op2_lo_byte=0x00, op2_hi_byte=0x11)

      self.assertEqual(cpu.memory(0x1101), 0x01)
      self.assertEqual(cpu.negative(), 0)
      self.assertEqual(cpu.zero(), 0)
      self.assertEqual(cpu.carry(), 0)

    def test_dex(self):
      cdef Cpu cpu = CreateTestCpu()
      cpu.clear_carry()
      cpu.set_X(0x01);

      execute_instruction(cpu, opcode=DEX)

      self.assertEqual(cpu.X(), 0x00)
      self.assertEqual(cpu.negative(), 0)
      self.assertEqual(cpu.zero(), 1)
      self.assertEqual(cpu.carry(), 0)

    def test_dey(self):
      cdef Cpu cpu = CreateTestCpu()
      cpu.clear_carry()
      cpu.set_Y(0x02);

      execute_instruction(cpu, opcode=DEY)

      self.assertEqual(cpu.Y(), 0x01)
      self.assertEqual(cpu.negative(), 0)
      self.assertEqual(cpu.zero(), 0)
      self.assertEqual(cpu.carry(), 0)

    def test_inc_zeropage(self):
      cdef Cpu cpu = CreateTestCpu()
      cpu.clear_carry()
      cpu.set_memory(0x10, 0x02)

      execute_instruction(cpu, opcode=INC_ZEROPAGE, op2_lo_byte=0x10)

      self.assertEqual(cpu.memory(0x10) , 0x03)
      self.assertEqual(cpu.negative(), 0)
      self.assertEqual(cpu.zero(), 0)

    def test_inc_zeropagex(self):
      cdef Cpu cpu = CreateTestCpu()
      cpu.clear_carry()
      cpu.set_X(1)
      cpu.set_memory(0x11, 0x02)

      execute_instruction(cpu, opcode=INC_ZEROPAGE_X, op2_lo_byte=0x10)

      self.assertEqual(cpu.memory(0x11) , 0x03)
      self.assertEqual(cpu.negative(), 0)
      self.assertEqual(cpu.zero(), 0)

    def test_inc_absolute(self):
      cdef Cpu cpu = CreateTestCpu()
      cpu.clear_carry()
      cpu.set_memory(0x1100, 0x00)

      execute_instruction(cpu, opcode=INC_ABSOLUTE, op2_lo_byte=0x00, op2_hi_byte=0x11)

      self.assertEqual(cpu.memory(0x1100), 0x01)
      self.assertEqual(cpu.negative(), 0)
      self.assertEqual(cpu.zero(), 0)

    def test_inc_absolute_x(self):
      cdef Cpu cpu = CreateTestCpu()
      cpu.clear_carry()
      cpu.set_X(1);
      cpu.set_memory(0x1101, 0x02)

      execute_instruction(cpu, opcode=INC_ABSOLUTE_X, op2_lo_byte=0x00, op2_hi_byte=0x11)

      self.assertEqual(cpu.memory(0x1101), 0x03)
      self.assertEqual(cpu.negative(), 0)
      self.assertEqual(cpu.zero(), 0)

    def test_inx(self):
      cdef Cpu cpu = CreateTestCpu()
      cpu.clear_carry()
      cpu.set_X(0x01)

      execute_instruction(cpu, opcode=INX)

      self.assertEqual(cpu.X(), 0x02)
      self.assertEqual(cpu.negative(), 0)
      self.assertEqual(cpu.zero(), 0)

    def test_INy(self):
      cdef Cpu cpu = CreateTestCpu()
      cpu.clear_carry()
      cpu.set_Y(0x02);

      execute_instruction(cpu, opcode=INY)

      self.assertEqual(cpu.Y(), 0x03)
      self.assertEqual(cpu.negative(), 0)
      self.assertEqual(cpu.zero(), 0)

    def test_sbc_immediate(self):
      cdef Cpu cpu = CreateTestCpu()
      cpu.clear_carry()
      cpu.set_A(0x01)

      # CLC
      # SBC #$01
      execute_instruction(cpu, opcode=SBC_IMMEDIATE, op2_lo_byte=0x01)

      self.assertEqual(cpu.A(), 0xFF)
      self.assertEqual(cpu.negative(), 1)
      self.assertEqual(cpu.overflow(), 0)
      self.assertEqual(cpu.zero(), 0)
      self.assertEqual(cpu.carry(), 0)

    def test_sbc_zeropage(self):
      cdef Cpu cpu = CreateTestCpu()
      cpu.clear_carry()
      cpu.set_A(0x02)
      cpu.set_memory(0x10, 0x01)

      # CLC
      # SBC *(0x10) ; 0x02 - 0x01 - (1 - carry) 
      execute_instruction(cpu, opcode=SBC_ZEROPAGE, op2_lo_byte=0x10)

      self.assertEqual(cpu.A(), 0x00)
      self.assertEqual(cpu.negative(), 0)
      self.assertEqual(cpu.overflow(), 0)
      self.assertEqual(cpu.zero(), 1)
      self.assertEqual(cpu.carry(), 1)

    def test_cpx_immediate(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_X(0x01)

        execute_instruction(cpu, opcode=CPX_IMMEDIATE, op2_lo_byte=0x01)

        self.assertEqual(cpu.X(), 0x01)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 1)
        self.assertEqual(cpu.carry(), 1)

    def test_cpx_zeropage_iqual(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_X(0x01)
        cpu.set_memory(0x10, 0x01)

        execute_instruction(cpu, opcode=CPX_ZEROPAGE, op2_lo_byte=0x10)

        self.assertEqual(cpu.X(), 0x01)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 1)
        self.assertEqual(cpu.carry(), 1)

    def test_cpx_absolute_iqual(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_X(0x01)
        cpu.set_memory(0x1100, 0x01)

        execute_instruction(cpu, opcode=CPX_ABSOLUTE, op2_lo_byte=0x00,  op2_hi_byte=0x11)

        self.assertEqual(cpu.X(), 0x01)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 1)
        self.assertEqual(cpu.carry(), 1)

    def test_cpy_immediate(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_Y(0x01)

        execute_instruction(cpu, opcode=CPY_IMMEDIATE, op2_lo_byte=0x01)

        self.assertEqual(cpu.Y(), 0x01)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 1)
        self.assertEqual(cpu.carry(), 1)

    def test_cpy_zeropage_iqual(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_Y(0x01)
        cpu.set_memory(0x10, 0x01)

        execute_instruction(cpu, opcode=CPY_ZEROPAGE, op2_lo_byte=0x10)

        self.assertEqual(cpu.Y(), 0x01)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 1)
        self.assertEqual(cpu.carry(), 1)

    def test_cpy_absolute_iqual(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.clear_carry()
        cpu.set_Y(0x01)
        cpu.set_memory(0x1100, 0x01)

        execute_instruction(cpu, opcode=CPY_ABSOLUTE, op2_lo_byte=0x00, op2_hi_byte=0x11)

        self.assertEqual(cpu.Y(), 0x01)
        self.assertEqual(cpu.negative(), 0)
        self.assertEqual(cpu.zero(), 1)
        self.assertEqual(cpu.carry(), 1)

if __name__ == '__main__':
    unittest.main()
