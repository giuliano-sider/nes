# cython: profile=True


from nes_cpu_utils cimport is_negative, is_adc_overflow, is_sbc_overflow, twos_comp
from Instructions.address_getters cimport *

ADC_IMMEDIATE = 0x69
cdef void adc_immediate(Cpu cpu, CpuLogger logger) except *:
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
cdef void adc_zeropage(Cpu cpu, CpuLogger logger) except *:
    addr = get_zeropage_addr(cpu)
    adc(cpu, logger, addr)
    cpu.clock_ticks_since_reset += 3

ADC_ZEROPAGEX = 0x75
cdef void adc_zeropage_x(Cpu cpu, CpuLogger logger) except *:
    addr = get_zeropage_x_addr(cpu)
    adc(cpu, logger, addr)
    cpu.clock_ticks_since_reset += 4

ADC_ABSOLUTE = 0x6D
cdef void adc_absolute(Cpu cpu, CpuLogger logger) except *:
    addr = get_absolute_addr(cpu)
    adc(cpu, logger, addr)
    cpu.clock_ticks_since_reset += 4

ADC_ABSOLUTE_X = 0x7D
cdef void adc_absolute_x(Cpu cpu, CpuLogger logger) except *:
    addr, pageCrossed = get_absolute_x_addr(cpu)
    cpu.clock_ticks_since_reset += 4 + pageCrossed
    adc(cpu, logger, addr)

ADC_ABSOLUTE_Y = 0x79
cdef void adc_absolute_y(Cpu cpu, CpuLogger logger) except *:
    addr, pageCrossed = get_absolute_y_addr(cpu)
    cpu.clock_ticks_since_reset += 4 + pageCrossed
    adc(cpu, logger, addr)

ADC_INDIRECT_X = 0x61
cdef void adc_indirect_x(Cpu cpu, CpuLogger logger) except *:
    addr = get_indirect_x_addr(cpu)
    cpu.clock_ticks_since_reset += 6
    adc(cpu, logger, addr)

ADC_INDIRECT_Y = 0x71
cdef void adc_indirect_y(Cpu cpu, CpuLogger logger) except *:
    addr, pageCrossed = get_indirect_y_addr(cpu)
    cpu.clock_ticks_since_reset += 5 + pageCrossed
    adc(cpu, logger, addr)

cdef void adc(Cpu cpu, CpuLogger logger, int addr) except *:
    op2 = cpu.memory(addr)
    op1 = cpu.A()
    result = cpu.A() + op2 + cpu.carry()
    cpu.set_A(result)

    cpu.set_negative_iff(is_negative(cpu.A()))
    cpu.set_overflow_iff(is_adc_overflow(op1, op2, cpu.A()))
    cpu.set_zero_iff(cpu.A() == 0)
    cpu.set_carry_iff(result >= 256)

    logger.log_memory_access_instruction(cpu, addr, op2)

CMP_IMMEDIATE = 0xC9
cdef void cmp_immediate(Cpu cpu, CpuLogger logger) except *:
    op1 = cpu.A()
    op2 = get_immediate(cpu)
    result = (op1 - op2) % 256  # Perform 2 complement subtraction
    cpu.set_zero_iff(op1 == op2)
    cpu.set_carry_iff(op1 >= op2)
    cpu.set_negative_iff(is_negative(result))
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

CMP_ZEROPAGE = 0xC5
cdef void cmp_zeropage(Cpu cpu, CpuLogger logger) except *:
    op1 = cpu.A()
    op2 = get_zeropage_addr(cpu)
    cpu.clock_ticks_since_reset += 3
    cmp(cpu, logger, op1, op2)


CMP_ZEROPAGE_X = 0xD5
cdef void cmp_zero_page_x(Cpu cpu, CpuLogger logger) except *:
    op1 = cpu.A()
    op2 = get_zeropage_x_addr(cpu)
    cpu.clock_ticks_since_reset += 4
    cmp(cpu, logger, op1, op2)

