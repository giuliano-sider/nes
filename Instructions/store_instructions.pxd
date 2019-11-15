
from cpu cimport Cpu
from log cimport CpuLogger

cdef void sta_indirect_x(Cpu cpu, CpuLogger logger) except *
cdef void sta_zeropage(Cpu cpu, CpuLogger logger) except *
cdef void sta_absolute(Cpu cpu, CpuLogger logger) except *
cdef void sta_indirect_y(Cpu cpu, CpuLogger logger) except *
cdef void sta_zeropage_x(Cpu cpu, CpuLogger logger) except *
cdef void sta_absolute_y(Cpu cpu, CpuLogger logger) except *
cdef void sta_absolute_x(Cpu cpu, CpuLogger logger) except *
cdef void sty_zeropage(Cpu cpu, CpuLogger logger) except *
cdef void sty_absolute(Cpu cpu, CpuLogger logger) except *
cdef void sty_zeropage_x(Cpu cpu, CpuLogger logger) except *
cdef void stx_zeropage(Cpu cpu, CpuLogger logger) except *
cdef void stx_absolute(Cpu cpu, CpuLogger logger) except *
cdef void stx_zeropage_y(Cpu cpu, CpuLogger logger) except *