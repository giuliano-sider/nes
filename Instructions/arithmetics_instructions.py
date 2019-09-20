from nes_cpu_utils import is_negative, is_overflow, twos_comp
from Instructions.address_getters import *

ADC_IMMEDIATE = 0x69
def adc_immediate(cpu, logger):
    op2 = get_immediate(cpu)
    adc(cpu, logger, op2)

ADC_ZEROPAGE = 0x65
def adc_zeropage(cpu, logger):
    op2 = get_zeropage(cpu)
    adc(cpu, logger, op2)

ADC_ZEROPAGEX = 0x75
def adc_zeropage_x(cpu, logger):
    op2 = get_zeropage_x(cpu)
    adc(cpu, logger, op2)

ADC_ABSOLUTE = 0x6D
def adc_absolute(cpu, logger):
    op2 = get_absolute(cpu)
    adc(cpu, logger, op2)

ADC_ABSOLUTE_X = 0x7D
def adc_absolute_x(cpu, logger):
    op2 = get_absolute_x(cpu)
    adc(cpu, logger, op2)

ADC_ABSOLUTE_Y = 0x79
def adc_absolute_y(cpu, logger):
    op2 = get_absolute_y(cpu)
    adc(cpu, logger, op2)

ADC_INDIRECT_X = 0x61
def adc_indirect_x(cpu, logger):
    op2 = get_indirect_x(cpu)
    adc(cpu, logger, op2)

ADC_INDIRECT_Y = 0x71
def adc_indirect_y(cpu, logger):
    op2 = get_indirect_y(cpu)
    adc(cpu, logger, op2)

def adc(cpu, logger, op2):
    op1 = cpu.A()
    result = cpu.A() + op2 + cpu.carry()
    cpu.set_A(result)

    cpu.set_negative_iff(is_negative(cpu.A()))
    cpu.set_overflow_iff(is_overflow(op1, op2, cpu.A()))
    cpu.set_zero_iff(cpu.A() == 0)
    cpu.set_carry_iff(result >= 256)

    logger.log_instruction(cpu)

CMP_IMMEDIATE = 0xC9
def cmp_immediate(cpu, logger):
    op2 = get_immediate(cpu)
    cmp(cpu, logger, op2)

CMP_ZEROPAGE = 0xC5
def cmp_zeropage(cpu, logger):
    op2 =  get_zeropage(cpu)
    cmp(cpu, logger, op2)

CMP_ZEROPAGE_X = 0xD5
def cmp_zero_page_x(cpu, logger):
    # to be implemented OPCODE d5
    raise NotImplementedError()

def cmp_absolute(cpu, logger):
    # to be implemented OPCODE cd
    raise NotImplementedError()

def cmp_absolute_x(cpu, logger):
    # to be implemented OPCODE dd
    raise NotImplementedError()

def cmp_absolute_y(cpu, logger):
    # to be implemented OPCODE d9
    raise NotImplementedError()

def cmp_indirect_x(cpu, logger):
    # to be implemented OPCODE d1
    raise NotImplementedError()

def cmp_indirect_y(cpu, logger):
    # to be implemented OPCODE d1
    raise NotImplementedError()


def cmp(cpu, logger, op2):
    op1 = cpu.A()
    result = (op1-op2) % 256 #Perform 2 complement subtraction
    cpu.set_zero_iff(op1 == op2)
    cpu.set_carry_iff(op1 >= op2)
    cpu.set_negative_iff(is_negative(result))