CMP_ABSOLUTE = 0xCD
cdef void cmp_absolute(Cpu cpu, CpuLogger logger) except *:
    op1 = cpu.A()
    op2 = get_absolute_addr(cpu)
    cpu.clock_ticks_since_reset += 4
    cmp(cpu, logger, op1, op2)


CMP_ABSOLUTE_X = 0xDD
cdef void cmp_absolute_x(Cpu cpu, CpuLogger logger) except *:
    op1 = cpu.A()
    op2, pageCrossed = get_absolute_x_addr(cpu)
    cpu.clock_ticks_since_reset += 4 + pageCrossed
    cmp(cpu, logger, op1, op2)

CMP_ABSOLUTE_Y = 0xD9
cdef void cmp_absolute_y(Cpu cpu, CpuLogger logger) except *:
    op1 = cpu.A()
    op2, pageCrossed = get_absolute_y_addr(cpu)
    cpu.clock_ticks_since_reset += 4 + pageCrossed
    cmp(cpu, logger, op1, op2)

CMP_INDIRECT_X = 0xC1
cdef void cmp_indirect_x(Cpu cpu, CpuLogger logger) except *:
    op1 = cpu.A()
    op2 = get_indirect_x_addr(cpu)
    cpu.clock_ticks_since_reset += 6
    cmp(cpu, logger, op1, op2)

CMP_INDIRECT_Y = 0xD1
cdef void cmp_indirect_y(Cpu cpu, CpuLogger logger) except *:
    op1 = cpu.A()
    op2, pageCrossed = get_indirect_y_addr(cpu)
    cpu.clock_ticks_since_reset += 5 + pageCrossed
    cmp(cpu, logger, op1, op2)

CPX_IMMEDIATE = 0xE0
cdef void cpx_immediate(Cpu cpu, CpuLogger logger) except *:
    op1 = cpu.X()
    op2 = get_immediate(cpu)
    result = (op1 - op2) % 256  # Perform 2 complement subtraction
    cpu.set_zero_iff(op1 == op2)
    cpu.set_carry_iff(op1 >= op2)
    cpu.set_negative_iff(is_negative(result))
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

CPX_ZEROPAGE = 0xE4
cdef void cpx_zeropage(Cpu cpu, CpuLogger logger) except *:
    op1 = cpu.X()
    op2 = get_zeropage_addr(cpu)
    cpu.clock_ticks_since_reset += 3
    cmp(cpu, logger, op1, op2)

CPX_ABSOLUTE = 0xEC
cdef void cpx_absolute(Cpu cpu, CpuLogger logger) except *:
    op1 = cpu.X()
    op2 = get_absolute_addr(cpu)
    cpu.clock_ticks_since_reset += 4
    cmp(cpu, logger, op1, op2)

CPY_IMMEDIATE = 0xC0
cdef void cpy_immediate(Cpu cpu, CpuLogger logger) except *:
    op1 = cpu.Y()
    op2 = get_immediate(cpu)
    result = (op1 - op2) % 256  # Perform 2 complement subtraction
    cpu.set_zero_iff(op1 == op2)
    cpu.set_carry_iff(op1 >= op2)
    cpu.set_negative_iff(is_negative(result))
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

CPY_ZEROPAGE = 0xC4
cdef void cpy_zeropage(Cpu cpu, CpuLogger logger) except *:
    op1 = cpu.Y()
    op2 = get_zeropage_addr(cpu)
    cpu.clock_ticks_since_reset += 3
    cmp(cpu, logger, op1, op2)

CPY_ABSOLUTE = 0xCC
cdef void cpy_absolute(Cpu cpu, CpuLogger logger) except *:
    op1 = cpu.Y()
    op2 = get_absolute_addr(cpu)
    cpu.clock_ticks_since_reset += 4
    cmp(cpu, logger, op1, op2)

