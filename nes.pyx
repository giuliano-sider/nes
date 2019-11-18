
from memory_mapper import MemoryMapper
from cpu import Cpu
from ppu import Ppu
from apu import Apu
import sys



A_KEY_PRESSED = 0b00000001
A_KEY_NOT_PRESSED = 0b11111111 - A_KEY_PRESSED

B_KEY_PRESSED = 0b00000010
B_KEY_NOT_PRESSED = 0b11111111 - B_KEY_PRESSED

SELECT_KEY_PRESSED = 0b00000100
SELECT_KEY_NOT_PRESSED = 0b11111111 - SELECT_KEY_PRESSED

START_KEY_PRESSED = 0b00001000
START_KEY_NOT_PRESSED = 0b11111111 - START_KEY_PRESSED

UP_KEY_PRESSED = 0b00010000
UP_KEY_NOT_PRESSED = 0b11111111 - UP_KEY_PRESSED

DOWN_KEY_PRESSED = 0b00100000
DOWN_KEY_NOT_PRESSED = 0b11111111 - DOWN_KEY_PRESSED

LEFT_KEY_PRESSED = 0b01000000
LEFT_KEY_NOT_PRESSED = 0b11111111 - LEFT_KEY_PRESSED

RIGHT_KEY_PRESSED = 0b10000000
RIGHT_KEY_NOT_PRESSED = 0b11111111 - RIGHT_KEY_PRESSED

class Controller():

    def __init__(self):
        self.key_pressed = 0 # Right Left Down Up Start Select B A
        self.shift_register = 0
        self.serial_read_mode = False

    def load_shift_register(self):
        self.shift_register = self.key_pressed
        self.serial_read_mode = False

    def set_serial_read_mode(self):
        self.serial_read_mode = True

    def read_shift_register(self):
        val = self.shift_register & 0b1
        if self.serial_read_mode:
            self.shift_register = (self.shift_register >> 1) | 0b10000000 # Nintendo controllers output all 1's after the buttons are read.
        return val

    def set_A_iff(self, condition):
        if condition: self.set_A()
        else:         self.clear_A()

    def set_A(self):
        self.key_pressed |= A_KEY_PRESSED
        # print('The A button was pressed', file=sys.stderr)

    def clear_A(self):
        self.key_pressed &= A_KEY_NOT_PRESSED

    def set_B_iff(self, condition):
        if condition: self.set_B()
        else:         self.clear_B()

    def set_B(self):
        self.key_pressed |= B_KEY_PRESSED

    def clear_B(self):
        self.key_pressed &= B_KEY_NOT_PRESSED

    def set_Select_iff(self, condition):
        if condition: self.set_Select()
        else:         self.clear_Select()

    def set_Select(self):
        self.key_pressed |= SELECT_KEY_PRESSED

    def clear_Select(self):
        self.key_pressed &= SELECT_KEY_NOT_PRESSED

    def set_Start_iff(self, condition):
        if condition: self.set_Start()
        else:         self.clear_Start()

    def set_Start(self):
        self.key_pressed |= START_KEY_PRESSED

    def clear_Start(self):
        self.key_pressed &= START_KEY_NOT_PRESSED

    def set_Up_iff(self, condition):
        if condition: self.set_Up()
        else:         self.clear_Up()

    def set_Up(self):
        self.key_pressed |= UP_KEY_PRESSED

    def clear_Up(self):
        self.key_pressed &= UP_KEY_NOT_PRESSED

    def set_Down_iff(self, condition):
        if condition: self.set_Down()
        else:         self.clear_Down()

    def set_Down(self):
        self.key_pressed |= DOWN_KEY_PRESSED

    def clear_Down(self):
        self.key_pressed &= DOWN_KEY_NOT_PRESSED

    def set_Left_iff(self, condition):
        if condition: self.set_Left()
        else:         self.clear_Left()

    def set_Left(self):
        self.key_pressed |= LEFT_KEY_PRESSED

    def clear_Left(self):
        self.key_pressed &= LEFT_KEY_NOT_PRESSED

    def set_Right_iff(self, condition):
        if condition: self.set_Right()
        else:         self.clear_Right()

    def set_Right(self):
        self.key_pressed |= RIGHT_KEY_PRESSED

    def clear_Right(self):
        self.key_pressed &= RIGHT_KEY_NOT_PRESSED


def run_for_n_cycles(Cpu cpu, long long num_cycles, CpuLogger logger):
    """Run the CPU for at least num_cycles; return the number of cycles actually elapsed."""
    cdef long long cycles_start = cpu.clock_ticks_since_reset
    cdef long long cycles_end = cycles_start + num_cycles
    while cpu.clock_ticks_since_reset < cycles_end:
        execute_instruction_at_PC(cpu, logger)
    return cpu.clock_ticks_since_reset - cycles_start


class Nes():

    def given_pattern_table_in_address(self, ppu, address, tile):
        current_address = address
        for x in range(0, 8):
            bit_string = ""
            for y in range(0, 8):
                bit_string = bit_string + str(tile[x][y])
            content = int(bit_string, 2)
            ppu.memory[current_address] = content
            current_address = current_address + 1

    def given_image_palette(self, ppu, image_palette):
        palette_start_address = 0x3f00
        for i in range(0, 16):
            ppu.memory[palette_start_address + i] = image_palette[i]
        return

    

    def __init__(self, iNES_file, test_mode=True):
        """Initialize a new Nes instance with the name of an iNES binary file or the binary contents of such a file."""
        self.memory_mapper = MemoryMapper(iNES_file, test_mode)
        self.cpu = Cpu(self.memory_mapper)
        self.ppu = Ppu(self.memory_mapper)
        self.apu = Apu()
        self.controller_1 = Controller()
        self.controller_2 = Controller()
        self.memory_mapper.setup_memory_mapping(self.cpu, self.ppu, self.apu, self.controller_1, self.controller_2)
        
        
