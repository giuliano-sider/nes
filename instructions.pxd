
from cpu cimport Cpu
from log cimport CpuLogger

cdef (int, int) _dummy_declaration # Cython bug 2745

ctypedef void (*CpuInstructionHandler)(Cpu, CpuLogger) except *

cdef CpuInstructionHandler instructions[256]

