from cpu cimport Cpu

cdef class CpuLogger():
    
    cdef object output_file
    cdef bint enable_logging

    cdef void log_instruction(self, Cpu cpu)

    cdef void log_memory_access_instruction(self, Cpu cpu, int mem_addr, int data)
