from memory_mapper import RESET_VECTOR, MEMORY_SIZE


# flag-related constants:

NEGATIVE       = 0b10000000
CLEAR_NEGATIVE = 0b11111111 - NEGATIVE

OVERFLOW       = 0b01000000
CLEAR_OVERFLOW = 0b11111111 - OVERFLOW

BREAK       = 0b00010000
CLEAR_BREAK = 0b11111111 - BREAK

DECIMAL       = 0b00001000
CLEAR_DECIMAL = 0b11111111 - DECIMAL

IRQ_DISABLE       = 0b00000100
CLEAR_IRQ_DISABLE = 0b11111111 - IRQ_DISABLE

ZERO       = 0b00000010
CLEAR_ZERO = 0b11111111 - ZERO

CARRY       = 0b00000001
CLEAR_CARRY = 0b11111111 - CARRY


class MemoryAccessor():
    """Allow convenient access to the CPU memory address space."""

    def __init__(self, memory_mapper):
        self.memory_mapper = memory_mapper

    def __getitem__(self, addr):
        return self.memory_mapper.cpu_read_byte(addr)
    def __setitem__(self, addr, value):
        self.memory_mapper.cpu_write_byte(addr, value)

class Cpu():

    def __init__(self, memory_mapper):
        """Instantiate a new CPU linked to the given cartridge memory mapper."""

        self.memory_mapper = memory_mapper
        self.memory = MemoryAccessor(memory_mapper)

        self.A_ = 0
        self.X_ = 0
        self.Y_ = 0
        self.SP_ = 0
        self.P_ = 0 # N V - B D I Z C

        self.Reset()

        self.is_test_mode = True

    # Interrupt vector:

    def trigger_NMI(self, source):
        # TODO: Find out how we should generate interrupts and test the interrupt mechanism.
        raise NotImplementedError()

    def Reset(self):

        self.P_ = IRQ_DISABLE
        self.PC_ = self.memory_mapper.cpu_read_word(RESET_VECTOR)

    def trigger_IRQ(self, source):
        # TODO: Find out how we should generate interrupts and test the interrupt mechanism.
        raise NotImplementedError()


    # Accessors for the registers:

    def A(self):
        return self.A_
    def set_A(self, value):
        self.A_ = value % 256

    def X(self):
        return self.X_
    def set_X(self, value):
        self.X_ = value % 256

    def Y(self):
        return self.Y_
    def set_Y(self, value):
        self.Y_ = value % 256

    def SP(self):
        return self.SP_
    def set_SP(self, value):
        self.SP_ = value % 256

    def P(self):
        return self.P_
    def set_P(self, value):
        self.P_ = value % 256

    def PC(self):
        return self.PC_
    def set_PC(self, value):
        self.PC_ = value % MEMORY_SIZE


    # Accessors for the flags:

    def set_negative_iff(self, condition):
        """Set the flag if condition is true, else clear it."""
        if condition: self.set_negative()
        else:         self.clear_negative()

    def set_overflow_iff(self, condition):
        """Set the flag if condition is true, else clear it."""
        if condition: self.set_overflow()
        else:         self.clear_overflow()

    def set_zero_iff(self, condition):
        """Set the flag if condition is true, else clear it."""
        if condition: self.set_zero()
        else:         self.clear_zero()

    def set_carry_iff(self, condition):
        """Set the flag if condition is true, else clear it."""
        if condition: self.set_carry()
        else:         self.clear_carry()

    def set_negative(self):
        self.P_ |= NEGATIVE
    def clear_negative(self):
        self.P_ &= CLEAR_NEGATIVE

    def set_overflow(self):
        self.P_ |= OVERFLOW
    def clear_overflow(self):
        self.P_ &= CLEAR_OVERFLOW

    def set_break(self):
        self.P_ |= BREAK
    def clear_break(self):
        self.P_ &= CLEAR_BREAK

    def set_decimal(self):
        self.P_ |= DECIMAL
    def clear_decimal(self):
        self.P_ &= CLEAR_DECIMAL

    def set_irq_disable(self):
        self.P_ |= IRQ_DISABLE
    def clear_irq_disable(self):
        self.P_ &= CLEAR_IRQ_DISABLE

    def set_zero(self):
        self.P_ |= ZERO
    def clear_zero(self):
        self.P_ &= CLEAR_ZERO

    def set_carry(self):
        self.P_ |= CARRY
    def clear_carry(self):
        self.P_ &= CLEAR_CARRY

    def negative(self):
        """Return value of the negative flag."""
        return 1 if (self.P_ & NEGATIVE) else 0

    def overflow(self):
        """Return value of the overflow flag."""
        return 1 if (self.P_ & OVERFLOW) else 0

    def zero(self):
        """Return value of the zero flag."""
        return 1 if (self.P_ & ZERO) else 0

    def carry(self):
        """Return value of the carry flag."""
        return 1 if (self.P_ & CARRY) else 0
