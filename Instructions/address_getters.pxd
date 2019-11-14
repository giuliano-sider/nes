from cpu cimport Cpu

cdef bint isCrossed(int addrA, int addrB) except *

cdef int get_immediate(Cpu cpu) except *

cdef int get_zeropage(Cpu cpu) except *

cdef int get_zeropage_x(Cpu cpu) except *

cdef int get_absolute(Cpu cpu) except *

cdef int get_absolute_x(Cpu cpu) except *

cdef int get_absolute_y(Cpu cpu) except *

cdef int get_indirect_x(Cpu cpu) except *

cdef int get_indirect_y(Cpu cpu) except *

cdef int get_zeropage_addr(Cpu cpu) except *

cdef int get_zeropage_x_addr(Cpu cpu) except *

cdef int get_absolute_addr(Cpu cpu) except *

cdef (int, bint) get_absolute_x_addr(Cpu cpu) except *

cdef (int, bint) get_absolute_y_addr(Cpu cpu) except *

cdef int get_indirect_x_addr(Cpu cpu) except *

cdef (int, bint) get_indirect_y_addr(Cpu cpu) except *
