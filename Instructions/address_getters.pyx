
"""The helper functions in this module return the value of operand 2
   or the affected address of the instruction for a given addressing mode.
   They have the additional side effect of incrementing PC depending on the
   addressing mode."""

"""Operand getters for the different addressing modes."""

cdef bint isCrossed(int addrA, int addrB) except *:
    if((addrA % 256) == (addrB % 256)):
        return 0
    else:
        return 1


cdef int get_immediate(Cpu cpu) except *:
    op2 = cpu.memory(cpu.PC() + 1)
    cpu.set_PC(cpu.PC() + 2)
    return op2


cdef int get_zeropage(Cpu cpu) except *:
    op2 = cpu.memory(cpu.memory(cpu.PC() + 1))
    cpu.set_PC(cpu.PC() + 2)
    return op2


cdef int get_zeropage_x(Cpu cpu) except *:
    op2 = cpu.memory((cpu.memory(cpu.PC() + 1) + cpu.X()) % 256)
    cpu.set_PC(cpu.PC() + 2)
    return op2


cdef int get_absolute(Cpu cpu) except *:
    op2 = cpu.memory(cpu.memory_mapper.cpu_read_word(cpu.PC() + 1))
    cpu.set_PC(cpu.PC() + 3)
    return op2

cdef int get_absolute_x(Cpu cpu) except *:
    op2 = cpu.memory(cpu.memory_mapper.cpu_read_word(cpu.PC() + 1) + cpu.X())
    cpu.set_PC(cpu.PC() + 3)
    return op2

cdef int get_absolute_y(Cpu cpu) except *:
    op2 = cpu.memory(cpu.memory_mapper.cpu_read_word(cpu.PC() + 1) + cpu.Y())
    cpu.set_PC(cpu.PC() + 3)
    return op2


cdef int get_indirect_x(Cpu cpu) except *:
    zero_page_base_addr = cpu.memory(cpu.PC() + 1)
    addr = (cpu.memory((zero_page_base_addr + cpu.X()    ) % 256) +
           (cpu.memory((zero_page_base_addr + cpu.X() + 1) % 256) << 8))
    op2 = cpu.memory(addr)
    cpu.set_PC(cpu.PC() + 2)
    return op2


cdef int get_indirect_y(Cpu cpu) except *:
    zero_page_base_addr = cpu.memory(cpu.PC() + 1)
    addr = (cpu.memory( zero_page_base_addr           ) +
           (cpu.memory((zero_page_base_addr + 1) % 256) << 8))
    op2 = cpu.memory(addr + cpu.Y())
    cpu.set_PC(cpu.PC() + 2)
    return op2


"""Address getters for several different addressing modes."""

cdef int get_zeropage_addr(Cpu cpu) except *:
    addr = cpu.memory(cpu.PC() + 1)
    cpu.set_PC(cpu.PC() + 2)
    return addr

cdef int get_zeropage_x_addr(Cpu cpu) except *:
    addr = (cpu.memory(cpu.PC() + 1) + cpu.X()) % 256
    cpu.set_PC(cpu.PC() + 2)
    return addr

cdef int get_absolute_addr(Cpu cpu) except *:
    addr = cpu.memory_mapper.cpu_read_word(cpu.PC() + 1)
    cpu.set_PC(cpu.PC() + 3)
    return addr

cdef (int, bint) get_absolute_x_addr(Cpu cpu) except *:
    addr = cpu.memory_mapper.cpu_read_word(cpu.PC() + 1) + cpu.X()
    pageCrossed = isCrossed(cpu.memory_mapper.cpu_read_word(cpu.PC() + 1), (cpu.memory_mapper.cpu_read_word(cpu.PC() + 1) + cpu.X()))
    cpu.set_PC(cpu.PC() + 3)
    return addr, pageCrossed

cdef (int, bint) get_absolute_y_addr(Cpu cpu) except *:
    addr = cpu.memory_mapper.cpu_read_word(cpu.PC() + 1) + cpu.Y()
    pageCrossed = isCrossed(cpu.memory_mapper.cpu_read_word(cpu.PC() + 1), (cpu.memory_mapper.cpu_read_word(cpu.PC() + 1) + cpu.Y()))
    cpu.set_PC(cpu.PC() + 3)
    return addr, pageCrossed

cdef int get_indirect_x_addr(Cpu cpu) except *:
    zero_page_base_addr = cpu.memory(cpu.PC() + 1)
    addr = (cpu.memory((zero_page_base_addr + cpu.X()    ) % 256) +
           (cpu.memory((zero_page_base_addr + cpu.X() + 1) % 256) << 8))
    cpu.set_PC(cpu.PC() + 2)
    return addr

cdef (int, bint) get_indirect_y_addr(Cpu cpu) except *:
    zero_page_base_addr = cpu.memory(cpu.PC() + 1)
    ind = (cpu.memory(zero_page_base_addr) +
           (cpu.memory((zero_page_base_addr + 1) % 256) << 8))
    addr =  ind +  cpu.Y()
    pageCrossed = isCrossed(ind, addr)
    cpu.set_PC(cpu.PC() + 2)
    return addr, pageCrossed