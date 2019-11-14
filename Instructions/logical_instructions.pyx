# cython: profile=True


from Instructions.address_getters cimport *
from nes_cpu_utils cimport is_negative


BIT_ZEROPAGE = 0x24
cdef void bit_zeropage(Cpu cpu, CpuLogger logger) except *:
    bit(cpu, logger, get_zeropage_addr(cpu))
    cpu.clock_ticks_since_reset += 3

BIT_ABSOLUTE = 0x2C
cdef void bit_absolute(Cpu cpu, CpuLogger logger) except *:
    bit(cpu, logger, get_absolute_addr(cpu))
    cpu.clock_ticks_since_reset += 4

cdef void bit(Cpu cpu, CpuLogger logger, int addr) except *:
    op2 = cpu.memory(addr)
    cpu.set_A(cpu.A() & op2)

    cpu.set_negative_iff(op2 & 0b10000000)
    cpu.set_overflow_iff(op2 & 0b01000000)
    cpu.set_zero_iff(cpu.A() == 0)

    logger.log_memory_access_instruction(cpu, addr, op2)


AND_IMMEDIATE = 0x29
cdef void and_immediate(Cpu cpu, CpuLogger logger) except *:
    op2 = get_immediate(cpu)
    cpu.set_A(cpu.A() & op2)

    cpu.set_negative_iff(is_negative(cpu.A()))
    cpu.set_zero_iff(cpu.A() == 0)

    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

AND_ZERO_PAGE = 0x25
cdef void and_zeropage(Cpu cpu, CpuLogger logger) except *:
    and_instruction(cpu, logger, get_zeropage_addr(cpu))
    cpu.clock_ticks_since_reset += 3

AND_ZERO_PAGE_X = 0x35
cdef void and_zeropage_x(Cpu cpu, CpuLogger logger) except *:
    and_instruction(cpu, logger, get_zeropage_x_addr(cpu))
    cpu.clock_ticks_since_reset += 4

AND_ABSOLUTE = 0x2D
cdef void and_absolute(Cpu cpu, CpuLogger logger) except *:
    and_instruction(cpu, logger, get_absolute_addr(cpu))
    cpu.clock_ticks_since_reset += 4

AND_ABSOLUTE_X = 0x3D
cdef void and_absolute_x(Cpu cpu, CpuLogger logger) except *:
    addr,  pageCrossed =  get_absolute_x_addr(cpu)
    and_instruction(cpu, logger, addr )
    cpu.clock_ticks_since_reset += 4 + pageCrossed

AND_ABSOLUTE_Y = 0x39
cdef void and_absolute_y(Cpu cpu, CpuLogger logger) except *:
    addr, pageCrossed = get_absolute_y_addr(cpu)
    and_instruction(cpu, logger, addr )
    cpu.clock_ticks_since_reset += 4 + pageCrossed

AND_INDIRECT_X = 0x21
cdef void and_indirect_x(Cpu cpu, CpuLogger logger) except *:
    and_instruction(cpu, logger, get_indirect_x_addr(cpu))
    cpu.clock_ticks_since_reset += 6

AND_INDIRECT_Y = 0x31
cdef void and_indirect_y(Cpu cpu, CpuLogger logger) except *:
    addr, pageCrossed = get_indirect_y_addr(cpu)
    and_instruction(cpu, logger, addr)
    cpu.clock_ticks_since_reset += 5 + pageCrossed

cdef void and_instruction(Cpu cpu, CpuLogger logger, int addr) except *:
    op2 = cpu.memory(addr)
    cpu.set_A(cpu.A() & op2)

    cpu.set_negative_iff(is_negative(cpu.A()))
    cpu.set_zero_iff(cpu.A() == 0)

    logger.log_memory_access_instruction(cpu, addr, op2)


EOR_IMMEDIATE = 0x49
cdef void eor_immediate(Cpu cpu, CpuLogger logger) except *:
    op2 = get_immediate(cpu)
    cpu.set_A(cpu.A() ^ op2)

    cpu.set_negative_iff(is_negative(cpu.A()))
    cpu.set_zero_iff(cpu.A() == 0)

    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

EOR_ZERO_PAGE = 0x45
cdef void eor_zeropage(Cpu cpu, CpuLogger logger) except *:
    eor_instruction(cpu, logger, get_zeropage_addr(cpu))
    cpu.clock_ticks_since_reset += 3

