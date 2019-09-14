import sys
sys.path += os.curdir

def get_immediate(cpu):
	op2 = cpu.memory[cpu.PC() + 1]
    cpu.set_PC(cpu.PC() + 2)
    return op2

def get_zeropage(cpu):
	op2 = cpu.memory[cpu.memory[cpu.PC() + 1]]
    cpu.set_PC(cpu.PC() + 2)
    return op2

def get_zeropage_x(cpu):
	op2 = cpu.memory[(cpu.memory[cpu.PC() + 1] + cpu.X()) % 256]
    cpu.set_PC(cpu.PC() + 2)
    return op2