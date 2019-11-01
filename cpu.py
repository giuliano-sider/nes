from memory_mapper import RESET_VECTOR, IRQ_VECTOR, NMI_VECTOR, MEMORY_SIZE, STACK_PAGE_ADDR
from instructions import instructions

# flag-related constants:

NEGATIVE       = 0b10000000
CLEAR_NEGATIVE = 0b11111111 - NEGATIVE

OVERFLOW       = 0b01000000
CLEAR_OVERFLOW = 0b11111111 - OVERFLOW

BIT_WITH_NO_FLAG = 0b00100000

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
        self.set_PC(handler_addr)

    def push(self, value):
        self.memory[STACK_PAGE_ADDR + self.SP()] = value
        self.set_SP((self.SP() - 1) % 256)

    def pull(self):
        self.set_SP((self.SP() + 1) % 256)
        return self.memory[STACK_PAGE_ADDR + self.SP()]

    def execute_instruction_at_PC(self, logger):
        opcode = self.memory[self.PC()]
        instructions[opcode](self, logger)

    def run_for_n_cycles(self, num_cycles, logger):
        """Run the CPU for at least num_cycles; return the number of cycles actually elapsed."""
        cycles_start = self.clock_ticks_since_reset
        while self.clock_ticks_since_reset - cycles_start < num_cycles:
            self.execute_instruction_at_PC(logger)
        return self.clock_ticks_since_reset - cycles_start

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
        self.P_ |= BIT_WITH_NO_FLAG | BREAK

    def PC(self):
        return self.PC_
    def PC_hi(self):
        return self.PC() >> 8
    def PC_lo(self):
        return self.PC() & 0xFF
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

    def irq_disable(self):
        """Return value of the interrupt disable flag."""
        return 1 if (self.P_ & IRQ_DISABLE) else 0
