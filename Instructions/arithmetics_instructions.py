from nes_cpu_utils import is_negative, is_adc_overflow, is_sbc_overflow, twos_comp
from Instructions.address_getters import *

ADC_IMMEDIATE = 0x69
def adc_immediate(cpu, logger):
    op1 = cpu.A()
    op2 = get_immediate(cpu)
    result = cpu.A() + op2 + cpu.carry()
    cpu.set_A(result)

    cpu.set_negative_iff(is_negative(cpu.A()))
    cpu.set_overflow_iff(is_adc_overflow(op1, op2, cpu.A()))
    cpu.set_zero_iff(cpu.A() == 0)
    cpu.set_carry_iff(result >= 256)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

ADC_ZEROPAGE = 0x65
def adc_zeropage(cpu, logger):
    addr = get_zeropage_addr(cpu)
    adc(cpu, logger, addr)
    cpu.clock_ticks_since_reset += 3

ADC_ZEROPAGEX = 0x75
def adc_zeropage_x(cpu, logger):
    addr = get_zeropage_x_addr(cpu)
    adc(cpu, logger, addr)
    cpu.clock_ticks_since_reset += 4

ADC_ABSOLUTE = 0x6D
def adc_absolute(cpu, logger):
    addr = get_absolute_addr(cpu)
    adc(cpu, logger, addr)
    cpu.clock_ticks_since_reset += 4

ADC_ABSOLUTE_X = 0x7D
def adc_absolute_x(cpu, logger):
    addr, pageCrossed = get_absolute_x_addr(cpu)
    cpu.clock_ticks_since_reset += 4 + pageCrossed
    adc(cpu, logger, addr)

ADC_ABSOLUTE_Y = 0x79
def adc_absolute_y(cpu, logger):
    addr, pageCrossed = get_absolute_y_addr(cpu)
    cpu.clock_ticks_since_reset += 4 + pageCrossed
    adc(cpu, logger, addr)

ADC_INDIRECT_X = 0x61
def adc_indirect_x(cpu, logger):
    addr = get_indirect_x_addr(cpu)
    cpu.clock_ticks_since_reset += 6
    adc(cpu, logger, addr)

ADC_INDIRECT_Y = 0x71
def adc_indirect_y(cpu, logger):
    addr, pageCrossed = get_indirect_y_addr(cpu)
    cpu.clock_ticks_since_reset += 5 + pageCrossed
    adc(cpu, logger, addr)

def adc(cpu, logger, addr):
    op2 = cpu.memory[addr]
    op1 = cpu.A()
    result = cpu.A() + op2 + cpu.carry()
    cpu.set_A(result)

    cpu.set_negative_iff(is_negative(cpu.A()))
    cpu.set_overflow_iff(is_adc_overflow(op1, op2, cpu.A()))
    cpu.set_zero_iff(cpu.A() == 0)
    cpu.set_carry_iff(result >= 256)

    logger.log_memory_access_instruction(cpu, addr, op2)

CMP_IMMEDIATE = 0xC9
def cmp_immediate(cpu, logger):
    op1 = cpu.A()
    op2 = get_immediate(cpu)
    result = (op1 - op2) % 256  # Perform 2 complement subtraction
    cpu.set_zero_iff(op1 == op2)
    cpu.set_carry_iff(op1 >= op2)
    cpu.set_negative_iff(is_negative(result))
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

CMP_ZEROPAGE = 0xC5
def cmp_zeropage(cpu, logger):
    op1 = cpu.A()
    op2 = get_zeropage_addr(cpu)
    cpu.clock_ticks_since_reset += 3
    cmp(cpu, logger, op1, op2)


CMP_ZEROPAGE_X = 0xD5
def cmp_zero_page_x(cpu, logger):
    op1 = cpu.A()
    op2 = get_zeropage_x_addr(cpu)
    cpu.clock_ticks_since_reset += 4
    cmp(cpu, logger, op1, op2)

CMP_ABSOLUTE = 0xCD
def cmp_absolute(cpu, logger):
    op1 = cpu.A()
    op2 = get_absolute_addr(cpu)
    cpu.clock_ticks_since_reset += 4
    cmp(cpu, logger, op1, op2)


CMP_ABSOLUTE_X = 0xDD
def cmp_absolute_x(cpu, logger):
    op1 = cpu.A()
    op2, pageCrossed = get_absolute_x_addr(cpu)
    cpu.clock_ticks_since_reset += 4 + pageCrossed
    cmp(cpu, logger, op1, op2)

CMP_ABSOLUTE_Y = 0xD9
def cmp_absolute_y(cpu, logger):
    op1 = cpu.A()
    op2, pageCrossed = get_absolute_y_addr(cpu)
    cpu.clock_ticks_since_reset += 4 + pageCrossed
    cmp(cpu, logger, op1, op2)

