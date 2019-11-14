# cython: profile=True


import nes_cpu_utils as utils
cimport nes_cpu_utils as utils
from Instructions.address_getters cimport *

LDA_IMMEDIATE = 0xA9
cdef void lda_immediate(Cpu cpu, CpuLogger logger) except *:
    content = cpu.memory(cpu.PC() + 1)
    cpu.set_PC(cpu.PC() + 2)
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_A(content)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

LDA_ZEROPAGE = 0xA5
cdef void lda_zeropage(Cpu cpu, CpuLogger logger) except *:
    cdef int address_8bit = cpu.memory(cpu.PC() + 1)
    cpu.set_PC(cpu.PC() + 2)
    cdef int content = cpu.memory(address_8bit)
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_A(content)
    cpu.clock_ticks_since_reset += 3
    logger.log_memory_access_instruction(cpu, address_8bit, content)

LDA_ABSOLUTE = 0xAD
cdef void lda_absolute(Cpu cpu, CpuLogger logger) except *:
    low_address_part = cpu.memory(cpu.PC() + 1)
    high_address_part = cpu.memory(cpu.PC() + 2) << 8
    cpu.set_PC(cpu.PC() + 3)
    address = low_address_part + high_address_part
    content = cpu.memory(address)
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_A(content)
    cpu.clock_ticks_since_reset += 4
    logger.log_memory_access_instruction(cpu, address, content)

LDA_INDIRECT_Y = 0xB1
cdef void lda_indirect_y(Cpu cpu, CpuLogger logger) except *:
    zero_page_address = cpu.memory(cpu.PC() + 1)
    # cpu.set_PC(cpu.PC() + 2)
    indirect_address_lo = cpu.memory(zero_page_address)
    indirect_address_hi = cpu.memory(zero_page_address + 1) << 8
    indirect_address = indirect_address_lo + indirect_address_hi
    offset_y_address = (indirect_address + cpu.Y()) % 0x10000
    content = cpu.memory(offset_y_address)
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_A(content)
    _ , pageCrossed = get_indirect_y_addr(cpu)
    cpu.clock_ticks_since_reset += 5 + pageCrossed
    logger.log_memory_access_instruction(cpu, offset_y_address, content)


LDA_INDIRECT_X = 0xA1
cdef void lda_indirect_x(Cpu cpu, CpuLogger logger) except *:
    zero_page_address = cpu.memory(cpu.PC() + 1)
    cpu.set_PC(cpu.PC() + 2)
    resolved_address = (cpu.memory(zero_page_address) + cpu.X()) % utils.MOD_ZERO_PAGE
    content = cpu.memory(resolved_address)
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_A(content)
    cpu.clock_ticks_since_reset += 6
    logger.log_memory_access_instruction(cpu, resolved_address, content)


LDA_ABSOLUTE_Y = 0xB9
cdef void lda_absolute_y(Cpu cpu, CpuLogger logger) except *:
    low_address_part = cpu.memory(cpu.PC() + 1)
    high_address_part = cpu.memory(cpu.PC() + 2) << 8
    # cpu.set_PC(cpu.PC()+3)
    address = (low_address_part + high_address_part + cpu.Y()) % utils.MOD_ABSOLUTE
    content = cpu.memory(address)
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_A(content)
    _ , pageCrossed = get_absolute_y_addr(cpu)
    cpu.clock_ticks_since_reset += 4 + pageCrossed
    logger.log_memory_access_instruction(cpu, address, content)

LDA_ABSOLUTE_X = 0xBD
cdef void lda_absolute_x(Cpu cpu, CpuLogger logger) except *:
    low_address_part = cpu.memory(cpu.PC() + 1)
    high_address_part = cpu.memory(cpu.PC() + 2) << 8
    # cpu.set_PC(cpu.PC()+3)
    address = (low_address_part + high_address_part + cpu.X()) % utils.MOD_ABSOLUTE
    content = cpu.memory(address)
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_A(content)
    _ , pageCrossed = get_absolute_x_addr(cpu)
    cpu.clock_ticks_since_reset += 4 + pageCrossed
    logger.log_memory_access_instruction(cpu, address, content)

LDA_ZEROPAGE_X = 0xB5
cdef void lda_zeropage_x(Cpu cpu, CpuLogger logger) except *:
    address_8bit = cpu.memory(cpu.PC() + 1)
    cpu.set_PC(cpu.PC()+2)
    resolved_address = (address_8bit + cpu.X()) % utils.MOD_ZERO_PAGE
    content = cpu.memory(resolved_address)
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_A(content)
    cpu.clock_ticks_since_reset += 4
    logger.log_memory_access_instruction(cpu, resolved_address, content)

