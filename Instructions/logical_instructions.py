from Instructions.address_getters import *
from nes_cpu_utils import is_negative


BIT_ZEROPAGE = 0x24
def bit_zeropage(cpu, logger):
    bit(cpu, logger, get_zeropage_addr(cpu))

BIT_ABSOLUTE = 0x2C
def bit_absolute(cpu, logger):
    bit(cpu, logger, get_absolute_addr(cpu))

def bit(cpu, logger, addr):
    op2 = cpu.memory[addr]
    cpu.set_A(cpu.A() & op2)

    cpu.set_negative_iff(op2 & 0b10000000)
    cpu.set_overflow_iff(op2 & 0b01000000)
    cpu.set_zero_iff(cpu.A() == 0)

    logger.log_memory_access_instruction(cpu, addr, op2)


AND_IMMEDIATE = 0x29
def and_immediate(cpu, logger):
    op2 = get_immediate(cpu)
    cpu.set_A(cpu.A() & op2)

    cpu.set_negative_iff(is_negative(cpu.A()))
    cpu.set_zero_iff(cpu.A() == 0)

    logger.log_instruction(cpu)

AND_ZERO_PAGE = 0x25
def and_zeropage(cpu, logger):
    and_instruction(cpu, logger, get_zeropage_addr(cpu))

AND_ZERO_PAGE_X = 0x35
def and_zeropage_x(cpu, logger):
    and_instruction(cpu, logger, get_zeropage_x_addr(cpu))

AND_ABSOLUTE = 0x2D
def and_absolute(cpu, logger):
    and_instruction(cpu, logger, get_absolute_addr(cpu))

AND_ABSOLUTE_X = 0x3D
def and_absolute_x(cpu, logger):
    and_instruction(cpu, logger, get_absolute_x_addr(cpu))

AND_ABSOLUTE_Y = 0x39
def and_absolute_y(cpu, logger):
    and_instruction(cpu, logger, get_absolute_y_addr(cpu))

AND_INDIRECT_X = 0x21
def and_indirect_x(cpu, logger):
    and_instruction(cpu, logger, get_indirect_x_addr(cpu))

AND_INDIRECT_Y = 0x31
def and_indirect_y(cpu, logger):
    and_instruction(cpu, logger, get_indirect_y_addr(cpu))

def and_instruction(cpu, logger, addr):
    op2 = cpu.memory[addr]
    cpu.set_A(cpu.A() & op2)

    cpu.set_negative_iff(is_negative(cpu.A()))
    cpu.set_zero_iff(cpu.A() == 0)

    logger.log_memory_access_instruction(cpu, addr, op2)


EOR_IMMEDIATE = 0x49
def eor_immediate(cpu, logger):
    op2 = get_immediate(cpu)
    cpu.set_A(cpu.A() ^ op2)

    cpu.set_negative_iff(is_negative(cpu.A()))
    cpu.set_zero_iff(cpu.A() == 0)

    logger.log_instruction(cpu)

EOR_ZERO_PAGE = 0x45
def eor_zeropage(cpu, logger):
    eor_instruction(cpu, logger, get_zeropage_addr(cpu))

EOR_ZERO_PAGE_X = 0x55
def eor_zeropage_x(cpu, logger):
    eor_instruction(cpu, logger, get_zeropage_x_addr(cpu))

EOR_ABSOLUTE = 0x4D
def eor_absolute(cpu, logger):
    eor_instruction(cpu, logger, get_absolute_addr(cpu))

EOR_ABSOLUTE_X = 0x5D
def eor_absolute_x(cpu, logger):
    eor_instruction(cpu, logger, get_absolute_x_addr(cpu))

EOR_ABSOLUTE_Y = 0x59
def eor_absolute_y(cpu, logger):
    eor_instruction(cpu, logger, get_absolute_y_addr(cpu))

EOR_INDIRECT_X = 0x41
def eor_indirect_x(cpu, logger):
    eor_instruction(cpu, logger, get_indirect_x_addr(cpu))

EOR_INDIRECT_Y = 0x51
def eor_indirect_y(cpu, logger):
    eor_instruction(cpu, logger, get_indirect_y_addr(cpu))

