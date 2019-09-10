from memory_mapper import RESET_VECTOR

BREAK       = 0b00010000
CLEAR_BREAK = 0b11111111 - BREAK

IRQ_DISABLE = 0b00000100

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
        raise NotImplementedError()
    def clear_negative(self):
        raise NotImplementedError()

    def set_overflow(self):
        raise NotImplementedError()
    def clear_overflow(self):
        raise NotImplementedError()

    def set_break(self):
        self.P |= BREAK
    def clear_break(self):
        self.P &= CLEAR_BREAK

    def set_decimal(self):
        raise NotImplementedError()
    def clear_decimal(self):
        raise NotImplementedError()

    def set_interrupt_disable(self):
        raise NotImplementedError()
    def clear_interrupt_disable(self):
        raise NotImplementedError()

    def set_zero(self):
        raise NotImplementedError()
    def clear_zero(self):
        raise NotImplementedError()

    def set_carry(self):
        raise NotImplementedError()
    def clear_carry(self):
        raise NotImplementedError()



