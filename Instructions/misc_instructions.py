from nes_cpu_utils import is_negative

TXA = 0x8A
def txa(cpu, logger):
    cpu.set_A(cpu.X())
    cpu.set_negative_iff(is_negative(cpu.X()))
    cpu.set_zero_iff(cpu.X() == 0)

    cpu.set_PC(cpu.PC() + 1)
    logger.log_instruction(cpu)

TXS = 0x9A
def txs(cpu, logger):
    cpu.set_SP(cpu.X())

    cpu.set_PC(cpu.PC() + 1)
    logger.log_instruction(cpu)

TYA = 0x98
def tya(cpu, logger):
    cpu.set_A(cpu.Y())
    cpu.set_negative_iff(is_negative(cpu.Y()))
    cpu.set_zero_iff(cpu.Y() == 0)

    cpu.set_PC(cpu.PC() + 1)
    logger.log_instruction(cpu)

TAY = 0xA8
def tay(cpu, logger):
    cpu.set_Y(cpu.A())
    cpu.set_negative_iff(is_negative(cpu.A()))
    cpu.set_zero_iff(cpu.A() == 0)

    cpu.set_PC(cpu.PC() + 1)
    logger.log_instruction(cpu)

TAX = 0xAA
def tax(cpu, logger):
    cpu.set_X(cpu.A())
    cpu.set_negative_iff(is_negative(cpu.A()))
    cpu.set_zero_iff(cpu.A() == 0)

    cpu.set_PC(cpu.PC() + 1)
    logger.log_instruction(cpu)

CLV = 0xB8
def clv(cpu, logger):
    cpu.clear_overflow()

    cpu.set_PC(cpu.PC() + 1)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

TSX = 0xBA
def tsx(cpu, logger):
    cpu.set_X(cpu.SP())
    cpu.set_negative_iff(is_negative(cpu.SP()))
    cpu.set_zero_iff(cpu.SP() == 0)

    cpu.set_PC(cpu.PC() + 1)
    logger.log_instruction(cpu)


CLD = 0xD8
def cld(cpu, logger):
    cpu.clear_decimal()

    cpu.set_PC(cpu.PC() + 1)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

SED = 0xF8
def sed(cpu, logger):
    cpu.set_decimal()

    cpu.set_PC(cpu.PC() + 1)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

SEI = 0x78
def sei(cpu, logger):
    cpu.set_irq_disable()

    cpu.set_PC(cpu.PC() + 1)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)


CLI = 0x58
def cli(cpu, logger):
    cpu.clear_irq_disable()

    cpu.set_PC(cpu.PC() + 1)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

SEC = 0x38
def sec(cpu, logger):
    cpu.set_carry()

    cpu.set_PC(cpu.PC()+1)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

CLC = 0x18
def clc(cpu, logger):
    cpu.clear_carry()

    cpu.set_PC(cpu.PC()+1)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)


NOP = 0xEA
def nop(cpu, logger):
    cpu.set_PC(cpu.PC() + 1)
    logger.log_instruction(cpu)


PHP = 0x08 # excellent language
def php(cpu, logger):
    cpu.push(cpu.P())

    cpu.set_PC(cpu.PC() + 1)
    logger.log_instruction(cpu)

PLP = 0x28
def plp(cpu, logger):
    cpu.set_P(cpu.pull())

    cpu.set_PC(cpu.PC() + 1)
    logger.log_instruction(cpu)

PHA = 0x48
def pha(cpu, logger):
    cpu.push(cpu.A())

    cpu.set_PC(cpu.PC() + 1)
    logger.log_instruction(cpu)

PLA = 0x68
def pla(cpu, logger):
    cpu.set_A(cpu.pull())

    cpu.set_PC(cpu.PC() + 1)
    logger.log_instruction(cpu)

