
LDA_IMMEDIATE = 0xA9
def lda_immediate(cpu, logger):
    op2 = cpu.memory[cpu.PC() + 1]
    cpu.set_PC(cpu.PC() + 2)
    if op2 == 0x00:
        cpu.set_zero()
    if op2 > 0x7f:
        cpu.set_negative()
    cpu.set_A(op2)
    logger.log_instruction(cpu)

LDA_ZEROPAGE = 0xA5
def lda_zeropage(cpu, logger):
    lda_immediate(cpu, logger)

LDA_ABSOLUTE = 0xAD
def lda_absolute(cpu, logger):
    # to be implemented OPCODE ad
    raise NotImplementedError()

LDA_INDIRECT_Y = 0xB1
def lda_indirect_y(cpu, logger):
    # to be implemented OPCODE b1
    raise NotImplementedError()

LDA_INDIRECT_X = 0xA1
def lda_indirect_x(cpu, logger):
    # to be implemented OPCODE a1
    raise NotImplementedError()

def lda_absolute_y(cpu, logger):
    # to be implemented OPCODE b9
    raise NotImplementedError()

def lda_absolute_x(cpu, logger):
    # to be implemented OPCODE bd
    raise NotImplementedError()

def lda_zeropage_x(cpu, logger):
    # to be implemented OPCODE b5
    raise NotImplementedError()

def ldx_immediate(cpu, logger):
    # to be implemented OPCODE a2
    raise NotImplementedError()

def ldx_zeropage(cpu, logger):
    # to be implemented OPCODE a6
    raise NotImplementedError()


def ldx_absolute(cpu, logger):
    # to be implemented OPCODE ae
    raise NotImplementedError()

def ldx_zeropage_y(cpu, logger):
    # to be implemented OPCODE b6
    raise NotImplementedError()

def ldx_absolute_y(cpu, logger):
    # to be implemented OPCODE be
    raise NotImplementedError()

def ldy_immediate(cpu, logger):
    # to be implemented OPCODE a0
    raise NotImplementedError()

def ldy_zeropage(cpu, logger):
    # to be implemented OPCODE a4
    raise NotImplementedError()

def ldy_absolute(cpu, logger):
    # to be implemented OPCODE ac
    raise NotImplementedError()

def ldy_zeropage_x(cpu, logger):
    # to be implemented OPCODE b4
    raise NotImplementedError()

def ldy_absolute_x(cpu, logger):
    # to be implemented OPCODE bc
    raise NotImplementedError()