cdef void cmp(Cpu cpu, CpuLogger logger, int op1, int addr) except *:
    op2 = cpu.memory(addr)
    result = (op1-op2) % 256  #Perform 2 complement subtraction
    cpu.set_zero_iff(op1 == op2)
    cpu.set_carry_iff(op1 >= op2)
    cpu.set_negative_iff(is_negative(result))
    logger.log_memory_access_instruction(cpu, addr, op2)

DEC_ZEROPAGE = 0XC6
cdef void dec_zeropage(Cpu cpu, CpuLogger logger) except *:
    addr = get_zeropage_addr(cpu)
    cpu.clock_ticks_since_reset += 5
    dec(cpu, logger, addr)

DEC_ZEROPAGE_X = 0xD6
cdef void dec_zeropage_x(Cpu cpu, CpuLogger logger) except *:
  addr = get_zeropage_x_addr(cpu)
  cpu.clock_ticks_since_reset += 6
  dec(cpu, logger, addr)

DEC_ABSOLUTE = 0xCE
cdef void dec_absolute(Cpu cpu, CpuLogger logger) except *:
  addr = get_absolute_addr(cpu)
  cpu.clock_ticks_since_reset += 6
  dec(cpu, logger, addr)

DEC_ABSOLUTE_X = 0xDE
cdef void dec_absolute_x(Cpu cpu, CpuLogger logger) except *:
  addr, pageCrossed = get_absolute_x_addr(cpu)
  cpu.clock_ticks_since_reset += 7
  dec(cpu, logger, addr)

DEX = 0xCA
cdef void dex(Cpu cpu, CpuLogger logger) except *:
    result = (cpu.X() - 1) % 256
    cpu.set_X(result)
    cpu.set_zero_iff(result == 0)
    cpu.set_negative_iff(is_negative(result))
    cpu.clock_ticks_since_reset += 2
    cpu.set_PC(cpu.PC() + 1)
    logger.log_instruction(cpu)

DEY = 0x88
cdef void dey(Cpu cpu, CpuLogger logger) except *:
  result = (cpu.Y() - 1) % 256
  cpu.set_Y(result)
  cpu.set_zero_iff(result == 0)
  cpu.set_negative_iff(is_negative(result))
  cpu.clock_ticks_since_reset += 2
  cpu.set_PC(cpu.PC() + 1)
  logger.log_instruction(cpu)


cdef void dec(Cpu cpu, CpuLogger logger, int addr) except *:
  result =   (cpu.memory(addr) - 1) % 256
  cpu.set_memory(addr, result)
  cpu.set_zero_iff(result == 0)
  cpu.set_negative_iff(is_negative(result))
  logger.log_memory_access_instruction(cpu, addr, cpu.memory(addr))


INC_ZEROPAGE = 0xE6
cdef void inc_zeropage(Cpu cpu, CpuLogger logger) except *:
  addr = get_zeropage_addr(cpu)
  cpu.clock_ticks_since_reset += 5
  inc(cpu, logger, addr)

INC_ZEROPAGE_X = 0xF6
cdef void inc_zeropage_x(Cpu cpu, CpuLogger logger) except *:
  addr = get_zeropage_x_addr(cpu)
  cpu.clock_ticks_since_reset += 6
  inc(cpu, logger, addr)

INC_ABSOLUTE = 0xEE
cdef void inc_absolute(Cpu cpu, CpuLogger logger) except *:
  addr = get_absolute_addr(cpu)
  cpu.clock_ticks_since_reset += 6
  inc(cpu, logger, addr)

INC_ABSOLUTE_X = 0xFE
cdef void inc_absolute_x(Cpu cpu, CpuLogger logger) except *:
  addr, pageCrossed = get_absolute_x_addr(cpu)
  cpu.clock_ticks_since_reset += 7
  inc(cpu, logger, addr)