EOR_ZERO_PAGE_X = 0x55
cdef void eor_zeropage_x(Cpu cpu, CpuLogger logger) except *:
    eor_instruction(cpu, logger, get_zeropage_x_addr(cpu))
    cpu.clock_ticks_since_reset += 4

EOR_ABSOLUTE = 0x4D
cdef void eor_absolute(Cpu cpu, CpuLogger logger) except *:
    eor_instruction(cpu, logger, get_absolute_addr(cpu))
    cpu.clock_ticks_since_reset += 4

EOR_ABSOLUTE_X = 0x5D
cdef void eor_absolute_x(Cpu cpu, CpuLogger logger) except *:
    addr,  pageCrossed =  get_absolute_x_addr(cpu)
    eor_instruction(cpu, logger, addr)
    cpu.clock_ticks_since_reset += 4 + pageCrossed

EOR_ABSOLUTE_Y = 0x59
cdef void eor_absolute_y(Cpu cpu, CpuLogger logger) except *:
    addr, pageCrossed = get_absolute_y_addr(cpu)
    eor_instruction(cpu, logger, addr)
    cpu.clock_ticks_since_reset += 4 + pageCrossed

EOR_INDIRECT_X = 0x41
cdef void eor_indirect_x(Cpu cpu, CpuLogger logger) except *:
    eor_instruction(cpu, logger, get_indirect_x_addr(cpu))
    cpu.clock_ticks_since_reset += 6

EOR_INDIRECT_Y = 0x51
cdef void eor_indirect_y(Cpu cpu, CpuLogger logger) except *:
    addr, pageCrossed = get_indirect_y_addr(cpu)
    eor_instruction(cpu, logger, addr)
    cpu.clock_ticks_since_reset += 5 + pageCrossed

cdef void eor_instruction(Cpu cpu, CpuLogger logger, int addr) except *:
    op2 = cpu.memory(addr)
    cpu.set_A(cpu.A() ^ op2)

    cpu.set_negative_iff(is_negative(cpu.A()))
    cpu.set_zero_iff(cpu.A() == 0)

    logger.log_memory_access_instruction(cpu, addr, op2)


ORA_IMMEDIATE = 0x09
cdef void ora_immediate(Cpu cpu, CpuLogger logger) except *:
    op2 = get_immediate(cpu)
    cpu.set_A(cpu.A() | op2)

    cpu.set_negative_iff(is_negative(cpu.A()))
    cpu.set_zero_iff(cpu.A() == 0)

    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

ORA_ZERO_PAGE = 0x05
cdef void ora_zeropage(Cpu cpu, CpuLogger logger) except *:
    ora_instruction(cpu, logger, get_zeropage_addr(cpu))
    cpu.clock_ticks_since_reset += 3

ORA_ZERO_PAGE_X = 0x15
cdef void ora_zeropage_x(Cpu cpu, CpuLogger logger) except *:
    ora_instruction(cpu, logger, get_zeropage_x_addr(cpu))
    cpu.clock_ticks_since_reset += 4

ORA_ABSOLUTE = 0x0D
cdef void ora_absolute(Cpu cpu, CpuLogger logger) except *:
    ora_instruction(cpu, logger, get_absolute_addr(cpu))
    cpu.clock_ticks_since_reset += 4

ORA_ABSOLUTE_X = 0x1D
cdef void ora_absolute_x(Cpu cpu, CpuLogger logger) except *:
    addr,  pageCrossed =  get_absolute_x_addr(cpu)
    ora_instruction(cpu, logger, addr)
    cpu.clock_ticks_since_reset += 4 + pageCrossed

ORA_ABSOLUTE_Y = 0x19
cdef void ora_absolute_y(Cpu cpu, CpuLogger logger) except *:
    addr, pageCrossed = get_absolute_y_addr(cpu)
    ora_instruction(cpu, logger, addr)
    cpu.clock_ticks_since_reset += 4 + pageCrossed

ORA_INDIRECT_X = 0x01
cdef void ora_indirect_x(Cpu cpu, CpuLogger logger) except *:
    ora_instruction(cpu, logger, get_indirect_x_addr(cpu))
    cpu.clock_ticks_since_reset += 6