CMP_INDIRECT_X = 0xC1
def cmp_indirect_x(cpu, logger):
    op1 = cpu.A()
    op2 = get_indirect_x_addr(cpu)
    cpu.clock_ticks_since_reset += 6
    cmp(cpu, logger, op1, op2)

CMP_INDIRECT_Y = 0xD1
def cmp_indirect_y(cpu, logger):
    op1 = cpu.A()
    op2, pageCrossed = get_indirect_y_addr(cpu)
    cpu.clock_ticks_since_reset += 5 + pageCrossed
    cmp(cpu, logger, op1, op2)

CPX_IMMEDIATE = 0xE0
def cpx_immediate(cpu, logger):
    op1 = cpu.X()
    op2 = get_immediate(cpu)
    result = (op1 - op2) % 256  # Perform 2 complement subtraction
    cpu.set_zero_iff(op1 == op2)
    cpu.set_carry_iff(op1 >= op2)
    cpu.set_negative_iff(is_negative(result))
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

CPX_ZEROPAGE = 0xE4
def cpx_zeropage(cpu, logger):
    op1 = cpu.X()
    op2 = get_zeropage_addr(cpu)
    cpu.clock_ticks_since_reset += 3
    cmp(cpu, logger, op1, op2)

CPX_ABSOLUTE = 0xEC
def cpx_absolute(cpu, logger):
    op1 = cpu.X()
    op2 = get_absolute_addr(cpu)
    cpu.clock_ticks_since_reset += 4
    cmp(cpu, logger, op1, op2)

CPY_IMMEDIATE = 0xC0
def cpy_immediate(cpu, logger):
    op1 = cpu.Y()
    op2 = get_immediate(cpu)
    result = (op1 - op2) % 256  # Perform 2 complement subtraction
    cpu.set_zero_iff(op1 == op2)
    cpu.set_carry_iff(op1 >= op2)
    cpu.set_negative_iff(is_negative(result))
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

CPY_ZEROPAGE = 0xC4
def cpy_zeropage(cpu, logger):
    op1 = cpu.Y()
    op2 = get_zeropage_addr(cpu)
    cpu.clock_ticks_since_reset += 3
    cmp(cpu, logger, op1, op2)

CPY_ABSOLUTE = 0xCC
def cpy_absolute(cpu, logger):
    op1 = cpu.Y()
    op2 = get_absolute_addr(cpu)
    cpu.clock_ticks_since_reset += 4
    cmp(cpu, logger, op1, op2)

def cmp(cpu, logger, op1, addr):
    op2 = cpu.memory[addr]
    result = (op1-op2) % 256  #Perform 2 complement subtraction
    cpu.set_zero_iff(op1 == op2)
    cpu.set_carry_iff(op1 >= op2)
    cpu.set_negative_iff(is_negative(result))
    logger.log_memory_access_instruction(cpu, addr, op2)

DEC_ZEROPAGE = 0XC6
def dec_zeropage(cpu, logger):
    addr = get_zeropage_addr(cpu)
    cpu.clock_ticks_since_reset += 5
    dec(cpu, logger, addr)

DEC_ZEROPAGE_X = 0xD6
def dec_zeropage_x(cpu, logger):
  addr = get_zeropage_x_addr(cpu)
  cpu.clock_ticks_since_reset += 6
  dec(cpu, logger, addr)

DEC_ABSOLUTE = 0xCE
def dec_absolute(cpu, logger):
  addr = get_absolute_addr(cpu)
  cpu.clock_ticks_since_reset += 6
  dec(cpu, logger, addr)

DEC_ABSOLUTE_X = 0xDE
def dec_absolute_x(cpu, logger):
  addr, pageCrossed = get_absolute_x_addr(cpu)
  cpu.clock_ticks_since_reset += 7
  dec(cpu, logger, addr)

DEX = 0xCA
def dex(cpu, logger):
    result = (cpu.X() - 1) % 256
    cpu.set_X(result)
    cpu.set_zero_iff(result == 0)
    cpu.set_negative_iff(is_negative(result))
    cpu.clock_ticks_since_reset += 2
    cpu.set_PC(cpu.PC() + 1)
    logger.log_instruction(cpu)

DEY = 0x88
def dey(cpu, logger):
  result = (cpu.Y() - 1) % 256
  cpu.set_Y(result)
  cpu.set_zero_iff(result == 0)
  cpu.set_negative_iff(is_negative(result))
  cpu.clock_ticks_since_reset += 2
  cpu.set_PC(cpu.PC() + 1)
  logger.log_instruction(cpu)


def dec(cpu, logger, addr):
  result =   (cpu.memory[addr] - 1) % 256
  cpu.memory[addr] = result
  cpu.set_zero_iff(result == 0)
  cpu.set_negative_iff(is_negative(result))
  logger.log_memory_access_instruction(cpu, addr, cpu.memory[addr])


