from Instructions.arithmetics_instructions import *
from Instructions.load_instructions import *
from Instructions.store_instructions import *
from Instructions.control_flow_instructions import *
from Instructions.logical_instructions import *
from Instructions.misc_instructions import *

def InstructionNotImplemented(*args):
    raise NotImplementedError('Instruction currently unimplemented')

"""Format:
    OPCODE = <opcode number>
    def <function that implements the instruction>:
      <implementation>

    instructions[OPCODE] = <function that implements the instruction>
"""
instructions = 256 * [InstructionNotImplemented]


# Undocumented opcodes:

def instruction_02(cpu, logger):
    # to be implemented OPCODE 02
    raise NotImplementedError()

def instruction_03(cpu, logger):
    # to be implemented OPCODE 03
    raise NotImplementedError()

def instruction_04(cpu, logger):
    # to be implemented OPCODE 04
    raise NotImplementedError()



def instruction_07(cpu, logger):
    # to be implemented OPCODE 07
    raise NotImplementedError()




def instruction_0b(cpu, logger):
    # to be implemented OPCODE 0b
    raise NotImplementedError()

def instruction_0c(cpu, logger):
    # to be implemented OPCODE 0c
    raise NotImplementedError()



def instruction_0f(cpu, logger):
    # to be implemented OPCODE 0f
    raise NotImplementedError()


def instruction_12(cpu, logger):
    # to be implemented OPCODE 12
    raise NotImplementedError()

def instruction_13(cpu, logger):
    # to be implemented OPCODE 13
    raise NotImplementedError()

def instruction_14(cpu, logger):
    # to be implemented OPCODE 14
    raise NotImplementedError()



def instruction_17(cpu, logger):
    # to be implemented OPCODE 17
    raise NotImplementedError()




def instruction_1a(cpu, logger):
    # to be implemented OPCODE 1a
    raise NotImplementedError()

def instruction_1b(cpu, logger):
    # to be implemented OPCODE 1b
    raise NotImplementedError()

def instruction_1c(cpu, logger):
    # to be implemented OPCODE 1c
    raise NotImplementedError()



def instruction_1f(cpu, logger):
    # to be implemented OPCODE 1f
    raise NotImplementedError()

def instruction_21(cpu, logger):
    # to be implemented OPCODE 21
    raise NotImplementedError()

def instruction_22(cpu, logger):
    # to be implemented OPCODE 22
    raise NotImplementedError()

def instruction_23(cpu, logger):
    # to be implemented OPCODE 23
    raise NotImplementedError()

def instruction_25(cpu, logger):
    # to be implemented OPCODE 25
    raise NotImplementedError()


def instruction_27(cpu, logger):
    # to be implemented OPCODE 27
    raise NotImplementedError()


def instruction_29(cpu, logger):
    # to be implemented OPCODE 29
    raise NotImplementedError()


def instruction_2b(cpu, logger):
    # to be implemented OPCODE 2b
    raise NotImplementedError()

def instruction_2d(cpu, logger):
    # to be implemented OPCODE 2d
    raise NotImplementedError()


def instruction_2f(cpu, logger):
    # to be implemented OPCODE 2f
    raise NotImplementedError()

def instruction_31(cpu, logger):
    # to be implemented OPCODE 31
    raise NotImplementedError()

def instruction_32(cpu, logger):
    # to be implemented OPCODE 32
    raise NotImplementedError()

def instruction_33(cpu, logger):
    # to be implemented OPCODE 33
    raise NotImplementedError()

def instruction_34(cpu, logger):
    # to be implemented OPCODE 34
    raise NotImplementedError()

def instruction_35(cpu, logger):
    # to be implemented OPCODE 35
    raise NotImplementedError()


def instruction_37(cpu, logger):
    # to be implemented OPCODE 37
    raise NotImplementedError()



def instruction_39(cpu, logger):
    # to be implemented OPCODE 39
    raise NotImplementedError()

def instruction_3a(cpu, logger):
    # to be implemented OPCODE 3a
    raise NotImplementedError()

def instruction_3b(cpu, logger):
    # to be implemented OPCODE 3b
    raise NotImplementedError()

def instruction_3c(cpu, logger):
    # to be implemented OPCODE 3c
    raise NotImplementedError()

