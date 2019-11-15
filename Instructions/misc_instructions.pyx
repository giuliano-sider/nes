
from nes_cpu_utils cimport is_negative
from memory_mapper cimport STACK_PAGE_ADDR
from nes_cpu_utils import CpuHalt

BRK = 0x00
cdef void brk(Cpu cpu, CpuLogger logger) except *:
    """In test mode, BRK halts the processor.
       Normally, BRK generates a software interrupt (IRQ with the Break flag set in the pushed value of P)."""
    if cpu.is_test_mode:
        raise CpuHalt('BRK executed in test mode')
    else:
        cpu.clock_ticks_since_reset += 7
        raise NotImplementedError()

TXA = 0x8A
cdef void txa(Cpu cpu, CpuLogger logger) except *:
    cpu.set_A(cpu.X())
    cpu.set_negative_iff(is_negative(cpu.X()))
    cpu.set_zero_iff(cpu.X() == 0)

    cpu.set_PC(cpu.PC() + 1)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

TXS = 0x9A
cdef void txs(Cpu cpu, CpuLogger logger) except *:
    cpu.set_SP(cpu.X())

    cpu.set_PC(cpu.PC() + 1)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

TYA = 0x98
cdef void tya(Cpu cpu, CpuLogger logger) except *:
    cpu.set_A(cpu.Y())
    cpu.set_negative_iff(is_negative(cpu.Y()))
    cpu.set_zero_iff(cpu.Y() == 0)

    cpu.set_PC(cpu.PC() + 1)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

TAY = 0xA8
cdef void tay(Cpu cpu, CpuLogger logger) except *:
    cpu.set_Y(cpu.A())
    cpu.set_negative_iff(is_negative(cpu.A()))
    cpu.set_zero_iff(cpu.A() == 0)

    cpu.set_PC(cpu.PC() + 1)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

TAX = 0xAA
cdef void tax(Cpu cpu, CpuLogger logger) except *:
    cpu.set_X(cpu.A())
    cpu.set_negative_iff(is_negative(cpu.A()))
    cpu.set_zero_iff(cpu.A() == 0)

    cpu.set_PC(cpu.PC() + 1)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

CLV = 0xB8
cdef void clv(Cpu cpu, CpuLogger logger) except *:
    cpu.clear_overflow()

    cpu.set_PC(cpu.PC() + 1)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

TSX = 0xBA
cdef void tsx(Cpu cpu, CpuLogger logger) except *:
    cpu.set_X(cpu.SP())
    cpu.set_negative_iff(is_negative(cpu.SP()))
    cpu.set_zero_iff(cpu.SP() == 0)

    cpu.set_PC(cpu.PC() + 1)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)


CLD = 0xD8
cdef void cld(Cpu cpu, CpuLogger logger) except *:
    cpu.clear_decimal()

    cpu.set_PC(cpu.PC() + 1)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

SED = 0xF8
cdef void sed(Cpu cpu, CpuLogger logger) except *:
    cpu.set_decimal()

    cpu.set_PC(cpu.PC() + 1)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

SEI = 0x78
cdef void sei(Cpu cpu, CpuLogger logger) except *:
    cpu.set_irq_disable()

    cpu.set_PC(cpu.PC() + 1)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)


CLI = 0x58
cdef void cli(Cpu cpu, CpuLogger logger) except *:
    cpu.clear_irq_disable()

    cpu.set_PC(cpu.PC() + 1)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

SEC = 0x38
cdef void sec(Cpu cpu, CpuLogger logger) except *:
    cpu.set_carry()

    cpu.set_PC(cpu.PC()+1)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

CLC = 0x18
cdef void clc(Cpu cpu, CpuLogger logger) except *:
    cpu.clear_carry()

    cpu.set_PC(cpu.PC()+1)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)


NOP = 0xEA
cdef void nop(Cpu cpu, CpuLogger logger) except *:
    cpu.set_PC(cpu.PC() + 1)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)


PHP = 0x08 # excellent language
cdef void php(Cpu cpu, CpuLogger logger) except *:
    affected_addr = STACK_PAGE_ADDR + cpu.SP()
    cpu.push(cpu.P())

    cpu.set_PC(cpu.PC() + 1)
    cpu.clock_ticks_since_reset += 3
    logger.log_memory_access_instruction(cpu, affected_addr, cpu.P())

PLP = 0x28
cdef void plp(Cpu cpu, CpuLogger logger) except *:
    data = cpu.pull()
    cpu.set_P(data)
    affected_addr = STACK_PAGE_ADDR + cpu.SP()

    cpu.set_PC(cpu.PC() + 1)
    cpu.clock_ticks_since_reset += 4
    logger.log_memory_access_instruction(cpu, affected_addr, data)

PHA = 0x48
cdef void pha(Cpu cpu, CpuLogger logger) except *:
    affected_addr = STACK_PAGE_ADDR + cpu.SP()
    cpu.push(cpu.A())

    cpu.set_PC(cpu.PC() + 1)
    cpu.clock_ticks_since_reset += 3
    logger.log_memory_access_instruction(cpu, affected_addr, cpu.A())

PLA = 0x68
cdef void pla(Cpu cpu, CpuLogger logger) except *:
    data = cpu.pull()
    cpu.set_A(data)
    affected_addr = STACK_PAGE_ADDR + cpu.SP()

    cpu.set_PC(cpu.PC() + 1)
    cpu.clock_ticks_since_reset += 4
    logger.log_memory_access_instruction(cpu, affected_addr, data)
