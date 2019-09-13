
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

