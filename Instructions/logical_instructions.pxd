
from cpu cimport Cpu
from log cimport CpuLogger

cdef (int, int) _dummy_declaration # Cython bug 2745


cdef void bit_zeropage(Cpu cpu, CpuLogger logger) except *

cdef void bit_absolute(Cpu cpu, CpuLogger logger) except *

cdef void bit(Cpu cpu, CpuLogger logger, int addr) except *


cdef void and_immediate(Cpu cpu, CpuLogger logger) except *

cdef void and_zeropage(Cpu cpu, CpuLogger logger) except *

cdef void and_zeropage_x(Cpu cpu, CpuLogger logger) except *

cdef void and_absolute(Cpu cpu, CpuLogger logger) except *

cdef void and_absolute_x(Cpu cpu, CpuLogger logger) except *

cdef void and_absolute_y(Cpu cpu, CpuLogger logger) except *

cdef void and_indirect_x(Cpu cpu, CpuLogger logger) except *

cdef void and_indirect_y(Cpu cpu, CpuLogger logger) except *

cdef void and_instruction(Cpu cpu, CpuLogger logger, int addr) except *


cdef void eor_immediate(Cpu cpu, CpuLogger logger) except *

cdef void eor_zeropage(Cpu cpu, CpuLogger logger) except *

cdef void eor_zeropage_x(Cpu cpu, CpuLogger logger) except *

cdef void eor_absolute(Cpu cpu, CpuLogger logger) except *

cdef void eor_absolute_x(Cpu cpu, CpuLogger logger) except *

cdef void eor_absolute_y(Cpu cpu, CpuLogger logger) except *

cdef void eor_indirect_x(Cpu cpu, CpuLogger logger) except *

cdef void eor_indirect_y(Cpu cpu, CpuLogger logger) except *

cdef void eor_instruction(Cpu cpu, CpuLogger logger, int addr) except *


cdef void ora_immediate(Cpu cpu, CpuLogger logger) except *

cdef void ora_zeropage(Cpu cpu, CpuLogger logger) except *

cdef void ora_zeropage_x(Cpu cpu, CpuLogger logger) except *

cdef void ora_absolute(Cpu cpu, CpuLogger logger) except *

cdef void ora_absolute_x(Cpu cpu, CpuLogger logger) except *

cdef void ora_absolute_y(Cpu cpu, CpuLogger logger) except *

cdef void ora_indirect_x(Cpu cpu, CpuLogger logger) except *

cdef void ora_indirect_y(Cpu cpu, CpuLogger logger) except *

cdef void ora_instruction(Cpu cpu, CpuLogger logger, int addr) except *


cdef void asl_accumulator(Cpu cpu, CpuLogger logger) except *

cdef void asl_zeropage(Cpu cpu, CpuLogger logger) except *

cdef void asl_zeropage_x(Cpu cpu, CpuLogger logger) except *

cdef void asl_absolute(Cpu cpu, CpuLogger logger) except *

cdef void asl_absolute_x(Cpu cpu, CpuLogger logger) except *

cdef void asl(Cpu cpu, CpuLogger logger, int addr) except *


cdef void lsr_accumulator(Cpu cpu, CpuLogger logger) except *

cdef void lsr_zeropage(Cpu cpu, CpuLogger logger) except *

cdef void lsr_zeropage_x(Cpu cpu, CpuLogger logger) except *

cdef void lsr_absolute(Cpu cpu, CpuLogger logger) except *

cdef void lsr_absolute_x(Cpu cpu, CpuLogger logger) except *

cdef void lsr(Cpu cpu, CpuLogger logger, int addr) except *


cdef void rol_accumulator(Cpu cpu, CpuLogger logger) except *

cdef void rol_zeropage(Cpu cpu, CpuLogger logger) except *

cdef void rol_zeropage_x(Cpu cpu, CpuLogger logger) except *

cdef void rol_absolute(Cpu cpu, CpuLogger logger) except *

cdef void rol_absolute_x(Cpu cpu, CpuLogger logger) except *

cdef void rol(Cpu cpu, CpuLogger logger, int addr) except *


cdef void ror_accumulator(Cpu cpu, CpuLogger logger) except *

cdef void ror_zeropage(Cpu cpu, CpuLogger logger) except *

cdef void ror_zeropage_x(Cpu cpu, CpuLogger logger) except *

cdef void ror_absolute(Cpu cpu, CpuLogger logger) except *

cdef void ror_absolute_x(Cpu cpu, CpuLogger logger) except *

cdef void ror(Cpu cpu, CpuLogger logger, int addr) except *



