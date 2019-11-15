
from cpu cimport Cpu
from ppu cimport Ppu
from memory_mapper cimport MemoryMapper
from log cimport CpuLogger
from instructions cimport instructions

cdef (int, int) _dummy_declaration # Cython bug 2745

# cdef class Nes():
    
#     cdef MemoryMapper memory_mapper
#     cdef Cpu cpu
#     cdef Ppu ppu

cpdef inline void execute_instruction_at_PC(Cpu cpu, CpuLogger logger) except *:
    cdef int opcode = cpu.memory(cpu.PC())
    instructions[opcode](cpu, logger)