def instruction_3d(cpu, logger):
    # to be implemented OPCODE 3d
    raise NotImplementedError()


def instruction_3f(cpu, logger):
    # to be implemented OPCODE 3f
    raise NotImplementedError()



def instruction_42(cpu, logger):
    # to be implemented OPCODE 42
    raise NotImplementedError()

def instruction_43(cpu, logger):
    # to be implemented OPCODE 43
    raise NotImplementedError()

def instruction_44(cpu, logger):
    # to be implemented OPCODE 44
    raise NotImplementedError()



def instruction_47(cpu, logger):
    # to be implemented OPCODE 47
    raise NotImplementedError()




def instruction_4b(cpu, logger):
    # to be implemented OPCODE 4b
    raise NotImplementedError()



def instruction_4f(cpu, logger):
    # to be implemented OPCODE 4f
    raise NotImplementedError()


def instruction_52(cpu, logger):
    # to be implemented OPCODE 52
    raise NotImplementedError()

def instruction_53(cpu, logger):
    # to be implemented OPCODE 53
    raise NotImplementedError()

def instruction_54(cpu, logger):
    # to be implemented OPCODE 54
    raise NotImplementedError()



def instruction_57(cpu, logger):
    # to be implemented OPCODE 57
    raise NotImplementedError()



def instruction_5a(cpu, logger):
    # to be implemented OPCODE 5a
    raise NotImplementedError()

def instruction_5b(cpu, logger):
    # to be implemented OPCODE 5b
    raise NotImplementedError()

def instruction_5c(cpu, logger):
    # to be implemented OPCODE 5c
    raise NotImplementedError()



def instruction_5f(cpu, logger):
    # to be implemented OPCODE 5f
    raise NotImplementedError()

def instruction_62(cpu, logger):
    # to be implemented OPCODE 62
    raise NotImplementedError()

def instruction_63(cpu, logger):
    # to be implemented OPCODE 63
    raise NotImplementedError()

def instruction_64(cpu, logger):
    # to be implemented OPCODE 64
    raise NotImplementedError()


def instruction_67(cpu, logger):
    # to be implemented OPCODE 67
    raise NotImplementedError()



def instruction_6b(cpu, logger):
    # to be implemented OPCODE 6b
    raise NotImplementedError()


def instruction_6f(cpu, logger):
    # to be implemented OPCODE 6f
    raise NotImplementedError()

def instruction_72(cpu, logger):
    # to be implemented OPCODE 72
    raise NotImplementedError()

def instruction_73(cpu, logger):
    # to be implemented OPCODE 73
    raise NotImplementedError()

def instruction_74(cpu, logger):
    # to be implemented OPCODE 74
    raise NotImplementedError()


def instruction_77(cpu, logger):
    # to be implemented OPCODE 77
    raise NotImplementedError()



def instruction_7a(cpu, logger):
    # to be implemented OPCODE 7a
    raise NotImplementedError()

def instruction_7b(cpu, logger):
    # to be implemented OPCODE 7b
    raise NotImplementedError()

def instruction_7c(cpu, logger):
    # to be implemented OPCODE 7c
    raise NotImplementedError()




def instruction_7f(cpu, logger):
    # to be implemented OPCODE 7f
    raise NotImplementedError()

def instruction_80(cpu, logger):
    # to be implemented OPCODE 80
    raise NotImplementedError()


def instruction_82(cpu, logger):
    # to be implemented OPCODE 82
    raise NotImplementedError()

def instruction_83(cpu, logger):
    # to be implemented OPCODE 83
    raise NotImplementedError()


def instruction_87(cpu, logger):
    # to be implemented OPCODE 87
    raise NotImplementedError()


def instruction_89(cpu, logger):
    # to be implemented OPCODE 89
    raise NotImplementedError()



def instruction_8b(cpu, logger):
    # to be implemented OPCODE 8b
    raise NotImplementedError()


def instruction_8f(cpu, logger):
    # to be implemented OPCODE 8f
    raise NotImplementedError()




def instruction_92(cpu, logger):
    # to be implemented OPCODE 92
    raise NotImplementedError()


def instruction_93(cpu, logger):
    # to be implemented OPCODE 93
    raise NotImplementedError()


def instruction_97(cpu, logger):
    # to be implemented OPCODE 97
    raise NotImplementedError()