def eor_instruction(cpu, logger, addr):
    op2 = cpu.memory[addr]
    cpu.set_A(cpu.A() ^ op2)

    cpu.set_negative_iff(is_negative(cpu.A()))
    cpu.set_zero_iff(cpu.A() == 0)

    logger.log_memory_access_instruction(cpu, addr, op2)


ORA_IMMEDIATE = 0x09
def ora_immediate(cpu, logger):
    op2 = get_immediate(cpu)
    cpu.set_A(cpu.A() | op2)

    cpu.set_negative_iff(is_negative(cpu.A()))
    cpu.set_zero_iff(cpu.A() == 0)

    logger.log_instruction(cpu)

ORA_ZERO_PAGE = 0x05
def ora_zeropage(cpu, logger):
    ora_instruction(cpu, logger, get_zeropage_addr(cpu))

ORA_ZERO_PAGE_X = 0x15
def ora_zeropage_x(cpu, logger):
    ora_instruction(cpu, logger, get_zeropage_x_addr(cpu))

ORA_ABSOLUTE = 0x0D
def ora_absolute(cpu, logger):
    ora_instruction(cpu, logger, get_absolute_addr(cpu))

ORA_ABSOLUTE_X = 0x1D
def ora_absolute_x(cpu, logger):
    ora_instruction(cpu, logger, get_absolute_x_addr(cpu))

ORA_ABSOLUTE_Y = 0x19
def ora_absolute_y(cpu, logger):
    ora_instruction(cpu, logger, get_absolute_y_addr(cpu))

ORA_INDIRECT_X = 0x01
def ora_indirect_x(cpu, logger):
    ora_instruction(cpu, logger, get_indirect_x_addr(cpu))

ORA_INDIRECT_Y = 0x11
def ora_indirect_y(cpu, logger):
    ora_instruction(cpu, logger, get_indirect_y_addr(cpu))

def ora_instruction(cpu, logger, addr):
    op2 = cpu.memory[addr]
    cpu.set_A(cpu.A() | op2)

    cpu.set_negative_iff(is_negative(cpu.A()))
    cpu.set_zero_iff(cpu.A() == 0)

    logger.log_memory_access_instruction(cpu, addr, op2)


ASL_ACCUMULATOR = 0x0A
def asl_accumulator(cpu, logger):
    result, carry = rotate_left(cpu.A(), 0)
    cpu.set_A(result)

    cpu.set_negative_iff(is_negative(result))
    cpu.set_zero_iff(result == 0)
    cpu.set_carry_iff(carry)

    cpu.set_PC(cpu.PC() + 1)
    logger.log_instruction(cpu)

ASL_ZERO_PAGE = 0x06
def asl_zeropage(cpu, logger):
    asl(cpu, logger, get_zeropage_addr(cpu))

ASL_ZERO_PAGE_X = 0x16
def asl_zeropage_x(cpu, logger):
    asl(cpu, logger, get_zeropage_x_addr(cpu))

ASL_ABSOLUTE = 0x0E
def asl_absolute(cpu, logger):
    asl(cpu, logger, get_absolute_addr(cpu))

ASL_ABSOLUTE_X = 0x1E
def asl_absolute_x(cpu, logger):
    asl(cpu, logger, get_absolute_x_addr(cpu))

def asl(cpu, logger, addr):
    result, carry = rotate_left(cpu.memory[addr], 0)
    cpu.memory[addr] = result

    cpu.set_negative_iff(is_negative(result))
    cpu.set_zero_iff(result == 0)
    cpu.set_carry_iff(carry)

    logger.log_memory_access_instruction(cpu, addr, result)


LSR_ACCUMULATOR = 0x4A
def lsr_accumulator(cpu, logger):
    result, carry = rotate_right(cpu.A(), 0)
    cpu.set_A(result)

    cpu.set_negative_iff(is_negative(result))
    cpu.set_zero_iff(result == 0)
    cpu.set_carry_iff(carry)

    cpu.set_PC(cpu.PC() + 1)
    logger.log_instruction(cpu)

LSR_ZERO_PAGE = 0x46
def lsr_zeropage(cpu, logger):
    lsr(cpu, logger, get_zeropage_addr(cpu))

