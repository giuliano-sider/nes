from cpu cimport Cpu
from log cimport CpuLogger

cdef inline void branch(Cpu cpu, CpuLogger logger, int oper) except *:
    cpu.set_PC(oper)

cdef void bcc(Cpu cpu, CpuLogger logger) except *
cdef void bcs(Cpu cpu, CpuLogger logger) except *
cdef void beq(Cpu cpu, CpuLogger logger) except *
cdef void bmi(Cpu cpu, CpuLogger logger) except *
cdef void bne(Cpu cpu, CpuLogger logger) except *
cdef void bpl(Cpu cpu, CpuLogger logger) except *
cdef void bvc(Cpu cpu, CpuLogger logger) except *
cdef void bvs(Cpu cpu, CpuLogger logger) except *

cdef void jmp_absolute(Cpu cpu, CpuLogger logger) except *
cdef void jmp_indirect(Cpu cpu, CpuLogger logger) except *
cdef void jsr(Cpu cpu, CpuLogger logger) except *

cdef void rts(Cpu cpu, CpuLogger logger) except *
cdef void rti(Cpu cpu, CpuLogger logger) except *