INX = 0xE8
cdef void inx(Cpu cpu, CpuLogger logger) except *:
  result = (cpu.X() + 1) % 256
  cpu.set_X(result)
  cpu.set_zero_iff(result == 0)
  cpu.set_negative_iff(is_negative(result))
  cpu.set_PC(cpu.PC() + 1)
  cpu.clock_ticks_since_reset += 2
  logger.log_instruction(cpu)

INY = 0xC8
cdef void iny(Cpu cpu, CpuLogger logger) except *:
  result = (cpu.Y() + 1) % 256
  cpu.set_Y(result)
  cpu.set_zero_iff(result == 0)
  cpu.set_negative_iff(is_negative(result))
  cpu.set_PC(cpu.PC() + 1)
  cpu.clock_ticks_since_reset += 2
  logger.log_instruction(cpu)


cdef void inc(Cpu cpu, CpuLogger logger, int addr) except *:
  result =   (cpu.memory(addr) + 1) % 256 #precisa?
  cpu.set_memory(addr, result)
  cpu.set_zero_iff(result == 0)
  cpu.set_negative_iff(is_negative(result))
  logger.log_memory_access_instruction(cpu, addr, cpu.memory(addr))


SBC_IMMEDIATE = 0xE9
cdef void sbc_immediate(Cpu cpu, CpuLogger logger) except *:
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
cdef void sbc_zeropage(Cpu cpu, CpuLogger logger) except *:
  op2 = get_zeropage_addr(cpu)
  cpu.clock_ticks_since_reset += 3
  sbc(cpu, logger, op2)

SBC_ZEROPAGE_X = 0xF5
cdef void sbc_zeropage_x(Cpu cpu, CpuLogger logger) except *:
  addr = get_zeropage_x_addr(cpu)
  cpu.clock_ticks_since_reset += 4
  sbc(cpu, logger, addr)

SBC_ABSOLUTE = 0xED
cdef void sbc_absolute(Cpu cpu, CpuLogger logger) except *:
  addr = get_absolute_addr(cpu)
  cpu.clock_ticks_since_reset += 4
  sbc(cpu, logger, addr)

SBC_ABSOLUTE_X = 0xFD
cdef void sbc_absolute_x(Cpu cpu, CpuLogger logger) except *:
  addr, pageCrossed = get_absolute_x_addr(cpu)
  cpu.clock_ticks_since_reset += 4 + pageCrossed
  sbc(cpu, logger, addr)

SBC_ABSOLUTE_Y = 0xF9
cdef void sbc_absolute_y(Cpu cpu, CpuLogger logger) except *:
  addr, pageCrossed  = get_absolute_y_addr(cpu)
  cpu.clock_ticks_since_reset += 4 + pageCrossed
  sbc(cpu, logger, addr)

SBC_INDIRECT_X = 0xE1
cdef void sbc_indirect_x(Cpu cpu, CpuLogger logger) except *:
  addr = get_indirect_x_addr(cpu)
  cpu.clock_ticks_since_reset += 6
  sbc(cpu, logger, addr)

SBC_INDIRECT_Y = 0xF1
cdef void sbc_indirect_y(Cpu cpu, CpuLogger logger) except *:
  addr, pageCrossed = get_indirect_y_addr(cpu)
  cpu.clock_ticks_since_reset += 5 + pageCrossed

  sbc(cpu, logger, addr)

cdef void sbc(Cpu cpu, CpuLogger logger, int addr) except *:
  op1 = cpu.A()
  op2 = cpu.memory(addr)
  result = cpu.A() - op2 - (1 - cpu.carry())
  cpu.set_A(result)

  cpu.set_negative_iff(is_negative(cpu.A()))
  cpu.set_overflow_iff(is_sbc_overflow(op1, op2, cpu.A()))
  cpu.set_zero_iff(cpu.A() == 0)
  cpu.set_carry_iff(result >= 0)
  logger.log_memory_access_instruction(cpu, addr, op2)
