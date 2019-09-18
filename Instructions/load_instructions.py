import nes_cpu_utils as utils

LDA_IMMEDIATE = 0xA9
def lda_immediate(cpu, logger):
    content = cpu.memory[cpu.PC() + 1]
    cpu.set_PC(cpu.PC() + 2)
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_A(content)
    logger.log_instruction(cpu)

LDA_ZEROPAGE = 0xA5
def lda_zeropage(cpu, logger):
    address_8bit = cpu.memory[cpu.PC() + 1]
    cpu.set_PC(cpu.PC() + 2)
    content = cpu.memory[address_8bit]
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_A(content)
    logger.log_instruction(cpu)

LDA_ABSOLUTE = 0xAD
def lda_absolute(cpu, logger):
    low_address_part = cpu.memory[cpu.PC() + 1]
    high_address_part = cpu.memory[cpu.PC() + 2] << 8
    cpu.set_PC(cpu.PC() + 3)
    address = low_address_part + high_address_part
    content = cpu.memory[address]
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_A(content)
    logger.log_instruction(cpu)

LDA_INDIRECT_Y = 0xB1
def lda_indirect_y(cpu, logger):
    zero_page_address = cpu.memory[cpu.PC() + 1]
    cpu.set_PC(cpu.PC() + 2)
    indirect_address_lo = cpu.memory[zero_page_address]
    indirect_address_hi = cpu.memory[zero_page_address + 1] << 8
    indirect_address = indirect_address_lo + indirect_address_hi
    offset_y_address = (indirect_address + cpu.Y()) % 0x10000
    content = cpu.memory[offset_y_address]
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_A(content)
    logger.log_instruction(cpu)


LDA_INDIRECT_X = 0xA1
def lda_indirect_x(cpu, logger): # TODO: add pc behavior
    zero_page_address = cpu.memory[cpu.PC() + 1]
    resolved_address = (cpu.memory[zero_page_address] + cpu.X()) % utils.MOD_ZERO_PAGE
    content = cpu.memory[resolved_address]
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_A(content)
    logger.log_instruction(cpu)


LDA_ABSOLUTE_Y = 0xB9
def lda_absolute_y(cpu, logger): # TODO: add pc behavior
    low_address_part = cpu.memory[cpu.PC() + 1]
    high_address_part = cpu.memory[cpu.PC() + 2] << 8
    address = (low_address_part + high_address_part + cpu.Y()) % utils.MOD_ABSOLUTE
    content = cpu.memory[address]
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_A(content)
    logger.log_instruction(cpu)

LDA_ABSOLUTE_X = 0xBD
def lda_absolute_x(cpu, logger): # TODO: add pc behavior
    low_address_part = cpu.memory[cpu.PC() + 1]
    high_address_part = cpu.memory[cpu.PC() + 2] << 8
    address = (low_address_part + high_address_part + cpu.X()) % utils.MOD_ABSOLUTE
    content = cpu.memory[address]
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_A(content)
    logger.log_instruction(cpu)

LDA_ZEROPAGE_X = 0xB5
def lda_zeropage_x(cpu, logger): # TODO: add pc behavior
    address_8bit = cpu.memory[cpu.PC() + 1]
    content = cpu.memory[(address_8bit + cpu.X()) % utils.MOD_ZERO_PAGE]
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_A(content)
    logger.log_instruction(cpu)

LDX_IMMEDIATE = 0xA2
def ldx_immediate(cpu, logger): # TODO: add pc behavior
    content = cpu.memory[cpu.PC() + 1]
    cpu.set_PC(cpu.PC() + 2)
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_X(content)
    logger.log_instruction(cpu)

LDX_ZEROPAGE = 0xA6
def ldx_zeropage(cpu, logger): # TODO: add pc behavior
    address_8bit = cpu.memory[cpu.PC() + 1]
    content = cpu.memory[address_8bit]
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_X(content)
    logger.log_instruction(cpu)


LDX_ABSOLUTE = 0xAE
def ldx_absolute(cpu, logger): # TODO: add pc behavior
    low_address_part = cpu.memory[cpu.PC() + 1]
    high_address_part = cpu.memory[cpu.PC() + 2] << 8
    address = low_address_part + high_address_part
    content = cpu.memory[address]
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_X(content)
    logger.log_instruction(cpu)


LDX_ZEROPAGE_Y = 0xB6
def ldx_zeropage_y(cpu, logger): # TODO: add pc behavior
    low_address_part = cpu.memory[cpu.PC() + 1]
    high_address_part = cpu.memory[cpu.PC() + 2] << 8
    address = (low_address_part + high_address_part + cpu.Y()) % utils.MOD_ABSOLUTE
    content = cpu.memory[address]
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_X(content)
    logger.log_instruction(cpu)

LDX_ABSOLUTE_Y = 0xBE
def ldx_absolute_y(cpu, logger):
    # to be implemented OPCODE be
    raise NotImplementedError()

LDY_IMMEDIATE = 0xA0
def ldy_immediate(cpu, logger): # TODO: add pc behavior
    content = cpu.memory[cpu.PC() + 1]
    cpu.set_PC(cpu.PC() + 2)
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_Y(content)
    logger.log_instruction(cpu)

LDY_ZEROPAGE = 0xA4
def ldy_zeropage(cpu, logger): # TODO: add pc behavior
    address_8bit = cpu.memory[cpu.PC() + 1]
    content = cpu.memory[address_8bit]
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_Y(content)
    logger.log_instruction(cpu)

LDY_ABSOLUTE = 0xAC
def ldy_absolute(cpu, logger): # TODO: add pc behavior
    low_address_part = cpu.memory[cpu.PC() + 1]
    high_address_part = cpu.memory[cpu.PC() + 2] << 8
    address = low_address_part + high_address_part
    content = cpu.memory[address]
    cpu.set_zero_iff(content == 0x00)
    cpu.set_negative_iff(utils.is_negative(content))
    cpu.set_Y(content)
    logger.log_instruction(cpu)

LDY_ZEROPAGE_X = 0xB4
def ldy_zeropage_x(cpu, logger): # TODO: add pc behavior
    # to be implemented OPCODE b4
    raise NotImplementedError()

LDY_ABSOLUTE_X = 0xBC
def ldy_absolute_x(cpu, logger): # TODO: add pc behavior
    # to be implemented OPCODE bc
    raise NotImplementedError()