ORA_INDIRECT_Y = 0x11
cdef void ora_indirect_y(Cpu cpu, CpuLogger logger) except *:
    addr, pageCrossed = get_indirect_y_addr(cpu)
    ora_instruction(cpu, logger, pageCrossed)
    cpu.clock_ticks_since_reset += 5 + pageCrossed

cdef void ora_instruction(Cpu cpu, CpuLogger logger, int addr) except *:
    op2 = cpu.memory(addr)
    cpu.set_A(cpu.A() | op2)

    cpu.set_negative_iff(is_negative(cpu.A()))
    cpu.set_zero_iff(cpu.A() == 0)

    logger.log_memory_access_instruction(cpu, addr, op2)


ASL_ACCUMULATOR = 0x0A
cdef void asl_accumulator(Cpu cpu, CpuLogger logger) except *:
    result, carry = rotate_left(cpu.A(), 0)
    cpu.set_A(result)

    cpu.set_negative_iff(is_negative(result))
    cpu.set_zero_iff(result == 0)
    cpu.set_carry_iff(carry)

    cpu.set_PC(cpu.PC() + 1)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

ASL_ZERO_PAGE = 0x06
cdef void asl_zeropage(Cpu cpu, CpuLogger logger) except *:
    asl(cpu, logger, get_zeropage_addr(cpu))
    cpu.clock_ticks_since_reset += 5

ASL_ZERO_PAGE_X = 0x16
cdef void asl_zeropage_x(Cpu cpu, CpuLogger logger) except *:
    asl(cpu, logger, get_zeropage_x_addr(cpu))
    cpu.clock_ticks_since_reset += 6

ASL_ABSOLUTE = 0x0E
cdef void asl_absolute(Cpu cpu, CpuLogger logger) except *:
    asl(cpu, logger, get_absolute_addr(cpu))
    cpu.clock_ticks_since_reset += 6

ASL_ABSOLUTE_X = 0x1E
cdef void asl_absolute_x(Cpu cpu, CpuLogger logger) except *:
    addr, pageCrossed =  get_absolute_x_addr(cpu)
    asl(cpu, logger, addr)
    cpu.clock_ticks_since_reset += 7

cdef void asl(Cpu cpu, CpuLogger logger, int addr) except *:
    result, carry = rotate_left(cpu.memory(addr), 0)
    cpu.set_memory(addr, result)

    cpu.set_negative_iff(is_negative(result))
    cpu.set_zero_iff(result == 0)
    cpu.set_carry_iff(carry)

    logger.log_memory_access_instruction(cpu, addr, result)


LSR_ACCUMULATOR = 0x4A
cdef void lsr_accumulator(Cpu cpu, CpuLogger logger) except *:
    result, carry = rotate_right(cpu.A(), 0)
    cpu.set_A(result)

    cpu.set_negative_iff(is_negative(result))
    cpu.set_zero_iff(result == 0)
    cpu.set_carry_iff(carry)

    cpu.set_PC(cpu.PC() + 1)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

LSR_ZERO_PAGE = 0x46
cdef void lsr_zeropage(Cpu cpu, CpuLogger logger) except *:
    lsr(cpu, logger, get_zeropage_addr(cpu))
    cpu.clock_ticks_since_reset += 5

LSR_ZERO_PAGE_X = 0x56
cdef void lsr_zeropage_x(Cpu cpu, CpuLogger logger) except *:
    lsr(cpu, logger, get_zeropage_x_addr(cpu))
    cpu.clock_ticks_since_reset += 6

LSR_ABSOLUTE = 0x4E
cdef void lsr_absolute(Cpu cpu, CpuLogger logger) except *:
    lsr(cpu, logger, get_absolute_addr(cpu))
    cpu.clock_ticks_since_reset += 6

LSR_ABSOLUTE_X = 0x5E
cdef void lsr_absolute_x(Cpu cpu, CpuLogger logger) except *:
    addr, pageCrossed = get_absolute_x_addr(cpu)
    lsr(cpu, logger, addr)
    cpu.clock_ticks_since_reset += 7

cdef void lsr(Cpu cpu, CpuLogger logger, int addr) except *:
    result, carry = rotate_right(cpu.memory(addr), 0)
    cpu.set_memory(addr, result)

    cpu.set_negative_iff(is_negative(result))
    cpu.set_zero_iff(result == 0)
    cpu.set_carry_iff(carry)

    logger.log_memory_access_instruction(cpu, addr, result)


