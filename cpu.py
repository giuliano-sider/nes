from memory_mapper import RESET_VECTOR

IRQ_DISABLE = 0b00000100
BREAK       = 0b00010000

class Cpu():

    def __init__(self, memory_mapper):

        self.memory_mapper = memory_mapper

        self.A = 0
        self.X = 0
        self.Y = 0
        self.SP = 0
        self.P = 0 # N V - B D I Z C

        self.Reset()

        self.is_test_mode = True

    def trigger_NMI(self, source):

        raise NotImplementedError()
    
    def Reset(self):

        self.P = IRQ_DISABLE
        self.PC = self.memory_mapper.cpu_read_word(RESET_VECTOR)

    def trigger_IRQ(self, source):

        raise NotImplementedError()

    def set_break(self):
        self.P |= BREAK

