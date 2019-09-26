from nes_cpu_utils import is_negative, is_overflow, twos_comp
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



BRK = 0x00
def brk(cpu, logger):
    """In test mode, BRK halts the processor. Normally, BRK generates a software interrupt (IRQ with the Break flag set)."""
    if not cpu.is_test_mode:
        raise NotImplementedError()
    else:
        cpu.set_break()

instructions[BRK] = brk



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

def php(cpu, logger):
    # to be implemented OPCODE 08
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

def plp(cpu, logger):
    # to be implemented OPCODE 28
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

def pha(cpu, logger):
    # to be implemented OPCODE 48
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

def pla(cpu, logger):
    # to be implemented OPCODE 68
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

def dey(cpu, logger):
    # to be implemented OPCODE 88
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

def cpx_immediate(cpu, logger):
    # to be implemented OPCODE <<<something>>
    raise NotImplementedError()

def cpy_immediate(cpu, logger):
    # to be implemented OPCODE c0
    raise NotImplementedError()

def instruction_c2(cpu, logger):
    # to be implemented OPCODE c2
    raise NotImplementedError()

def instruction_c3(cpu, logger):
    # to be implemented OPCODE c3
    raise NotImplementedError()

def cpx_zeropage(cpu, logger):
    # to be implemented OPCODE <<<something>>>
    raise NotImplementedError()

def cpy_zeropage(cpu, logger):
    # to be implemented OPCODE c4
    raise NotImplementedError()

def dec_zeropage(cpu, logger):
    # to be implemented OPCODE c6
    raise NotImplementedError()

def instruction_c7(cpu, logger):
    # to be implemented OPCODE c7
    raise NotImplementedError()

def iny(cpu, logger):
    # to be implemented OPCODE c8
    raise NotImplementedError()

def dex(cpu, logger):
    # to be implemented OPCODE ca
    raise NotImplementedError()

def instruction_cb(cpu, logger):
    # to be implemented OPCODE cb
    raise NotImplementedError()

def cpx_absolute(cpu, logger):
    # to be implemented OPCODE <<<something>>>
    raise NotImplementedError()

def cpy_absolute(cpu, logger):
    # to be implemented OPCODE cc
    raise NotImplementedError()

def dec_absolute(cpu, logger):
    # to be implemented OPCODE ce
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


def dec_zeropage_x(cpu, logger):
    # to be implemented OPCODE d6
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

def dec_absolute_x(cpu, logger):
    # to be implemented OPCODE de
    raise NotImplementedError()

def instruction_df(cpu, logger):
    # to be implemented OPCODE df
    raise NotImplementedError()

def sbs_indirect_x(cpu, logger):
    # to be implemented OPCODE e1
    raise NotImplementedError()

def instruction_e2(cpu, logger):
    # to be implemented OPCODE e2
    raise NotImplementedError()

def instruction_e3(cpu, logger):
    # to be implemented OPCODE e3
    raise NotImplementedError()

def sbc_zeropage(cpu, logger):
    # to be implemented OPCODE e5
    raise NotImplementedError()

def inc_zeropage(cpu, logger):
    # to be implemented OPCODE e6
    raise NotImplementedError()

def instruction_e7(cpu, logger):
    # to be implemented OPCODE e7
    raise NotImplementedError()

def inx(cpu, logger):
    # to be implemented OPCODE e8
    raise NotImplementedError()

def sbc_immediate(cpu, logger):
    # to be implemented OPCODE e9
    raise NotImplementedError()

def nop(cpu, logger):
    # to be implemented OPCODE ea
    raise NotImplementedError()

def instruction_eb(cpu, logger):
    # to be implemented OPCODE eb
    raise NotImplementedError()

def sbc_absolute(cpu, logger):
    # to be implemented OPCODE ed
    raise NotImplementedError()

def inc_absolute(cpu, logger):
    # to be implemented OPCODE ee
    raise NotImplementedError()

def instruction_ef(cpu, logger):
    # to be implemented OPCODE ef
    raise NotImplementedError()

def sbc_indirect_y(cpu, logger):
    # to be implemented OPCODE f1
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

def sbc_zeropage_x(cpu, logger):
    # to be implemented OPCODE f5
    raise NotImplementedError()

def inc_zeropage_x(cpu, logger):
    # to be implemented OPCODE f6
    raise NotImplementedError()

def instruction_f7(cpu, logger):
    # to be implemented OPCODE f7
    raise NotImplementedError()



def sbc_absolute_y(cpu, logger):
    # to be implemented OPCODE f9
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

def sbc_absolute_x(cpu, logger):
    # to be implemented OPCODE fd
    raise NotImplementedError()

def inc_absolute_x(cpu, logger):
    # to be implemented OPCODE fe
    raise NotImplementedError()



