# cython: profile=True

import cython
from memory_mapper cimport RESET_VECTOR, IRQ_VECTOR, NMI_VECTOR

# import cython
# if cython.compiled:
#     print("cpu.py is cython compiled")
# else:
#     print("cpu.py is not cython compiled")





# cdef class MemoryAccessor():
#     """Allow convenient access to the CPU memory address space."""

#     def __init__(self, MemoryMapper memory_mapper):
#         self.memory_mapper = memory_mapper

#     @cython.returns(cython.int)
#     def __getitem__(self, int addr):
#         return self.memory_mapper.cpu_read_byte(addr)

#     @cython.returns(cython.void)
#     def __setitem__(self, int addr, int value):
#         self.memory_mapper.cpu_write_byte(addr, value)


cdef class Cpu():

    def __init__(self, memory_mapper):
        """Instantiate a new CPU linked to the given cartridge memory mapper."""

        self.memory_mapper = memory_mapper
        # self.memory = MemoryAccessor(memory_mapper)

        self.A_ = 0
        self.X_ = 0
        self.Y_ = 0
        self.SP_ = 0xFD
        # Invariant: both fictitious flags ("-" and "B") are set so that they appear as 1 in the instruction log tests.
        self.P_ = BIT_WITH_NO_FLAG | BREAK | IRQ_DISABLE # N V - B D I Z C

        self.Reset()

        self.is_test_mode = True

        # TODO: Increment this correctly for each instruction.
        self.clock_ticks_since_reset = 0

    # Interrupt vector:

    def trigger_NMI(self, source):
        # TODO: Find out how we should generate interrupts and test the interrupt mechanism.
        self.generate_interrupt(self.memory_mapper.cpu_read_word(NMI_VECTOR))

    def Reset(self):
        """Carry out the 2 guaranteed operations on a 6502 Reset."""
        self.set_irq_disable()
        self.set_PC(self.memory_mapper.cpu_read_word(RESET_VECTOR))

    def trigger_IRQ(self, source):
        # TODO: Find out how we should generate interrupts and test the interrupt mechanism.
        if not self.irq_disable():
            self.generate_interrupt(self.memory_mapper.cpu_read_word(IRQ_VECTOR))

    # Various helper methods:

    def generate_interrupt(self, handler_addr):
        """Generate a non-BRK interrupt handled by code at @param handler_addr."""
        self.push(self.PC_hi())
        self.push(self.PC_lo())
        self.push(self.P() & CLEAR_BREAK)
        self.set_irq_disable()
        self.clock_ticks_since_reset += 7
        self.set_PC(handler_addr)

    def tick_clock(self, int num_ticks):
        self.clock_ticks_since_reset += num_ticks