LSR_ZERO_PAGE_X = 0x56
def lsr_zeropage_x(cpu, logger):
    lsr(cpu, logger, get_zeropage_x_addr(cpu))

LSR_ABSOLUTE = 0x4E
def lsr_absolute(cpu, logger):
    lsr(cpu, logger, get_absolute_addr(cpu))

LSR_ABSOLUTE_X = 0x5E
def lsr_absolute_x(cpu, logger):
    lsr(cpu, logger, get_absolute_x_addr(cpu))

def lsr(cpu, logger, addr):
    result, carry = rotate_right(cpu.memory[addr], 0)
    cpu.memory[addr] = result

    cpu.set_negative_iff(is_negative(result))
    cpu.set_zero_iff(result == 0)
    cpu.set_carry_iff(carry)

    logger.log_memory_access_instruction(cpu, addr, result)


ROL_ACCUMULATOR = 0x2A
def rol_accumulator(cpu, logger):
    result, carry = rotate_left(cpu.A(), cpu.carry())
    cpu.set_A(result)

    cpu.set_negative_iff(is_negative(result))
    cpu.set_zero_iff(result == 0)
    cpu.set_carry_iff(carry)

    cpu.set_PC(cpu.PC() + 1)
    logger.log_instruction(cpu)

ROL_ZERO_PAGE = 0x26
def rol_zeropage(cpu, logger):
    rol(cpu, logger, get_zeropage_addr(cpu))

ROL_ZERO_PAGE_X = 0x36
def rol_zeropage_x(cpu, logger):
    rol(cpu, logger, get_zeropage_x_addr(cpu))

ROL_ABSOLUTE = 0x2E
def rol_absolute(cpu, logger):
    rol(cpu, logger, get_absolute_addr(cpu))

ROL_ABSOLUTE_X = 0x3E
def rol_absolute_x(cpu, logger):
    rol(cpu, logger, get_absolute_x_addr(cpu))

def rol(cpu, logger, addr):
    result, carry = rotate_left(cpu.memory[addr], cpu.carry())
    cpu.memory[addr] = result

    cpu.set_negative_iff(is_negative(result))
    cpu.set_zero_iff(result == 0)
    cpu.set_carry_iff(carry)

    logger.log_memory_access_instruction(cpu, addr, result)


ROR_ACCUMULATOR = 0x6A
def ror_accumulator(cpu, logger):
    result, carry = rotate_right(cpu.A(), cpu.carry())
    cpu.set_A(result)

    cpu.set_negative_iff(is_negative(result))
    cpu.set_zero_iff(result == 0)
    cpu.set_carry_iff(carry)

    cpu.set_PC(cpu.PC() + 1)
    logger.log_instruction(cpu)

ROR_ZERO_PAGE = 0x66
def ror_zeropage(cpu, logger):
    ror(cpu, logger, get_zeropage_addr(cpu))

ROR_ZERO_PAGE_X = 0x76
def ror_zeropage_x(cpu, logger):
    ror(cpu, logger, get_zeropage_x_addr(cpu))

ROR_ABSOLUTE = 0x6E
def ror_absolute(cpu, logger):
    ror(cpu, logger, get_absolute_addr(cpu))

ROR_ABSOLUTE_X = 0x7E
def ror_absolute_x(cpu, logger):
    ror(cpu, logger, get_absolute_x_addr(cpu))

def ror(cpu, logger, addr):
    result, carry = rotate_right(cpu.memory[addr], cpu.carry())
    cpu.memory[addr] = result

    cpu.set_negative_iff(is_negative(result))
    cpu.set_zero_iff(result == 0)
    cpu.set_carry_iff(carry)

    logger.log_memory_access_instruction(cpu, addr, result)



def rotate_left(value, carry_in):
    assert 0 <= value < 256
    assert 0 <= carry_in < 2

    carry_out = int(value & 0b10000000 != 0)
    result = ((value << 1) % 256) | carry_in

    return result, carry_out

def rotate_right(value, carry_in):
    assert 0 <= value < 256
    assert 0 <= carry_in < 2

    carry_out = int(value & 0b1 != 0)
    result = (value >> 1) | (carry_in << 7)

    return result, carry_out
    