ROL_ACCUMULATOR = 0x2A
cdef void rol_accumulator(Cpu cpu, CpuLogger logger) except *:
    result, carry = rotate_left(cpu.A(), cpu.carry())
    cpu.set_A(result)

    cpu.set_negative_iff(is_negative(result))
    cpu.set_zero_iff(result == 0)
    cpu.set_carry_iff(carry)

    cpu.set_PC(cpu.PC() + 1)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

ROL_ZERO_PAGE = 0x26
cdef void rol_zeropage(Cpu cpu, CpuLogger logger) except *:
    rol(cpu, logger, get_zeropage_addr(cpu))
    cpu.clock_ticks_since_reset += 5

ROL_ZERO_PAGE_X = 0x36
cdef void rol_zeropage_x(Cpu cpu, CpuLogger logger) except *:
    rol(cpu, logger, get_zeropage_x_addr(cpu))
    cpu.clock_ticks_since_reset += 6

ROL_ABSOLUTE = 0x2E
cdef void rol_absolute(Cpu cpu, CpuLogger logger) except *:
    rol(cpu, logger, get_absolute_addr(cpu))
    cpu.clock_ticks_since_reset += 6

ROL_ABSOLUTE_X = 0x3E
cdef void rol_absolute_x(Cpu cpu, CpuLogger logger) except *:
    addr, pageCrossed = get_absolute_x_addr(cpu)
    rol(cpu, logger, addr)
    cpu.clock_ticks_since_reset += 7

cdef void rol(Cpu cpu, CpuLogger logger, int addr) except *:
    result, carry = rotate_left(cpu.memory(addr), cpu.carry())
    cpu.set_memory(addr, result)

    cpu.set_negative_iff(is_negative(result))
    cpu.set_zero_iff(result == 0)
    cpu.set_carry_iff(carry)

    logger.log_memory_access_instruction(cpu, addr, result)


ROR_ACCUMULATOR = 0x6A
cdef void ror_accumulator(Cpu cpu, CpuLogger logger) except *:
    result, carry = rotate_right(cpu.A(), cpu.carry())
    cpu.set_A(result)

    cpu.set_negative_iff(is_negative(result))
    cpu.set_zero_iff(result == 0)
    cpu.set_carry_iff(carry)

    cpu.set_PC(cpu.PC() + 1)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

ROR_ZERO_PAGE = 0x66
cdef void ror_zeropage(Cpu cpu, CpuLogger logger) except *:
    ror(cpu, logger, get_zeropage_addr(cpu))
    cpu.clock_ticks_since_reset += 5

ROR_ZERO_PAGE_X = 0x76
cdef void ror_zeropage_x(Cpu cpu, CpuLogger logger) except *:
    ror(cpu, logger, get_zeropage_x_addr(cpu))
    cpu.clock_ticks_since_reset += 6

ROR_ABSOLUTE = 0x6E
cdef void ror_absolute(Cpu cpu, CpuLogger logger) except *:
    ror(cpu, logger, get_absolute_addr(cpu))
    cpu.clock_ticks_since_reset += 6

ROR_ABSOLUTE_X = 0x7E
cdef void ror_absolute_x(Cpu cpu, CpuLogger logger) except *:
    addr, pageCrossed = get_absolute_x_addr(cpu)
    ror(cpu, logger, addr)
    cpu.clock_ticks_since_reset += 7

cdef void ror(Cpu cpu, CpuLogger logger, int addr) except *:
    result, carry = rotate_right(cpu.memory(addr), cpu.carry())
    cpu.set_memory(addr, result)

    cpu.set_negative_iff(is_negative(result))
    cpu.set_zero_iff(result == 0)
    cpu.set_carry_iff(carry)

    logger.log_memory_access_instruction(cpu, addr, result)


cdef inline (int, int) rotate_left(int value, int carry_in) except *:
    assert 0 <= value < 256
    assert 0 <= carry_in < 2

    carry_out = int(value & 0b10000000 != 0)
    result = ((value << 1) % 256) | carry_in

    return result, carry_out

cdef inline (int, int) rotate_right(int value, int carry_in) except *:
    assert 0 <= value < 256
    assert 0 <= carry_in < 2

    carry_out = int(value & 0b1 != 0)
    result = (value >> 1) | (carry_in << 7)

    return result, carry_out
