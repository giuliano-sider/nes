
from cpu cimport Cpu
from log cimport CpuLogger

cdef void brk(Cpu cpu, CpuLogger logger) except *

cdef void txa(Cpu cpu, CpuLogger logger) except *

cdef void txs(Cpu cpu, CpuLogger logger) except *

cdef void tya(Cpu cpu, CpuLogger logger) except *

cdef void tay(Cpu cpu, CpuLogger logger) except *

cdef void tax(Cpu cpu, CpuLogger logger) except *

cdef void clv(Cpu cpu, CpuLogger logger) except *

cdef void tsx(Cpu cpu, CpuLogger logger) except *

cdef void cld(Cpu cpu, CpuLogger logger) except *

cdef void sed(Cpu cpu, CpuLogger logger) except *

cdef void sei(Cpu cpu, CpuLogger logger) except *

cdef void cli(Cpu cpu, CpuLogger logger) except *

cdef void sec(Cpu cpu, CpuLogger logger) except *

cdef void clc(Cpu cpu, CpuLogger logger) except *

cdef void nop(Cpu cpu, CpuLogger logger) except *

cdef void php(Cpu cpu, CpuLogger logger) except *

cdef void plp(Cpu cpu, CpuLogger logger) except *

cdef void pha(Cpu cpu, CpuLogger logger) except *

cdef void pla(Cpu cpu, CpuLogger logger) except *
