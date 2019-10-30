# 6502 control flow instructions

from nes_cpu_utils import twos_comp
from memory_mapper import MEMORY_SIZE

BCC = 0x90
def bcc(cpu, logger):
    if cpu.carry() == 0:
        offset = twos_comp(cpu.memory[cpu.PC()+1], 8) + 2
        oper = cpu.PC() + offset
        branch(cpu, logger, oper)
    else:
        cpu.set_PC(cpu.PC() + 2)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

def branch(cpu, logger, oper):
    cpu.set_PC(oper)


BCS = 0xb0
def bcs(cpu, logger):
    if cpu.carry() == 1:
        offset = twos_comp(cpu.memory[cpu.PC()+1], 8) + 2
        oper = cpu.PC() + offset
        branch(cpu, logger, oper)
    else:
        cpu.set_PC(cpu.PC() + 2)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

BEQ = 0xf0
def beq(cpu, logger):
    if cpu.zero() == 1:
        offset = twos_comp(cpu.memory[cpu.PC()+1], 8) + 2
        oper = cpu.PC() + offset
        branch(cpu, logger, oper)
    else:
        cpu.set_PC(cpu.PC() + 2)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

BMI = 0x30
def bmi(cpu, logger):
    if cpu.negative() == 1:
        offset = twos_comp(cpu.memory[cpu.PC()+1], 8) + 2
        oper = cpu.PC() + offset
        branch(cpu, logger, oper)
    else:
        cpu.set_PC(cpu.PC() + 2)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

BNE = 0xd0
def bne(cpu, logger):
    if cpu.zero() == 0:
        offset = twos_comp(cpu.memory[cpu.PC()+1], 8) + 2
        oper = cpu.PC() + offset
        branch(cpu, logger, oper)
    else:
        cpu.set_PC(cpu.PC() + 2)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

BPL = 0x10
def bpl(cpu, logger):
    if cpu.negative() == 0:
        offset = twos_comp(cpu.memory[cpu.PC()+1], 8) + 2
        oper = cpu.PC() + offset
        branch(cpu, logger, oper)
    else:
        cpu.set_PC(cpu.PC() + 2)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

BVC = 0x50
def bvc(cpu, logger):
    if cpu.overflow() == 0:
        offset = twos_comp(cpu.memory[cpu.PC()+1], 8) + 2
        oper = cpu.PC() + offset
        branch(cpu, logger, oper)
    else:
        cpu.set_PC(cpu.PC() + 2)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

BVS = 0x70
def bvs(cpu, logger):
    if cpu.overflow() == 1:
        offset = twos_comp(cpu.memory[cpu.PC()+1], 8) + 2
        oper = cpu.PC() + offset
        branch(cpu, logger, oper)
    else:
        cpu.set_PC(cpu.PC() + 2)
    cpu.clock_ticks_since_reset += 2
    logger.log_instruction(cpu)

JMP_ABSOLUTE = 0x4c
def jmp_absolute(cpu, logger):
    oper = cpu.memory[cpu.PC()+1] + (cpu.memory[cpu.PC()+2]<<8)
    branch(cpu, logger, oper)
    cpu.clock_ticks_since_reset += 3
    logger.log_instruction(cpu)

JMP_INDIRECT = 0x6c
def jmp_indirect(cpu, logger):
    LAST_BYTE = 0xFF

    mem = cpu.memory[cpu.PC()+1] + (cpu.memory[cpu.PC()+2]<<8)

    if (mem & LAST_BYTE) == LAST_BYTE:
        high = cpu.memory[mem-LAST_BYTE]<<8
    else:
        high = cpu.memory[mem+1]<<8
    low = cpu.memory[mem]

    oper = low+high

    branch(cpu, logger, oper)
    cpu.clock_ticks_since_reset += 5
    logger.log_instruction(cpu)

JSR = 0x20
def jsr(cpu, logger):
    LOW_ADDR  = 0x00ff
    HIGH_ADDR = 0xff00

    # push PC+2
    pushed_pc = (cpu.PC() + 2) % MEMORY_SIZE
    high = (pushed_pc & HIGH_ADDR) >> 8
    low = pushed_pc & LOW_ADDR
    cpu.push(high)
    cpu.push(low)

    #print("%00x" % (hight))
    #print("%00x" % (low))

    oper = cpu.memory[cpu.PC()+1] + (cpu.memory[cpu.PC()+2] << 8)
    branch(cpu, logger, oper)

    logger.log_instruction(cpu)

RTS = 0x60
def rts(cpu, logger):
    pc_lo = cpu.pull()
    pc_hi = cpu.pull()
    pc = pc_lo + (pc_hi<<8) + 1
    cpu.set_PC(pc)

    logger.log_instruction(cpu)

RTI = 0x40
def rti(cpu, logger):
    cpu.set_P(cpu.pull())
    pc_lo = cpu.pull()
    pc_hi = cpu.pull()
    pc = pc_lo + (pc_hi << 8)
    cpu.set_PC(pc)

    logger.log_instruction(cpu)