def instruction_9c(cpu, logger):
    # to be implemented OPCODE 9c
    raise NotImplementedError()


def instruction_9e(cpu, logger):
    # to be implemented OPCODE 9e
    raise NotImplementedError()

def instruction_9f(cpu, logger):
    # to be implemented OPCODE 9f
    raise NotImplementedError()


def instruction_a3(cpu, logger):
    # to be implemented OPCODE a3
    raise NotImplementedError()


def instruction_a7(cpu, logger):
    # to be implemented OPCODE a7
    raise NotImplementedError()


def instruction_ab(cpu, logger):
    # to be implemented OPCODE ab
    raise NotImplementedError()


def instruction_af(cpu, logger):
    # to be implemented OPCODE af
    raise NotImplementedError()


def instruction_b2(cpu, logger):
    # to be implemented OPCODE b2
    raise NotImplementedError()


def instruction_b3(cpu, logger):
    # to be implemented OPCODE b3
    raise NotImplementedError()


def instruction_b7(cpu, logger):
    # to be implemented OPCODE b7
    raise NotImplementedError()



def instruction_bb(cpu, logger):
    # to be implemented OPCODE bb
    raise NotImplementedError()


def instruction_bf(cpu, logger):
    # to be implemented OPCODE bf
    raise NotImplementedError()


def instruction_c2(cpu, logger):
    # to be implemented OPCODE c2
    raise NotImplementedError()

def instruction_c3(cpu, logger):
    # to be implemented OPCODE c3
    raise NotImplementedError()



def instruction_c7(cpu, logger):
    # to be implemented OPCODE c7
    raise NotImplementedError()


def instruction_cb(cpu, logger):
    # to be implemented OPCODE cb
    raise NotImplementedError()

    raise NotImplementedError()

def instruction_cf(cpu, logger):
    # to be implemented OPCODE cf
    raise NotImplementedError()

def instruction_d2(cpu, logger):
    # to be implemented OPCODE d2
    raise NotImplementedError()

def instruction_d3(cpu, logger):
    # to be implemented OPCODE d3
    raise NotImplementedError()

def instruction_d4(cpu, logger):
    # to be implemented OPCODE d4
    raise NotImplementedError()


def instruction_d7(cpu, logger):
    # to be implemented OPCODE d7
    raise NotImplementedError()



def instruction_da(cpu, logger):
    # to be implemented OPCODE da
    raise NotImplementedError()

def instruction_db(cpu, logger):
    # to be implemented OPCODE db
    raise NotImplementedError()

def instruction_dc(cpu, logger):
    # to be implemented OPCODE dc
    raise NotImplementedError()

def instruction_df(cpu, logger):
    # to be implemented OPCODE df
    raise NotImplementedError()


def instruction_e2(cpu, logger):
    # to be implemented OPCODE e2
    raise NotImplementedError()

def instruction_e3(cpu, logger):
    # to be implemented OPCODE e3
    raise NotImplementedError()



def instruction_e7(cpu, logger):
    # to be implemented OPCODE e7
    raise NotImplementedError()


def instruction_eb(cpu, logger):
    # to be implemented OPCODE eb
    raise NotImplementedError()


def instruction_ef(cpu, logger):
    # to be implemented OPCODE ef
    raise NotImplementedError()


def instruction_f2(cpu, logger):
    # to be implemented OPCODE f2
    raise NotImplementedError()

def instruction_f3(cpu, logger):
    # to be implemented OPCODE f3
    raise NotImplementedError()

def instruction_f4(cpu, logger):
    # to be implemented OPCODE f4
    raise NotImplementedError()



def instruction_f7(cpu, logger):
    # to be implemented OPCODE f7
    raise NotImplementedError()


def instruction_fa(cpu, logger):
    # to be implemented OPCODE fa
    raise NotImplementedError()

def instruction_fb(cpu, logger):
    # to be implemented OPCODE fb
    raise NotImplementedError()

def instruction_fc(cpu, logger):
    # to be implemented OPCODE fc
    raise NotImplementedError()