instructions[ORA_INDIRECT_X] = ora_indirect_x
instructions[2] = instruction_02
instructions[3] = instruction_03
instructions[4] = instruction_04
instructions[ORA_ZERO_PAGE] = ora_zeropage
instructions[ASL_ZERO_PAGE] = asl_zeropage
instructions[7] = instruction_07
instructions[8] = php
instructions[ORA_IMMEDIATE] = ora_immediate
instructions[ASL_ACCUMULATOR] = asl_accumulator
instructions[11] = instruction_0b
instructions[12] = instruction_0c
instructions[ORA_ABSOLUTE] = ora_absolute
instructions[ASL_ABSOLUTE] = asl_absolute
instructions[15] = instruction_0f
instructions[16] = bpl
instructions[ORA_INDIRECT_Y] = ora_indirect_y
instructions[18] = instruction_12
instructions[19] = instruction_13
instructions[20] = instruction_14
instructions[ORA_ZERO_PAGE_X] = ora_zeropage_x
instructions[ASL_ZERO_PAGE_X] = asl_zeropage_x
instructions[23] = instruction_17
instructions[CLC] = clc
instructions[ORA_ABSOLUTE_Y] = ora_absolute_y
instructions[26] = instruction_1a
instructions[27] = instruction_1b
instructions[28] = instruction_1c
instructions[ORA_ABSOLUTE_X] = ora_absolute_x
instructions[ASL_ABSOLUTE_X] = asl_absolute_x
instructions[31] = instruction_1f
instructions[32] = jsr
instructions[33] = instruction_21
instructions[34] = instruction_22
instructions[35] = instruction_23
instructions[BIT_ZEROPAGE] = bit_zeropage
instructions[37] = instruction_25
instructions[ROL_ZERO_PAGE] = rol_zeropage
instructions[39] = instruction_27
instructions[40] = plp
instructions[41] = instruction_29
instructions[ROL_ACCUMULATOR] = rol_accumulator
instructions[43] = instruction_2b
instructions[BIT_ABSOLUTE] = bit_absolute
instructions[45] = instruction_2d
instructions[ROL_ABSOLUTE] = rol_absolute
instructions[47] = instruction_2f
instructions[48] = bmi
instructions[49] = instruction_31
instructions[50] = instruction_32
instructions[51] = instruction_33
instructions[52] = instruction_34
instructions[53] = instruction_35
instructions[ROL_ZERO_PAGE_X] = rol_zeropage_x
instructions[55] = instruction_37
instructions[SEC] = sec
instructions[57] = instruction_39
instructions[58] = instruction_3a
instructions[59] = instruction_3b
instructions[60] = instruction_3c
instructions[61] = instruction_3d
instructions[ROL_ABSOLUTE_X] = rol_absolute_x
instructions[63] = instruction_3f
instructions[64] = rti
instructions[EOR_INDIRECT_X] = eor_indirect_x
instructions[66] = instruction_42
instructions[67] = instruction_43
instructions[68] = instruction_44
instructions[EOR_ZERO_PAGE] = eor_zeropage
instructions[LSR_ZERO_PAGE] = lsr_zeropage
instructions[71] = instruction_47
instructions[72] = pha
instructions[EOR_IMMEDIATE] = eor_immediate
instructions[LSR_ACCUMULATOR] = lsr_accumulator
instructions[75] = instruction_4b
instructions[76] = jmp_absolute
instructions[EOR_ABSOLUTE] = eor_absolute
instructions[LSR_ABSOLUTE] = lsr_absolute
instructions[79] = instruction_4f
instructions[80] = bvc
instructions[EOR_INDIRECT_Y] = eor_indirect_y
instructions[82] = instruction_52
instructions[83] = instruction_53
instructions[84] = instruction_54
instructions[EOR_ZERO_PAGE_X] = eor_zeropage_x
instructions[LSR_ZERO_PAGE_X] = lsr_zeropage_x
instructions[87] = instruction_57
instructions[CLI] = cli
instructions[EOR_ABSOLUTE_Y] = eor_absolute_y
instructions[90] = instruction_5a
instructions[91] = instruction_5b
instructions[92] = instruction_5c
instructions[EOR_ABSOLUTE_X] = eor_absolute_x
instructions[LSR_ABSOLUTE_X] = lsr_absolute_x
instructions[95] = instruction_5f
instructions[96] = rts
instructions[98] = instruction_62
instructions[99] = instruction_63
instructions[100] = instruction_64
instructions[ROR_ZERO_PAGE] = ror_zeropage
instructions[103] = instruction_67
instructions[104] = pla
instructions[ROR_ACCUMULATOR] = ror_accumulator
instructions[107] = instruction_6b
instructions[108] = jmp_indirect
instructions[ROR_ABSOLUTE] = ror_absolute
instructions[111] = instruction_6f
instructions[112] = bvs
instructions[114] = instruction_72
instructions[115] = instruction_73
instructions[116] = instruction_74
instructions[ROR_ZERO_PAGE_X] = ror_zeropage_x
instructions[119] = instruction_77
instructions[SEI] = sei
instructions[122] = instruction_7a
instructions[123] = instruction_7b
instructions[124] = instruction_7c
instructions[ROR_ABSOLUTE_X] = ror_absolute_x
instructions[127] = instruction_7f
instructions[128] = instruction_80
instructions[129] = sta_indirect_x
instructions[130] = instruction_82
instructions[131] = instruction_83
instructions[132] = sty_zeropage
instructions[133] = sta_zeropage
instructions[134] = stx_zeropage
instructions[135] = instruction_87
instructions[136] = dey
instructions[137] = instruction_89
instructions[TXA] = txa
instructions[139] = instruction_8b
instructions[140] = sty_absolute
instructions[STA_ABSOLUTE] = sta_absolute
instructions[142] = stx_absolute
instructions[143] = instruction_8f
instructions[BCC] = bcc
instructions[145] = sta_indirect_y
instructions[146] = instruction_92
instructions[147] = instruction_93
instructions[148] = sty_zeropage_x
instructions[149] = sta_zeropage_x
instructions[150] = stx_zeropage_y
instructions[151] = instruction_97
instructions[TYA] = tya
instructions[153] = sta_absolute_y
instructions[TXS] = txs
instructions[TYA] = tya
instructions[156] = instruction_9c
instructions[157] = sta_absolute_x
instructions[158] = instruction_9e
instructions[159] = instruction_9f
instructions[160] = ldy_immediate
instructions[LDA_INDIRECT_X] = lda_indirect_x
instructions[162] = ldx_immediate
instructions[163] = instruction_a3
instructions[164] = ldy_zeropage
instructions[LDA_ZEROPAGE] = lda_zeropage
instructions[166] = ldx_zeropage
instructions[167] = instruction_a7
instructions[TAY] = tay
instructions[LDA_IMMEDIATE] = lda_immediate
instructions[TAX] = tax
instructions[171] = instruction_ab
instructions[172] = ldy_absolute
instructions[173] = lda_absolute
instructions[174] = ldx_absolute
instructions[175] = instruction_af
instructions[BCS] = bcs
instructions[LDA_INDIRECT_Y] = lda_indirect_y
instructions[178] = instruction_b2
instructions[179] = instruction_b3
instructions[180] = ldy_zeropage_x
instructions[181] = lda_zeropage_x
instructions[182] = ldx_zeropage_y
instructions[183] = instruction_b7
instructions[CLV] = clv
instructions[185] = lda_absolute_y
instructions[TSX] = tsx
instructions[187] = instruction_bb
instructions[188] = ldy_absolute_x
instructions[189] = lda_absolute_x
instructions[190] = ldx_absolute_y
instructions[191] = instruction_bf
instructions[192] = cpy_immediate
instructions[194] = instruction_c2
instructions[195] = instruction_c3
instructions[196] = cpy_zeropage
instructions[198] = dec_zeropage
instructions[199] = instruction_c7
instructions[200] = iny
instructions[202] = dex
instructions[203] = instruction_cb
instructions[204] = cpy_absolute
instructions[206] = dec_absolute
instructions[207] = instruction_cf
instructions[208] = bne
instructions[210] = instruction_d2
instructions[211] = instruction_d3
instructions[212] = instruction_d4
instructions[214] = dec_zeropage_x
instructions[215] = instruction_d7
instructions[CLD] = cld
instructions[218] = instruction_da
instructions[219] = instruction_db
instructions[220] = instruction_dc
instructions[222] = dec_absolute_x
instructions[223] = instruction_df
instructions[225] = sbs_indirect_x
instructions[226] = instruction_e2
instructions[227] = instruction_e3
instructions[229] = sbc_zeropage
instructions[230] = inc_zeropage
instructions[231] = instruction_e7
instructions[232] = inx
instructions[233] = sbc_immediate
instructions[234] = nop
instructions[235] = instruction_eb
instructions[237] = sbc_absolute
instructions[238] = inc_absolute
instructions[239] = instruction_ef
instructions[240] = beq
instructions[241] = sbc_indirect_y
instructions[242] = instruction_f2
instructions[243] = instruction_f3
instructions[244] = instruction_f4
instructions[245] = sbc_zeropage_x
instructions[246] = inc_zeropage_x
instructions[247] = instruction_f7
instructions[SED] = sed
instructions[249] = sbc_absolute_y
instructions[250] = instruction_fa
instructions[251] = instruction_fb
instructions[252] = instruction_fc
instructions[253] = sbc_absolute_x
instructions[254] = inc_absolute_x

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
CPX_IMMEDIATE = 0xE0
instructions[CPX_IMMEDIATE] = cpx_immediate
CPX_ZEROPAGE = 0xE4
instructions[CPX_ZEROPAGE] = cpx_zeropage
CPX_ABSOLUTE = 0xEC
instructions[CPX_ABSOLUTE] = cpx_absolute



instructions[AND_IMMEDIATE] = and_immediate
instructions[AND_ZERO_PAGE] = and_zeropage
instructions[AND_ZERO_PAGE_X] = and_zeropage_x
instructions[AND_ABSOLUTE] = and_absolute
instructions[AND_ABSOLUTE_X] = and_absolute_x
instructions[AND_ABSOLUTE_Y] = and_absolute_y
instructions[AND_INDIRECT_X] = and_indirect_x
instructions[AND_INDIRECT_Y] = and_indirect_y
