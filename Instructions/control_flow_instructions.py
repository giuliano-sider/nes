# 6502 control flow instructions

from nes_cpu_utils import twos_comp

BCC = 0x90
def bcc(cpu, logger):
    if cpu.carry() == 0:
        offset = twos_comp(cpu.memory[cpu.PC()+1], 8) + 2
        oper = cpu.PC() + offset
        branch(cpu, logger, oper)
    else:
        cpu.set_PC(cpu.PC() + 2)
    
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
    
    logger.log_instruction(cpu)

BEQ = 0xf0
def beq(cpu, logger):
    if cpu.zero() == 1:
        offset = twos_comp(cpu.memory[cpu.PC()+1], 8) + 2
        oper = cpu.PC() + offset
        branch(cpu, logger, oper)
    else:
        cpu.set_PC(cpu.PC() + 2)
    
    logger.log_instruction(cpu)

BMI = 0x30
def bmi(cpu, logger):
    if cpu.negative() == 1:
        offset = twos_comp(cpu.memory[cpu.PC()+1], 8) + 2
        oper = cpu.PC() + offset
        branch(cpu, logger, oper)
    else:
        cpu.set_PC(cpu.PC() + 2)
    
    logger.log_instruction(cpu)

BNE = 0xd0
def bne(cpu, logger):
    if cpu.zero() == 0:
        offset = twos_comp(cpu.memory[cpu.PC()+1], 8) + 2
        oper = cpu.PC() + offset
        branch(cpu, logger, oper)
    else:
        cpu.set_PC(cpu.PC() + 2)
    
    logger.log_instruction(cpu)

BPL = 0x10
def bpl(cpu, logger):
    if cpu.negative() == 0:
        offset = twos_comp(cpu.memory[cpu.PC()+1], 8) + 2
        oper = cpu.PC() + offset
        branch(cpu, logger, oper)
    else:
        cpu.set_PC(cpu.PC() + 2)
    
    logger.log_instruction(cpu)

BVC = 0x50
def bvc(cpu, logger):
    if cpu.overflow() == 0:
        offset = twos_comp(cpu.memory[cpu.PC()+1], 8) + 2
        oper = cpu.PC() + offset
        branch(cpu, logger, oper)
    else:
        cpu.set_PC(cpu.PC() + 2)
    
    logger.log_instruction(cpu)

BVS = 0x70
def bvs(cpu, logger):
    if cpu.overflow() == 1:
        offset = twos_comp(cpu.memory[cpu.PC()+1], 8) + 2
        oper = cpu.PC() + offset
        branch(cpu, logger, oper)
    else:
        cpu.set_PC(cpu.PC() + 2)
    
    logger.log_instruction(cpu)

JMP = 0x4c
def jmp_absolute(cpu, logger):
    oper = cpu.memory[cpu.PC()+1] + (cpu.memory[cpu.PC()+2]<<8)
    branch(cpu, logger, oper)
    logger.log_instruction(cpu)