INC_ZEROPAGE = 0xE6
def inc_zeropage(cpu, logger):
  addr = get_zeropage_addr(cpu)
  cpu.clock_ticks_since_reset += 5
  inc(cpu, logger, addr)

INC_ZEROPAGE_X = 0xF6
def inc_zeropage_x(cpu, logger):
  addr = get_zeropage_x_addr(cpu)
  cpu.clock_ticks_since_reset += 6
  inc(cpu, logger, addr)

INC_ABSOLUTE = 0xEE
def inc_absolute(cpu, logger):
  addr = get_absolute_addr(cpu)
  cpu.clock_ticks_since_reset += 6
  inc(cpu, logger, addr)

INC_ABSOLUTE_X = 0xFE
def inc_absolute_x(cpu, logger):
  addr, pageCrossed = get_absolute_x_addr(cpu)
  cpu.clock_ticks_since_reset += 7
  inc(cpu, logger, addr)

INX = 0xE8
def inx(cpu, logger):
  result = (cpu.X() + 1) % 256
  cpu.set_X(result)
  cpu.set_zero_iff(result == 0)
  cpu.set_negative_iff(is_negative(result))
  cpu.set_PC(cpu.PC() + 1)
  cpu.clock_ticks_since_reset += 2
  logger.log_instruction(cpu)

INY = 0xC8
def iny(cpu, logger):
  result = (cpu.Y() + 1) % 256
  cpu.set_Y(result)
  cpu.set_zero_iff(result == 0)
  cpu.set_negative_iff(is_negative(result))
  cpu.set_PC(cpu.PC() + 1)
  cpu.clock_ticks_since_reset += 2
  logger.log_instruction(cpu)


def inc(cpu, logger, addr):
  result =   (cpu.memory[addr] + 1) % 256 #precisa?
  cpu.memory[addr] = result
  cpu.set_zero_iff(result == 0)
  cpu.set_negative_iff(is_negative(result))
  logger.log_memory_access_instruction(cpu, addr, cpu.memory[addr])


SBC_IMMEDIATE = 0xE9
def sbc_immediate(cpu, logger):
  op1 = cpu.A()
  op2 = get_immediate(cpu)
  result = cpu.A() - op2 - (1 - cpu.carry())
  cpu.set_A(result)

  cpu.set_negative_iff(is_negative(cpu.A()))
  cpu.set_overflow_iff(is_sbc_overflow(op1, op2, cpu.A()))
  cpu.set_zero_iff(cpu.A() == 0)
  cpu.set_carry_iff(result >= 0)
  cpu.clock_ticks_since_reset += 2
  logger.log_instruction(cpu)


SBC_ZEROPAGE = 0xE5
def sbc_zeropage(cpu, logger):
  op2 = get_zeropage_addr(cpu)
  cpu.clock_ticks_since_reset += 3
  sbc(cpu, logger, op2)

SBC_ZEROPAGE_X = 0xF5
def sbc_zeropage_x(cpu, logger):
  addr = get_zeropage_x_addr(cpu)
  cpu.clock_ticks_since_reset += 4
  sbc(cpu, logger, addr)

SBC_ABSOLUTE = 0xED
def sbc_absolute(cpu, logger):
  addr = get_absolute_addr(cpu)
  cpu.clock_ticks_since_reset += 4
  sbc(cpu, logger, addr)

SBC_ABSOLUTE_X = 0xFD
def sbc_absolute_x(cpu, logger):
  addr, pageCrossed = get_absolute_x_addr(cpu)
  cpu.clock_ticks_since_reset += 4 + pageCrossed
  sbc(cpu, logger, addr)

SBC_ABSOLUTE_Y = 0xF9
def sbc_absolute_y(cpu, logger):
  addr, pageCrossed  = get_absolute_y_addr(cpu)
  cpu.clock_ticks_since_reset += 4 + pageCrossed
  sbc(cpu, logger, addr)

SBC_INDIRECT_X = 0xE1
def sbc_indirect_x(cpu, logger):
  addr = get_indirect_x_addr(cpu)
  cpu.clock_ticks_since_reset += 6
  sbc(cpu, logger, addr)

SBC_INDIRECT_Y = 0xF1
def sbc_indirect_y(cpu, logger):
  addr, pageCrossed = get_indirect_y_addr(cpu)
  cpu.clock_ticks_since_reset += 5 + pageCrossed

  sbc(cpu, logger, addr)

def sbc(cpu, logger, addr):
  op1 = cpu.A()
  op2 = cpu.memory[addr]
  result = cpu.A() - op2 - (1 - cpu.carry())
  cpu.set_A(result)

  cpu.set_negative_iff(is_negative(cpu.A()))
  cpu.set_overflow_iff(is_sbc_overflow(op1, op2, cpu.A()))
  cpu.set_zero_iff(cpu.A() == 0)
  cpu.set_carry_iff(result >= 0)
  logger.log_memory_access_instruction(cpu, addr, op2)
