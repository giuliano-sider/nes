from cpu cimport Cpu
from log cimport CpuLogger

cdef (int, int) _dummy_declaration # Cython bug 2745


cdef void lda_immediate(Cpu cpu, CpuLogger logger) except *
cdef void lda_zeropage(Cpu cpu, CpuLogger logger) except *
cdef void lda_absolute(Cpu cpu, CpuLogger logger) except *
cdef void lda_indirect_y(Cpu cpu, CpuLogger logger) except *
cdef void lda_indirect_x(Cpu cpu, CpuLogger logger) except *
cdef void lda_absolute_y(Cpu cpu, CpuLogger logger) except *
cdef void lda_absolute_x(Cpu cpu, CpuLogger logger) except *
cdef void lda_zeropage_x(Cpu cpu, CpuLogger logger) except *

cdef void ldx_immediate(Cpu cpu, CpuLogger logger) except *
cdef void ldx_zeropage(Cpu cpu, CpuLogger logger) except *
cdef void ldx_absolute(Cpu cpu, CpuLogger logger) except *
cdef void ldx_zeropage_y(Cpu cpu, CpuLogger logger) except *
cdef void ldx_absolute_y(Cpu cpu, CpuLogger logger) except *

cdef void ldy_immediate(Cpu cpu, CpuLogger logger) except *
cdef void ldy_zeropage(Cpu cpu, CpuLogger logger) except *
cdef void ldy_absolute(Cpu cpu, CpuLogger logger) except *
cdef void ldy_zeropage_x(Cpu cpu, CpuLogger logger) except *
cdef void ldy_absolute_x(Cpu cpu, CpuLogger logger) except *