instructions[2] = instruction_02
instructions[3] = instruction_03
instructions[4] = instruction_04
instructions[7] = instruction_07
instructions[11] = instruction_0b
instructions[12] = instruction_0c
instructions[15] = instruction_0f
instructions[18] = instruction_12
instructions[19] = instruction_13
instructions[20] = instruction_14
instructions[23] = instruction_17
instructions[26] = instruction_1a
instructions[27] = instruction_1b
instructions[28] = instruction_1c
instructions[31] = instruction_1f
instructions[33] = instruction_21
instructions[34] = instruction_22
instructions[35] = instruction_23
instructions[37] = instruction_25
instructions[39] = instruction_27
instructions[41] = instruction_29
instructions[43] = instruction_2b
instructions[45] = instruction_2d
instructions[47] = instruction_2f
instructions[49] = instruction_31
instructions[50] = instruction_32
instructions[51] = instruction_33
instructions[52] = instruction_34
instructions[53] = instruction_35
instructions[55] = instruction_37
instructions[57] = instruction_39
instructions[58] = instruction_3a
instructions[59] = instruction_3b
instructions[60] = instruction_3c
instructions[61] = instruction_3d
instructions[63] = instruction_3f
instructions[66] = instruction_42
instructions[67] = instruction_43
instructions[68] = instruction_44
instructions[71] = instruction_47
instructions[75] = instruction_4b
instructions[79] = instruction_4f
instructions[82] = instruction_52
instructions[83] = instruction_53
instructions[84] = instruction_54
instructions[87] = instruction_57
instructions[90] = instruction_5a
instructions[91] = instruction_5b
instructions[92] = instruction_5c
instructions[95] = instruction_5f
instructions[98] = instruction_62
instructions[99] = instruction_63
instructions[100] = instruction_64
instructions[103] = instruction_67
instructions[107] = instruction_6b
instructions[111] = instruction_6f
instructions[114] = instruction_72
instructions[115] = instruction_73
instructions[116] = instruction_74
instructions[119] = instruction_77
instructions[122] = instruction_7a
instructions[123] = instruction_7b
instructions[124] = instruction_7c
instructions[127] = instruction_7f
instructions[128] = instruction_80
instructions[130] = instruction_82
instructions[131] = instruction_83
instructions[135] = instruction_87
instructions[137] = instruction_89
instructions[139] = instruction_8b
instructions[143] = instruction_8f
instructions[146] = instruction_92
instructions[147] = instruction_93
instructions[151] = instruction_97
instructions[156] = instruction_9c
instructions[158] = instruction_9e
instructions[159] = instruction_9f
instructions[163] = instruction_a3
instructions[167] = instruction_a7
instructions[171] = instruction_ab
instructions[175] = instruction_af
instructions[178] = instruction_b2
instructions[179] = instruction_b3
instructions[183] = instruction_b7
instructions[187] = instruction_bb
instructions[191] = instruction_bf
instructions[194] = instruction_c2
instructions[195] = instruction_c3
instructions[199] = instruction_c7
instructions[203] = instruction_cb
instructions[207] = instruction_cf
instructions[210] = instruction_d2
instructions[211] = instruction_d3
instructions[212] = instruction_d4
instructions[215] = instruction_d7
instructions[218] = instruction_da
instructions[219] = instruction_db
instructions[220] = instruction_dc
instructions[223] = instruction_df
instructions[226] = instruction_e2
instructions[227] = instruction_e3
instructions[231] = instruction_e7
instructions[235] = instruction_eb
instructions[239] = instruction_ef
instructions[242] = instruction_f2
instructions[243] = instruction_f3
instructions[244] = instruction_f4
instructions[247] = instruction_f7
instructions[250] = instruction_fa
instructions[251] = instruction_fb
instructions[252] = instruction_fc

# End of undocumented opcodes.


instructions[STA_INDIRECT_X] = sta_indirect_x
instructions[STY_ZEROPAGE] = sty_zeropage
instructions[STA_ZEROPAGE] = sta_zeropage
instructions[STX_ZEROPAGE] = stx_zeropage
instructions[STY_ABSOLUTE] = sty_absolute
instructions[STA_ABSOLUTE] = sta_absolute
instructions[STX_ABSOLUTE] = stx_absolute
instructions[STA_INDIRECT_Y] = sta_indirect_y
instructions[STY_ZEROPAGE_X] = sty_zeropage_x
instructions[STA_ZEROPAGE_X] = sta_zeropage_x
instructions[STX_ZEROPAGE_Y] = stx_zeropage_y
instructions[STA_ABSOLUTE_Y] = sta_absolute_y
instructions[STA_ABSOLUTE_X] = sta_absolute_x

