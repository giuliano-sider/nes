"""The helper functions in this module return the value of operand 2
   or the affected address of the instruction for a given addressing mode.
   They have the additional side effect of incrementing PC depending on the
   addressing mode."""

"""Operand getters for the different addressing modes."""

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
    zero_page_base_addr = cpu.memory[cpu.PC() + 1]
    addr = (cpu.memory[(zero_page_base_addr + cpu.X()    ) % 256] +
           (cpu.memory[(zero_page_base_addr + cpu.X() + 1) % 256] << 8))
    op2 = cpu.memory[addr]
    cpu.set_PC(cpu.PC() + 2)
    return op2


def get_indirect_y(cpu):
    zero_page_base_addr = cpu.memory[cpu.PC() + 1]
    addr = (cpu.memory[ zero_page_base_addr           ] +
           (cpu.memory[(zero_page_base_addr + 1) % 256] << 8))
    op2 = cpu.memory[addr + cpu.Y()]
    cpu.set_PC(cpu.PC() + 2)
    return op2


"""Address getters for several different addressing modes."""

def get_zeropage_addr(cpu):
    addr = cpu.memory[cpu.PC() + 1]
    cpu.set_PC(cpu.PC() + 2)
    return addr

def get_zeropage_x_addr(cpu):
    addr = (cpu.memory[cpu.PC() + 1] + cpu.X()) % 256
    cpu.set_PC(cpu.PC() + 2)
    return addr

def get_absolute_addr(cpu):
    addr = cpu.memory_mapper.cpu_read_word(cpu.PC() + 1)
    cpu.set_PC(cpu.PC() + 3)
    return addr

def get_absolute_x_addr(cpu):
    addr = cpu.memory_mapper.cpu_read_word(cpu.PC() + 1) + cpu.X()
    cpu.set_PC(cpu.PC() + 3)
    return addr

def get_absolute_y_addr(cpu):
    addr = cpu.memory_mapper.cpu_read_word(cpu.PC() + 1) + cpu.Y()
    cpu.set_PC(cpu.PC() + 3)
    return addr

def get_indirect_x_addr(cpu):
    zero_page_base_addr = cpu.memory[cpu.PC() + 1]
    addr = (cpu.memory[(zero_page_base_addr + cpu.X()    ) % 256] +
           (cpu.memory[(zero_page_base_addr + cpu.X() + 1) % 256] << 8))
    cpu.set_PC(cpu.PC() + 2)
    return addr

def get_indirect_y_addr(cpu):
    zero_page_base_addr = cpu.memory[cpu.PC() + 1]
    addr = (cpu.memory[ zero_page_base_addr           ] +
           (cpu.memory[(zero_page_base_addr + 1) % 256] << 8) +
            cpu.Y())
    cpu.set_PC(cpu.PC() + 2)
    return addr