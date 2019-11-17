import os
import sys
import unittest

sys.path += os.pardir
from nes_cpu_test_utils import CreateTestCpu, execute_instruction
from cpu cimport Cpu
from instructions import *

class TestMiscInstructions(unittest.TestCase):

    def test_CLC(self):
        cdef Cpu cpu = CreateTestCpu()
        cpu.set_carry()

        execute_instruction(cpu, opcode=CLC)

        self.assertEqual(cpu.carry(), 0)

    def test_that_every_documented_instruction_is_implemented(self):
        cdef Cpu cpu = CreateTestCpu()
        dont_care = 0x06

        self.assertEqual(ADC_IMMEDIATE, 0x69)
        execute_instruction(cpu, opcode=ADC_IMMEDIATE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(ADC_ZEROPAGE, 0x65)
        execute_instruction(cpu, opcode=ADC_ZEROPAGE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(ADC_ZEROPAGEX, 0x75)
        execute_instruction(cpu, opcode=ADC_ZEROPAGEX, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(ADC_ABSOLUTE, 0x6D)
        execute_instruction(cpu, opcode=ADC_ABSOLUTE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(ADC_ABSOLUTE_X, 0x7D)
        execute_instruction(cpu, opcode=ADC_ABSOLUTE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(ADC_ABSOLUTE_Y, 0x79)
        execute_instruction(cpu, opcode=ADC_ABSOLUTE_Y, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(ADC_INDIRECT_X, 0x61)
        execute_instruction(cpu, opcode=ADC_INDIRECT_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(ADC_INDIRECT_Y, 0x71)
        execute_instruction(cpu, opcode=ADC_INDIRECT_Y, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(AND_IMMEDIATE, 0x29)
        execute_instruction(cpu, opcode=AND_IMMEDIATE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(AND_ZERO_PAGE, 0x25)
        execute_instruction(cpu, opcode=AND_ZERO_PAGE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(AND_ZERO_PAGE_X, 0x35)
        execute_instruction(cpu, opcode=AND_ZERO_PAGE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(AND_ABSOLUTE, 0x2D)
        execute_instruction(cpu, opcode=AND_ABSOLUTE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(AND_ABSOLUTE_X, 0x3D)
        execute_instruction(cpu, opcode=AND_ABSOLUTE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(AND_ABSOLUTE_Y, 0x39)
        execute_instruction(cpu, opcode=AND_ABSOLUTE_Y, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(AND_INDIRECT_X, 0x21)
        execute_instruction(cpu, opcode=AND_INDIRECT_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(AND_INDIRECT_Y, 0x31)
        execute_instruction(cpu, opcode=AND_INDIRECT_Y, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(ASL_ACCUMULATOR, 0x0A)
        execute_instruction(cpu, opcode=ASL_ACCUMULATOR, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(ASL_ZERO_PAGE, 0x06)
        execute_instruction(cpu, opcode=ASL_ZERO_PAGE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(ASL_ZERO_PAGE_X, 0x16)
        execute_instruction(cpu, opcode=ASL_ZERO_PAGE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(ASL_ABSOLUTE, 0x0E)
        execute_instruction(cpu, opcode=ASL_ABSOLUTE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(ASL_ABSOLUTE_X, 0x1E)
        execute_instruction(cpu, opcode=ASL_ABSOLUTE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(BIT_ZEROPAGE, 0x24)
        execute_instruction(cpu, opcode=BIT_ZEROPAGE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(BIT_ABSOLUTE, 0x2C)
        execute_instruction(cpu, opcode=BIT_ABSOLUTE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(BPL, 0x10)
        execute_instruction(cpu, opcode=BPL, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(BMI, 0x30)
        execute_instruction(cpu, opcode=BMI, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(BVC, 0x50)
        execute_instruction(cpu, opcode=BVC, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(BVS, 0x70)
        execute_instruction(cpu, opcode=BVS, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(BCC, 0x90)
        execute_instruction(cpu, opcode=BCC, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(BCS, 0xB0)
        execute_instruction(cpu, opcode=BCS, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(BNE, 0xD0)
        execute_instruction(cpu, opcode=BNE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(BEQ, 0xF0)
        execute_instruction(cpu, opcode=BEQ, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(CMP_IMMEDIATE, 0xC9)
        execute_instruction(cpu, opcode=CMP_IMMEDIATE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(CMP_ZEROPAGE, 0xC5)
        execute_instruction(cpu, opcode=CMP_ZEROPAGE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(CMP_ZEROPAGE_X, 0xD5)
        execute_instruction(cpu, opcode=CMP_ZEROPAGE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(CMP_ABSOLUTE, 0xCD)
        execute_instruction(cpu, opcode=CMP_ABSOLUTE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(CMP_ABSOLUTE_X, 0xDD)
        execute_instruction(cpu, opcode=CMP_ABSOLUTE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(CMP_ABSOLUTE_Y, 0xD9)
        execute_instruction(cpu, opcode=CMP_ABSOLUTE_Y, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(CMP_INDIRECT_X, 0xC1)
        execute_instruction(cpu, opcode=CMP_INDIRECT_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(CMP_INDIRECT_Y, 0xD1)
        execute_instruction(cpu, opcode=CMP_INDIRECT_Y, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(CPX_IMMEDIATE, 0xE0)
        execute_instruction(cpu, opcode=CPX_IMMEDIATE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(CPX_ZEROPAGE, 0xE4)
        execute_instruction(cpu, opcode=CPX_ZEROPAGE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(CPX_ABSOLUTE, 0xEC)
        execute_instruction(cpu, opcode=CPX_ABSOLUTE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(CPY_IMMEDIATE, 0xC0)
        execute_instruction(cpu, opcode=CPY_IMMEDIATE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(CPY_ZEROPAGE, 0xC4)
        execute_instruction(cpu, opcode=CPY_ZEROPAGE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(CPY_ABSOLUTE, 0xCC)
        execute_instruction(cpu, opcode=CPY_ABSOLUTE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(DEC_ZEROPAGE, 0xC6)
        execute_instruction(cpu, opcode=DEC_ZEROPAGE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(DEC_ZEROPAGE_X, 0xD6)
        execute_instruction(cpu, opcode=DEC_ZEROPAGE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(DEC_ABSOLUTE, 0xCE)
        execute_instruction(cpu, opcode=DEC_ABSOLUTE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(DEC_ABSOLUTE_X, 0xDE)
        execute_instruction(cpu, opcode=DEC_ABSOLUTE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(EOR_IMMEDIATE, 0x49)
        execute_instruction(cpu, opcode=EOR_IMMEDIATE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(EOR_ZERO_PAGE, 0x45)
        execute_instruction(cpu, opcode=EOR_ZERO_PAGE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(EOR_ZERO_PAGE_X, 0x55)
        execute_instruction(cpu, opcode=EOR_ZERO_PAGE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(EOR_ABSOLUTE, 0x4D)
        execute_instruction(cpu, opcode=EOR_ABSOLUTE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(EOR_ABSOLUTE_X, 0x5D)
        execute_instruction(cpu, opcode=EOR_ABSOLUTE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(EOR_ABSOLUTE_Y, 0x59)
        execute_instruction(cpu, opcode=EOR_ABSOLUTE_Y, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(EOR_INDIRECT_X, 0x41)
        execute_instruction(cpu, opcode=EOR_INDIRECT_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(EOR_INDIRECT_Y, 0x51)
        execute_instruction(cpu, opcode=EOR_INDIRECT_Y, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(INC_ZEROPAGE, 0xE6)
        execute_instruction(cpu, opcode=INC_ZEROPAGE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(INC_ZEROPAGE_X, 0xF6)
        execute_instruction(cpu, opcode=INC_ZEROPAGE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(INC_ABSOLUTE, 0xEE)
        execute_instruction(cpu, opcode=INC_ABSOLUTE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(INC_ABSOLUTE_X, 0xFE)
        execute_instruction(cpu, opcode=INC_ABSOLUTE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(JMP_ABSOLUTE, 0x4C)
        execute_instruction(cpu, opcode=JMP_ABSOLUTE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(JMP_INDIRECT, 0x6C)
        execute_instruction(cpu, opcode=JMP_INDIRECT, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(JSR, 0x20)
        execute_instruction(cpu, opcode=JSR, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(LDA_IMMEDIATE, 0xA9)
        execute_instruction(cpu, opcode=LDA_IMMEDIATE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(LDA_ZEROPAGE, 0xA5)
        execute_instruction(cpu, opcode=LDA_ZEROPAGE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(LDA_ZEROPAGE_X, 0xB5)
        execute_instruction(cpu, opcode=LDA_ZEROPAGE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(LDA_ABSOLUTE, 0xAD)
        execute_instruction(cpu, opcode=LDA_ABSOLUTE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(LDA_ABSOLUTE_X, 0xBD)
        execute_instruction(cpu, opcode=LDA_ABSOLUTE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(LDA_ABSOLUTE_Y, 0xB9)
        execute_instruction(cpu, opcode=LDA_ABSOLUTE_Y, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(LDA_INDIRECT_X, 0xA1)
        execute_instruction(cpu, opcode=LDA_INDIRECT_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(LDA_INDIRECT_Y, 0xB1)
        execute_instruction(cpu, opcode=LDA_INDIRECT_Y, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(LDX_IMMEDIATE, 0xA2)
        execute_instruction(cpu, opcode=LDX_IMMEDIATE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(LDX_ZEROPAGE, 0xA6)
        execute_instruction(cpu, opcode=LDX_ZEROPAGE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(LDX_ZEROPAGE_Y, 0xB6)
        execute_instruction(cpu, opcode=LDX_ZEROPAGE_Y, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(LDX_ABSOLUTE, 0xAE)
        execute_instruction(cpu, opcode=LDX_ABSOLUTE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(LDX_ABSOLUTE_Y, 0xBE)
        execute_instruction(cpu, opcode=LDX_ABSOLUTE_Y, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(LDY_IMMEDIATE, 0xA0)
        execute_instruction(cpu, opcode=LDY_IMMEDIATE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(LDY_ZEROPAGE, 0xA4)
        execute_instruction(cpu, opcode=LDY_ZEROPAGE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(LDY_ZEROPAGE_X, 0xB4)
        execute_instruction(cpu, opcode=LDY_ZEROPAGE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(LDY_ABSOLUTE, 0xAC)
        execute_instruction(cpu, opcode=LDY_ABSOLUTE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(LDY_ABSOLUTE_X, 0xBC)
        execute_instruction(cpu, opcode=LDY_ABSOLUTE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(LSR_ACCUMULATOR, 0x4A)
        execute_instruction(cpu, opcode=LSR_ACCUMULATOR, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(LSR_ZERO_PAGE, 0x46)
        execute_instruction(cpu, opcode=LSR_ZERO_PAGE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(LSR_ZERO_PAGE_X, 0x56)
        execute_instruction(cpu, opcode=LSR_ZERO_PAGE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(LSR_ABSOLUTE, 0x4E)
        execute_instruction(cpu, opcode=LSR_ABSOLUTE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(LSR_ABSOLUTE_X, 0x5E)
        execute_instruction(cpu, opcode=LSR_ABSOLUTE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(NOP, 0xEA)
        execute_instruction(cpu, opcode=NOP, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(ORA_IMMEDIATE, 0x09)
        execute_instruction(cpu, opcode=ORA_IMMEDIATE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(ORA_ZERO_PAGE, 0x05)
        execute_instruction(cpu, opcode=ORA_ZERO_PAGE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(ORA_ZERO_PAGE_X, 0x15)
        execute_instruction(cpu, opcode=ORA_ZERO_PAGE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(ORA_ABSOLUTE, 0x0D)
        execute_instruction(cpu, opcode=ORA_ABSOLUTE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(ORA_ABSOLUTE_X, 0x1D)
        execute_instruction(cpu, opcode=ORA_ABSOLUTE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(ORA_ABSOLUTE_Y, 0x19)
        execute_instruction(cpu, opcode=ORA_ABSOLUTE_Y, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(ORA_INDIRECT_X, 0x01)
        execute_instruction(cpu, opcode=ORA_INDIRECT_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(ORA_INDIRECT_Y, 0x11)
        execute_instruction(cpu, opcode=ORA_INDIRECT_Y, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(ROL_ACCUMULATOR, 0x2A)
        execute_instruction(cpu, opcode=ROL_ACCUMULATOR, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(ROL_ZERO_PAGE, 0x26)
        execute_instruction(cpu, opcode=ROL_ZERO_PAGE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(ROL_ZERO_PAGE_X, 0x36)
        execute_instruction(cpu, opcode=ROL_ZERO_PAGE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(ROL_ABSOLUTE, 0x2E)
        execute_instruction(cpu, opcode=ROL_ABSOLUTE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(ROL_ABSOLUTE_X, 0x3E)
        execute_instruction(cpu, opcode=ROL_ABSOLUTE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(ROR_ACCUMULATOR, 0x6A)
        execute_instruction(cpu, opcode=ROR_ACCUMULATOR, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(ROR_ZERO_PAGE, 0x66)
        execute_instruction(cpu, opcode=ROR_ZERO_PAGE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(ROR_ZERO_PAGE_X, 0x76)
        execute_instruction(cpu, opcode=ROR_ZERO_PAGE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(ROR_ABSOLUTE, 0x6E)
        execute_instruction(cpu, opcode=ROR_ABSOLUTE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(ROR_ABSOLUTE_X, 0x7E)
        execute_instruction(cpu, opcode=ROR_ABSOLUTE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(RTI, 0x40)
        execute_instruction(cpu, opcode=RTI, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(RTS, 0x60)
        execute_instruction(cpu, opcode=RTS, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(SBC_IMMEDIATE, 0xE9)
        execute_instruction(cpu, opcode=SBC_IMMEDIATE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(SBC_ZEROPAGE, 0xE5)
        execute_instruction(cpu, opcode=SBC_ZEROPAGE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(SBC_ZEROPAGE_X, 0xF5)
        execute_instruction(cpu, opcode=SBC_ZEROPAGE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(SBC_ABSOLUTE, 0xED)
        execute_instruction(cpu, opcode=SBC_ABSOLUTE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(SBC_ABSOLUTE_X, 0xFD)
        execute_instruction(cpu, opcode=SBC_ABSOLUTE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(SBC_ABSOLUTE_Y, 0xF9)
        execute_instruction(cpu, opcode=SBC_ABSOLUTE_Y, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(SBC_INDIRECT_X, 0xE1)
        execute_instruction(cpu, opcode=SBC_INDIRECT_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(SBC_INDIRECT_Y, 0xF1)
        execute_instruction(cpu, opcode=SBC_INDIRECT_Y, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(STA_ZEROPAGE, 0x85)
        execute_instruction(cpu, opcode=STA_ZEROPAGE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(STA_ZEROPAGE_X, 0x95)
        execute_instruction(cpu, opcode=STA_ZEROPAGE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(STA_ABSOLUTE, 0x8D)
        execute_instruction(cpu, opcode=STA_ABSOLUTE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(STA_ABSOLUTE_X, 0x9D)
        execute_instruction(cpu, opcode=STA_ABSOLUTE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(STA_ABSOLUTE_Y, 0x99)
        execute_instruction(cpu, opcode=STA_ABSOLUTE_Y, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(STA_INDIRECT_X, 0x81)
        execute_instruction(cpu, opcode=STA_INDIRECT_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(STA_INDIRECT_Y, 0x91)
        execute_instruction(cpu, opcode=STA_INDIRECT_Y, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(STX_ZEROPAGE, 0x86)
        execute_instruction(cpu, opcode=STX_ZEROPAGE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(STX_ZEROPAGE_Y, 0x96)
        execute_instruction(cpu, opcode=STX_ZEROPAGE_Y, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(STX_ABSOLUTE, 0x8E)
        execute_instruction(cpu, opcode=STX_ABSOLUTE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(STY_ZEROPAGE, 0x84)
        execute_instruction(cpu, opcode=STY_ZEROPAGE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(STY_ZEROPAGE_X, 0x94)
        execute_instruction(cpu, opcode=STY_ZEROPAGE_X, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(STY_ABSOLUTE, 0x8C)
        execute_instruction(cpu, opcode=STY_ABSOLUTE, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        # Flag instructions:

        self.assertEqual(CLC, 0x18)
        execute_instruction(cpu, opcode=CLC, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(SEC, 0x38)
        execute_instruction(cpu, opcode=SEC, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(CLI, 0x58)
        execute_instruction(cpu, opcode=CLI, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(SEI, 0x78)
        execute_instruction(cpu, opcode=SEI, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(CLV, 0xB8)
        execute_instruction(cpu, opcode=CLV, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        self.assertEqual(CLD, 0xD8)
        execute_instruction(cpu, opcode=CLD, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(SED, 0xF8)
        execute_instruction(cpu, opcode=SED, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

        # Register instructions:

        self.assertEqual(TAX, 0xAA)
        execute_instruction(cpu, opcode=TAX, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(TXA, 0x8A)
        execute_instruction(cpu, opcode=TXA, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(DEX, 0xCA)
        execute_instruction(cpu, opcode=DEX, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(INX, 0xE8)
        execute_instruction(cpu, opcode=INX, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(TAY, 0xA8)
        execute_instruction(cpu, opcode=TAY, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(TYA, 0x98)
        execute_instruction(cpu, opcode=TYA, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(DEY, 0x88)
        execute_instruction(cpu, opcode=DEY, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(INY, 0xC8)
        execute_instruction(cpu, opcode=INY, op2_lo_byte=dont_care, op2_hi_byte=dont_care)       

        # Stack instructions:

        self.assertEqual(TXS, 0x9A)
        execute_instruction(cpu, opcode=TXS, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(TSX, 0xBA)
        execute_instruction(cpu, opcode=TSX, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(PHA, 0x48)
        execute_instruction(cpu, opcode=PHA, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(PLA, 0x68)
        execute_instruction(cpu, opcode=PLA, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(PHP, 0x08)
        execute_instruction(cpu, opcode=PHP, op2_lo_byte=dont_care, op2_hi_byte=dont_care)
        self.assertEqual(PLP, 0x28)
        execute_instruction(cpu, opcode=PLP, op2_lo_byte=dont_care, op2_hi_byte=dont_care)

if __name__ == '__main__':
    unittest.main()