instructions[LDY_IMMEDIATE] = ldy_immediate
instructions[LDA_INDIRECT_X] = lda_indirect_x
instructions[LDX_IMMEDIATE] = ldx_immediate
instructions[LDY_ZEROPAGE] = ldy_zeropage
instructions[LDA_ZEROPAGE] = lda_zeropage
instructions[LDX_ZEROPAGE] = ldx_zeropage
instructions[LDA_IMMEDIATE] = lda_immediate
instructions[LDY_ABSOLUTE] = ldy_absolute
instructions[LDA_ABSOLUTE] = lda_absolute
instructions[LDX_ABSOLUTE] = ldx_absolute
instructions[LDA_INDIRECT_Y] = lda_indirect_y
instructions[LDY_ZEROPAGE_X] = ldy_zeropage_x
instructions[LDA_ZEROPAGE_X] = lda_zeropage_x
instructions[LDX_ZEROPAGE_Y] = ldx_zeropage_y
instructions[LDA_ABSOLUTE_Y] = lda_absolute_y
instructions[LDY_ABSOLUTE_X] = ldy_absolute_x
instructions[LDA_ABSOLUTE_X] = lda_absolute_x
instructions[LDX_ABSOLUTE_Y] = ldx_absolute_y

instructions[JSR] = jsr
instructions[RTI] = rti
instructions[RTS] = rts
instructions[JMP_ABSOLUTE] = jmp_absolute
instructions[JMP_INDIRECT] = jmp_indirect

instructions[BNE] = bne
instructions[BEQ] = beq
instructions[BCS] = bcs
instructions[BVS] = bvs
instructions[BCC] = bcc
instructions[BVC] = bvc
instructions[BPL] = bpl
instructions[BMI] = bmi

instructions[BRK] = brk

instructions[NOP] = nop

instructions[TAY] = tay
instructions[TYA] = tya

instructions[TXS] = txs
instructions[TSX] = tsx

instructions[TAX] = tax
instructions[TXA] = txa

instructions[SED] = sed
instructions[CLD] = cld

instructions[SEC] = sec
instructions[CLC] = clc

instructions[SEI] = sei
instructions[CLI] = cli

instructions[CLV] = clv

instructions[PHP] = php
instructions[PLP] = plp

instructions[PHA] = pha
instructions[PLA] = pla


instructions[ADC_IMMEDIATE] = adc_immediate
instructions[ADC_ZEROPAGE] = adc_zeropage
instructions[ADC_ZEROPAGEX] = adc_zeropage_x
instructions[ADC_ABSOLUTE] = adc_absolute
instructions[ADC_ABSOLUTE_X] = adc_absolute_x
instructions[ADC_ABSOLUTE_Y] = adc_absolute_y
instructions[ADC_INDIRECT_X] = adc_indirect_x
instructions[ADC_INDIRECT_Y ] = adc_indirect_y

instructions[CMP_IMMEDIATE] = cmp_immediate
instructions[CMP_ZEROPAGE] = cmp_zeropage
instructions[CMP_ZEROPAGE_X] = cmp_zero_page_x
instructions[CMP_INDIRECT_X] = cmp_indirect_x
instructions[CMP_INDIRECT_Y] = cmp_indirect_y
instructions[CMP_ABSOLUTE] = cmp_absolute
instructions[CMP_ABSOLUTE_Y] = cmp_absolute_y
instructions[CMP_ABSOLUTE_X] = cmp_absolute_x

instructions[CPX_IMMEDIATE] = cpx_immediate
instructions[CPX_ZEROPAGE] = cpx_zeropage
instructions[CPX_ABSOLUTE] = cpx_absolute

instructions[CPY_IMMEDIATE] = cpy_immediate
instructions[CPY_ZEROPAGE] = cpy_zeropage
instructions[CPY_ABSOLUTE] = cpy_absolute

instructions[DEC_ZEROPAGE] = dec_zeropage
instructions[DEC_ABSOLUTE] = dec_absolute
instructions[DEC_ZEROPAGE_X] = dec_zeropage_x
instructions[DEC_ABSOLUTE_X] = dec_absolute_x

