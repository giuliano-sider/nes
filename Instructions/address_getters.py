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


def get_absolute(cpu):
    op2 = cpu.memory[cpu.memory_mapper.cpu_read_word(cpu.PC() + 1)]
    cpu.set_PC(cpu.PC() + 3)
    return op2


def get_absolute_x(cpu):
    op2 = cpu.memory[cpu.memory_mapper.cpu_read_word(cpu.PC() + 1) + cpu.X()]
    cpu.set_PC(cpu.PC() + 3)
    return op2


def get_absolute_y(cpu):
    op2 = cpu.memory[cpu.memory_mapper.cpu_read_word(cpu.PC() + 1) + cpu.Y()]
    cpu.set_PC(cpu.PC() + 3)
    return op2


def get_indirect_x(cpu):
    op2 = cpu.memory[cpu.memory[(cpu.memory[cpu.PC() + 1] + cpu.X()) % 256]]
    cpu.set_PC(cpu.PC() + 2)
    return op2


def get_indirect_y(cpu):
    op2 = cpu.memory[(cpu.memory[cpu.memory[cpu.PC() + 1]] + cpu.Y()) % 256]
    cpu.set_PC(cpu.PC() + 2)
    return op2
