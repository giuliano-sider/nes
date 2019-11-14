from cpu cimport Cpu
from log cimport CpuLogger

cdef (int, int) _dummy_declaration # Cython bug 2745

cdef void adc_immediate(Cpu cpu, CpuLogger logger) except *

cdef void adc_zeropage(Cpu cpu, CpuLogger logger) except *

cdef void adc_zeropage_x(Cpu cpu, CpuLogger logger) except *

cdef void adc_absolute(Cpu cpu, CpuLogger logger) except *

cdef void adc_absolute_x(Cpu cpu, CpuLogger logger) except *

cdef void adc_absolute_y(Cpu cpu, CpuLogger logger) except *

cdef void adc_indirect_x(Cpu cpu, CpuLogger logger) except *

cdef void adc_indirect_y(Cpu cpu, CpuLogger logger) except *

cdef void adc(Cpu cpu, CpuLogger logger, int addr) except *


cdef void cmp_immediate(Cpu cpu, CpuLogger logger) except *

cdef void cmp_zeropage(Cpu cpu, CpuLogger logger) except *

cdef void cmp_zero_page_x(Cpu cpu, CpuLogger logger) except *

cdef void cmp_absolute(Cpu cpu, CpuLogger logger) except *

cdef void cmp_absolute_x(Cpu cpu, CpuLogger logger) except *

cdef void cmp_absolute_y(Cpu cpu, CpuLogger logger) except *

cdef void cmp_indirect_x(Cpu cpu, CpuLogger logger) except *

cdef void cmp_indirect_y(Cpu cpu, CpuLogger logger) except *

cdef void cpx_immediate(Cpu cpu, CpuLogger logger) except *

cdef void cpx_zeropage(Cpu cpu, CpuLogger logger) except *

cdef void cpx_absolute(Cpu cpu, CpuLogger logger) except *

cdef void cpy_immediate(Cpu cpu, CpuLogger logger) except *

cdef void cpy_zeropage(Cpu cpu, CpuLogger logger) except *

cdef void cpy_absolute(Cpu cpu, CpuLogger logger) except *

cdef void cmp(Cpu cpu, CpuLogger logger, int op1, int addr) except *


cdef void dec_zeropage(Cpu cpu, CpuLogger logger) except *

cdef void dec_zeropage_x(Cpu cpu, CpuLogger logger) except *

cdef void dec_absolute(Cpu cpu, CpuLogger logger) except *

cdef void dec_absolute_x(Cpu cpu, CpuLogger logger) except *

cdef void dec(Cpu cpu, CpuLogger logger, int addr) except *


cdef void dex(Cpu cpu, CpuLogger logger) except *

cdef void dey(Cpu cpu, CpuLogger logger) except *


cdef void inc_zeropage(Cpu cpu, CpuLogger logger) except *

cdef void inc_zeropage_x(Cpu cpu, CpuLogger logger) except *

cdef void inc_absolute(Cpu cpu, CpuLogger logger) except *

cdef void inc_absolute_x(Cpu cpu, CpuLogger logger) except *

cdef void inc(Cpu cpu, CpuLogger logger, int addr) except *


cdef void inx(Cpu cpu, CpuLogger logger) except *

cdef void iny(Cpu cpu, CpuLogger logger) except *


cdef void sbc_immediate(Cpu cpu, CpuLogger logger) except *

cdef void sbc_zeropage(Cpu cpu, CpuLogger logger) except *

cdef void sbc_zeropage_x(Cpu cpu, CpuLogger logger) except *

cdef void sbc_absolute(Cpu cpu, CpuLogger logger) except *

cdef void sbc_absolute_x(Cpu cpu, CpuLogger logger) except *

cdef void sbc_absolute_y(Cpu cpu, CpuLogger logger) except *

cdef void sbc_indirect_x(Cpu cpu, CpuLogger logger) except *

cdef void sbc_indirect_y(Cpu cpu, CpuLogger logger) except *

cdef void sbc(Cpu cpu, CpuLogger logger, int addr) except *

