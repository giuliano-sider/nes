
from memory_mapper cimport MemoryMapper, MEMORY_SIZE, STACK_PAGE_ADDR

# flag-related constants:

cdef enum:

    NEGATIVE       = 0b10000000,
    CLEAR_NEGATIVE = 0b11111111 - NEGATIVE,

    OVERFLOW       = 0b01000000,
    CLEAR_OVERFLOW = 0b11111111 - OVERFLOW,

    BIT_WITH_NO_FLAG = 0b00100000,

    BREAK       = 0b00010000,
    CLEAR_BREAK = 0b11111111 - BREAK,

    DECIMAL       = 0b00001000,
    CLEAR_DECIMAL = 0b11111111 - DECIMAL,

    IRQ_DISABLE       = 0b00000100,
    CLEAR_IRQ_DISABLE = 0b11111111 - IRQ_DISABLE,

    ZERO       = 0b00000010,
    CLEAR_ZERO = 0b11111111 - ZERO,

    CARRY       = 0b00000001,
    CLEAR_CARRY = 0b11111111 - CARRY,

# cdef class MemoryAccessor():

#     cdef MemoryMapper memory_mapper



cdef class Cpu():
    
    cdef MemoryMapper memory_mapper
    # cdef MemoryAccessor memory
    cdef int A_, X_, Y_, SP_, P_, PC_
    cdef bint is_test_mode
    cdef long long clock_ticks_since_reset

    cdef inline int memory(self, int addr) except *:
        return self.memory_mapper.cpu_read_byte(addr)

    cdef inline void set_memory(self, int addr, int value) except *:
        self.memory_mapper.cpu_write_byte(addr, value)

    # Stack management methods:

    cdef inline void push(self, int value) except *:
        self.set_memory(STACK_PAGE_ADDR + self.SP(), value)
        self.set_SP((self.SP() - 1) % 256)

    cdef inline int pull(self) except *:
        self.set_SP((self.SP() + 1) % 256)
        return self.memory(STACK_PAGE_ADDR + self.SP())

     # Accessors for the registers:

    cdef inline int A(self) except *:
        return self.A_
    cdef inline void set_A(self, int value) except *:
        self.A_ = value % 256

    cdef inline int X(self) except *:
        return self.X_
    cdef inline void set_X(self, int value) except *:
        self.X_ = value % 256

    cdef inline int Y(self) except *:
        return self.Y_
    cdef inline void set_Y(self, int value) except *:
        self.Y_ = value % 256

    cdef inline int SP(self) except *:
        return self.SP_
    cdef inline void set_SP(self, int value) except *:
        self.SP_ = value % 256

    cdef inline int P(self) except *:
        return self.P_
    cdef inline void set_P(self, int value) except *:
        self.P_ = value % 256
        self.P_ |= BIT_WITH_NO_FLAG | BREAK

    cdef inline int PC(self) except *:
        return self.PC_
    cdef inline int PC_hi(self) except *:
        return self.PC() >> 8
    cdef inline int PC_lo(self) except *:
        return self.PC() & 0xFF
    cdef inline void set_PC(self, int value) except *:
        self.PC_ = value % MEMORY_SIZE


    # Accessors for the flags:

    cdef inline void set_negative_iff(self, bint condition) except *:
        """Set the flag if condition is true, else clear it."""
        if condition: self.set_negative()
        else:         self.clear_negative()

    cdef inline void set_overflow_iff(self, bint condition) except *:
        """Set the flag if condition is true, else clear it."""
        if condition: self.set_overflow()
        else:         self.clear_overflow()

    cdef inline void set_zero_iff(self, bint condition) except *:
        """Set the flag if condition is true, else clear it."""
        if condition: self.set_zero()
        else:         self.clear_zero()

    cdef inline void set_carry_iff(self, bint condition) except *:
        """Set the flag if condition is true, else clear it."""
        if condition: self.set_carry()
        else:         self.clear_carry()

    cdef inline void set_negative(self) except *:
        self.P_ |= NEGATIVE
    cdef inline void clear_negative(self) except *:
        self.P_ &= CLEAR_NEGATIVE

    cdef inline void set_overflow(self) except *:
        self.P_ |= OVERFLOW
    cdef inline void clear_overflow(self) except *:
        self.P_ &= CLEAR_OVERFLOW

    cdef inline void set_decimal(self) except *:
        self.P_ |= DECIMAL
    cdef inline void clear_decimal(self) except *:
        self.P_ &= CLEAR_DECIMAL

    cdef inline void set_irq_disable(self) except *:
        self.P_ |= IRQ_DISABLE
    cdef inline void clear_irq_disable(self) except *:
        self.P_ &= CLEAR_IRQ_DISABLE

    cdef inline void set_zero(self) except *:
        self.P_ |= ZERO
    cdef inline void clear_zero(self) except *:
        self.P_ &= CLEAR_ZERO

    cdef inline void set_carry(self) except *:
        self.P_ |= CARRY
    cdef inline void clear_carry(self) except *:
        self.P_ &= CLEAR_CARRY

    cdef inline int negative(self) except *:
        """Return value of the negative flag."""
        return 1 if (self.P_ & NEGATIVE) else 0

    cdef inline int overflow(self) except *:
        """Return value of the overflow flag."""
        return 1 if (self.P_ & OVERFLOW) else 0

    cdef inline int zero(self) except *:
        """Return value of the zero flag."""
        return 1 if (self.P_ & ZERO) else 0

    cdef inline int carry(self) except *:
        """Return value of the carry flag."""
        return 1 if (self.P_ & CARRY) else 0

    cdef inline int irq_disable(self) except *:
        """Return value of the interrupt disable flag."""
        return 1 if (self.P_ & IRQ_DISABLE) else 0