LDX_IMMEDIATE = 0xA2
cdef void ldx_immediate(Cpu cpu, CpuLogger logger) except *:
    content = cpu.memory(cpu.PC() + 1)
    cpu.set_PC(cpu.PC() + 2)
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_X(content)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

LDX_ZEROPAGE = 0xA6
cdef void ldx_zeropage(Cpu cpu, CpuLogger logger) except *:
    address_8bit = cpu.memory(cpu.PC() + 1)
    cpu.set_PC(cpu.PC() + 2)
    content = cpu.memory(address_8bit)
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_X(content)
    cpu.clock_ticks_since_reset += 3
    logger.log_memory_access_instruction(cpu, address_8bit, content)


LDX_ABSOLUTE = 0xAE
cdef void ldx_absolute(Cpu cpu, CpuLogger logger) except *:
    low_address_part = cpu.memory(cpu.PC() + 1)
    high_address_part = cpu.memory(cpu.PC() + 2) << 8
    cpu.set_PC(cpu.PC() + 3)
    address = low_address_part + high_address_part
    content = cpu.memory(address)
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_X(content)
    cpu.clock_ticks_since_reset += 4
    logger.log_memory_access_instruction(cpu, address, content)


LDX_ZEROPAGE_Y = 0xB6
cdef void ldx_zeropage_y(Cpu cpu, CpuLogger logger) except *:
    low_address_part = cpu.memory(cpu.PC() + 1)
    cpu.set_PC(cpu.PC() + 2)
    address = (low_address_part + cpu.Y()) % utils.MOD_ZERO_PAGE
    content = cpu.memory(address)
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_X(content)
    cpu.clock_ticks_since_reset += 4
    logger.log_memory_access_instruction(cpu, address, content)

LDX_ABSOLUTE_Y = 0xBE
cdef void ldx_absolute_y(Cpu cpu, CpuLogger logger) except *:
    low_address_part = cpu.memory(cpu.PC() + 1)
    high_address_part = cpu.memory(cpu.PC() + 2) << 8
    # cpu.set_PC(cpu.PC()+3)
    address = (low_address_part + high_address_part + cpu.Y()) % utils.MOD_ABSOLUTE
    content = cpu.memory(address)
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_X(content)
    _ , pageCrossed = get_absolute_y_addr(cpu)
    cpu.clock_ticks_since_reset += 4 + pageCrossed
    logger.log_memory_access_instruction(cpu, address, content)

LDY_IMMEDIATE = 0xA0
cdef void ldy_immediate(Cpu cpu, CpuLogger logger) except *:
    content = cpu.memory(cpu.PC() + 1)
    cpu.set_PC(cpu.PC() + 2)
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_Y(content)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

LDY_ZEROPAGE = 0xA4
cdef void ldy_zeropage(Cpu cpu, CpuLogger logger) except *:
    address_8bit = cpu.memory(cpu.PC() + 1)
    cpu.set_PC(cpu.PC() + 2)
    content = cpu.memory(address_8bit)
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_Y(content)
    cpu.clock_ticks_since_reset += 3
    logger.log_memory_access_instruction(cpu, address_8bit, content)

LDY_ABSOLUTE = 0xAC
cdef void ldy_absolute(Cpu cpu, CpuLogger logger) except *:
    low_address_part = cpu.memory(cpu.PC() + 1)
    high_address_part = cpu.memory(cpu.PC() + 2) << 8
    cpu.set_PC(cpu.PC() + 3)

    address = low_address_part + high_address_part
    content = cpu.memory(address)
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_Y(content)
    cpu.clock_ticks_since_reset += 4
    logger.log_memory_access_instruction(cpu, address, content)

LDY_ZEROPAGE_X = 0xB4
cdef void ldy_zeropage_x(Cpu cpu, CpuLogger logger) except *:
    address_8bit = cpu.memory(cpu.PC() + 1)
    cpu.set_PC(cpu.PC() + 2)
    resolved_address = (address_8bit + cpu.X()) % utils.MOD_ZERO_PAGE
    content = cpu.memory(resolved_address)
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_Y(content)
    cpu.clock_ticks_since_reset += 4
    logger.log_memory_access_instruction(cpu, resolved_address, content)

LDY_ABSOLUTE_X = 0xBC
cdef void ldy_absolute_x(Cpu cpu, CpuLogger logger) except *:
    low_address_part = cpu.memory(cpu.PC() + 1)
    high_address_part = cpu.memory(cpu.PC() + 2) << 8
    # cpu.set_PC(cpu.PC() + 3)
    address = (low_address_part + high_address_part + cpu.X()) % utils.MOD_ABSOLUTE
    content = cpu.memory(address)
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_Y(content)
    _ , pageCrossed = get_absolute_x_addr(cpu)
    cpu.clock_ticks_since_reset += 4 + pageCrossed
    logger.log_memory_access_instruction(cpu, address, content)