instructions[DEX] = dex

instructions[DEY] = dey

instructions[INC_ZEROPAGE] = inc_zeropage
instructions[INC_ZEROPAGE_X] = inc_zeropage_x
instructions[INC_ABSOLUTE] = inc_absolute
instructions[INC_ABSOLUTE_X] = inc_absolute_x

instructions[INX] = inx

instructions[INY] = iny

instructions[SBC_ZEROPAGE] = sbc_zeropage
instructions[SBC_IMMEDIATE] = sbc_immediate
instructions[SBC_ABSOLUTE] = sbc_absolute
instructions[SBC_INDIRECT_X] = sbc_indirect_y
instructions[SBC_INDIRECT_Y] = sbc_indirect_x
instructions[SBC_ZEROPAGE_X] = sbc_zeropage_x
instructions[SBC_ABSOLUTE_Y] = sbc_absolute_y
instructions[SBC_ABSOLUTE_X] = sbc_absolute_x


instructions[BIT_ZEROPAGE] = bit_zeropage
instructions[BIT_ABSOLUTE] = bit_absolute

instructions[AND_IMMEDIATE] = and_immediate
instructions[AND_ZERO_PAGE] = and_zeropage
instructions[AND_ZERO_PAGE_X] = and_zeropage_x
instructions[AND_ABSOLUTE] = and_absolute
instructions[AND_ABSOLUTE_X] = and_absolute_x
instructions[AND_ABSOLUTE_Y] = and_absolute_y
instructions[AND_INDIRECT_X] = and_indirect_x
instructions[AND_INDIRECT_Y] = and_indirect_y

instructions[ORA_IMMEDIATE] = ora_immediate
instructions[ORA_ZERO_PAGE] = ora_zeropage
instructions[ORA_ZERO_PAGE_X] = ora_zeropage_x
instructions[ORA_ABSOLUTE] = ora_absolute
instructions[ORA_ABSOLUTE_X] = ora_absolute_x
instructions[ORA_ABSOLUTE_Y] = ora_absolute_y
instructions[ORA_INDIRECT_X] = ora_indirect_x
instructions[ORA_INDIRECT_Y] = ora_indirect_y

instructions[EOR_IMMEDIATE] = eor_immediate
instructions[EOR_ZERO_PAGE] = eor_zeropage
instructions[EOR_ZERO_PAGE_X] = eor_zeropage_x
instructions[EOR_ABSOLUTE] = eor_absolute
instructions[EOR_ABSOLUTE_X] = eor_absolute_x
instructions[EOR_ABSOLUTE_Y] = eor_absolute_y
instructions[EOR_INDIRECT_X] = eor_indirect_x
instructions[EOR_INDIRECT_Y] = eor_indirect_y

instructions[ASL_ACCUMULATOR] = asl_accumulator
instructions[ASL_ZERO_PAGE] = asl_zeropage
instructions[ASL_ZERO_PAGE_X] = asl_zeropage_x
instructions[ASL_ABSOLUTE] = asl_absolute
instructions[ASL_ABSOLUTE_X] = asl_absolute_x

instructions[LSR_ACCUMULATOR] = lsr_accumulator
instructions[LSR_ZERO_PAGE] = lsr_zeropage
instructions[LSR_ZERO_PAGE_X] = lsr_zeropage_x
instructions[LSR_ABSOLUTE] = lsr_absolute
instructions[LSR_ABSOLUTE_X] = lsr_absolute_x

instructions[ROL_ACCUMULATOR] = rol_accumulator
instructions[ROL_ZERO_PAGE] = rol_zeropage
instructions[ROL_ZERO_PAGE_X] = rol_zeropage_x
instructions[ROL_ABSOLUTE] = rol_absolute
instructions[ROL_ABSOLUTE_X] = rol_absolute_x

instructions[ROR_ACCUMULATOR] = ror_accumulator
instructions[ROR_ZERO_PAGE] = ror_zeropage
instructions[ROR_ZERO_PAGE_X] = ror_zeropage_x
instructions[ROR_ABSOLUTE] = ror_absolute
instructions[ROR_ABSOLUTE_X] = ror_absolute_x