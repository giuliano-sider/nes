from memory_mapper import RESET_VECTOR

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

        self.A = 0
        self.X = 0
        self.Y = 0
        self.SP = 0
        self.P = 0 # N V - B D I Z C

        self.Reset()

        self.is_test_mode = True

    # Interrupt vector:

    def trigger_NMI(self, source):
        # TODO: Find out how we should generate interrupts and test the interrupt mechanism.
        raise NotImplementedError()
    
    def Reset(self):

        self.P = IRQ_DISABLE
        self.PC = self.memory_mapper.cpu_read_word(RESET_VECTOR)

    def trigger_IRQ(self, source):
        # TODO: Find out how we should generate interrupts and test the interrupt mechanism.
        raise NotImplementedError()

    # Accessors for the flags:

    def set_negative(self):
        self.P |= NEGATIVE
    def clear_negative(self):
        self.P &= CLEAR_NEGATIVE

    def set_overflow(self):
        self.P |= OVERFLOW
    def clear_overflow(self):
        self.P &= CLEAR_OVERFLOW

    def set_break(self):
        self.P |= BREAK
    def clear_break(self):
        self.P &= CLEAR_BREAK

    def set_decimal(self):
        self.P |= DECIMAL
    def clear_decimal(self):
        self.P &= CLEAR_DECIMAL

    def set_irq_disable(self):
        self.P |= IRQ_DISABLE
    def clear_irq_disable(self):
        self.P &= CLEAR_IRQ_DISABLE

    def set_zero(self):
        self.P |= ZERO
    def clear_zero(self):
        self.P &= CLEAR_ZERO

    def set_carry(self):
        self.P |= CARRY
    def clear_carry(self):
        self.P &= CLEAR_CARRY



