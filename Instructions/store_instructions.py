import nes_cpu_utils as utils

STA_INDIRECT_X = 0x81
def sta_indirect_x(cpu, logger):
    zero_page_address = cpu.memory[cpu.PC() + 1]
    x_offset = cpu.X()
    resolved_address = (zero_page_address + x_offset) % utils.MOD_ZERO_PAGE
    lo_byte_address = cpu.memory[resolved_address]
    hi_byte_address = cpu.memory[resolved_address + 1]
    final_address = lo_byte_address + (hi_byte_address << 8)
    cpu.memory[final_address] = cpu.A()
    cpu.set_PC(cpu.PC() + 2)
    cpu.clock_ticks_since_reset += 6
    logger.log_memory_access_instruction(cpu, final_address, cpu.A())

STA_ZEROPAGE = 0x85
def sta_zeropage(cpu, logger):
    zero_page_address = cpu.memory[cpu.PC() + 1]
    cpu.memory[zero_page_address] = cpu.A()
    cpu.set_PC(cpu.PC() + 2)
    cpu.clock_ticks_since_reset += 3
    logger.log_memory_access_instruction(cpu, zero_page_address, cpu.A())

STA_ABSOLUTE = 0x8D
def sta_absolute(cpu, logger):
    lo_address_byte = cpu.memory[cpu.PC() + 1]
    hi_address_byte = cpu.memory[cpu.PC() + 2]
    cpu.set_PC(cpu.PC() + 3)
    resolved_address_byte = lo_address_byte + (hi_address_byte << 8)
    cpu.memory[resolved_address_byte] = cpu.A()
    cpu.clock_ticks_since_reset += 4
    logger.log_memory_access_instruction(cpu, resolved_address_byte, cpu.A())

STA_INDIRECT_Y = 0x91
def sta_indirect_y(cpu, logger):
    zero_page_address = cpu.memory[cpu.PC() + 1]
    cpu.set_PC(cpu.PC() + 2)
    lo_address_byte = cpu.memory[zero_page_address]
    hi_address_byte = cpu.memory[zero_page_address + 1]
    resolved_address = (lo_address_byte + (hi_address_byte << 8) + cpu.Y()) % utils.MOD_ABSOLUTE
    cpu.memory[resolved_address] = cpu.A()
    cpu.clock_ticks_since_reset += 6
    logger.log_memory_access_instruction(cpu, resolved_address, cpu.A())


STA_ZEROPAGE_X = 0x95
def sta_zeropage_x(cpu, logger):
    zero_page_address = cpu.memory[cpu.PC() + 1]
    cpu.set_PC(cpu.PC() + 2)
    resolved_address = (zero_page_address + cpu.X()) % utils.MOD_ZERO_PAGE
    cpu.memory[resolved_address] = cpu.A()
    cpu.clock_ticks_since_reset += 4
    logger.log_memory_access_instruction(cpu, resolved_address, cpu.A())

STA_ABSOLUTE_Y = 0x99
def sta_absolute_y(cpu, logger):
    lo_byte_address = cpu.memory[cpu.PC() + 1]
    hi_byte_address = cpu.memory[cpu.PC() + 2]
    cpu.set_PC(cpu.PC() + 3)
    resolved_address = (lo_byte_address + (hi_byte_address << 8) + cpu.Y()) % utils.MOD_ABSOLUTE
    cpu.memory[resolved_address] = cpu.A()
    cpu.clock_ticks_since_reset += 5
    logger.log_memory_access_instruction(cpu, resolved_address, cpu.A())


STA_ABSOLUTE_X = 0x9D
def sta_absolute_x(cpu, logger):
    lo_byte_address = cpu.memory[cpu.PC() + 1]
    hi_byte_address = cpu.memory[cpu.PC() + 2]
    cpu.set_PC(cpu.PC() + 3)
    resolved_address = (lo_byte_address + (hi_byte_address << 8) + cpu.X()) % utils.MOD_ABSOLUTE
    cpu.memory[resolved_address] = cpu.A()
    cpu.clock_ticks_since_reset += 5
    logger.log_memory_access_instruction(cpu, resolved_address, cpu.A())

STY_ZEROPAGE = 0x84
def sty_zeropage(cpu, logger):
    zero_page_address = cpu.memory[cpu.PC() + 1]
    cpu.memory[zero_page_address] = cpu.Y()
    cpu.set_PC(cpu.PC() + 2)
    cpu.clock_ticks_since_reset += 3
    logger.log_memory_access_instruction(cpu, zero_page_address, cpu.Y())

STY_ABSOLUTE = 0x8C
def sty_absolute(cpu, logger):
    lo_address_byte = cpu.memory[cpu.PC() + 1]
    hi_address_byte = cpu.memory[cpu.PC() + 2]
    cpu.set_PC(cpu.PC() + 3)
    resolved_address_byte = lo_address_byte + (hi_address_byte << 8)
    cpu.memory[resolved_address_byte] = cpu.Y()
    cpu.clock_ticks_since_reset += 4
    logger.log_memory_access_instruction(cpu, resolved_address_byte, cpu.Y())

STY_ZEROPAGE_X = 0x94
def sty_zeropage_x(cpu, logger):
    zero_page_address = cpu.memory[cpu.PC() + 1]
    cpu.set_PC(cpu.PC() + 2)
    resolved_address = (zero_page_address + cpu.X()) % utils.MOD_ZERO_PAGE
    cpu.memory[resolved_address] = cpu.Y()
    cpu.clock_ticks_since_reset += 4
    logger.log_memory_access_instruction(cpu, resolved_address, cpu.Y())

STX_ZEROPAGE = 0x86
def stx_zeropage(cpu, logger):
    zero_page_address = cpu.memory[cpu.PC() + 1]
    cpu.memory[zero_page_address] = cpu.X()
    cpu.set_PC(cpu.PC() + 2)
    cpu.clock_ticks_since_reset += 3
    logger.log_memory_access_instruction(cpu, zero_page_address, cpu.X())

STX_ABSOLUTE = 0x8E
def stx_absolute(cpu, logger):
    lo_address_byte = cpu.memory[cpu.PC() + 1]
    hi_address_byte = cpu.memory[cpu.PC() + 2]
    cpu.set_PC(cpu.PC() + 3)
    resolved_address_byte = lo_address_byte + (hi_address_byte << 8)
    cpu.memory[resolved_address_byte] = cpu.X()
    cpu.clock_ticks_since_reset += 4
    logger.log_memory_access_instruction(cpu, resolved_address_byte, cpu.X())

STX_ZEROPAGE_Y = 0x96
def stx_zeropage_y(cpu, logger):
    zero_page_address = cpu.memory[cpu.PC() + 1]
    cpu.set_PC(cpu.PC() + 2)
    resolved_address = (zero_page_address + cpu.Y()) % utils.MOD_ZERO_PAGE
    cpu.memory[resolved_address] = cpu.X()
    cpu.clock_ticks_since_reset += 4
    logger.log_memory_access_instruction(cpu, resolved_address, cpu.X())
