
from libc.stdint cimport uint8_t

"""NES memory related constants"""

cdef enum:

    MEMORY_SIZE = 0x10000, # 64KiB CPU and PPU address spaces

    # CPU

    STACK_PAGE_ADDR = 0x0100,

    RAM_SIZE = 0x0800,
    RAM_REGION_BEGIN = 0x0000,
    RAM_REGION_END = 0x2000,

    PPU_NUM_REGISTERS = 0x0008,
    PPU_REGISTERS_REGION_BEGIN = 0x2000,
    PPU_REGISTERS_REGION_END = 0x4000,
    APU_NUM_REGISTERS = 0xF

    LOWER_PRG_ROM_BANK = 0x8000,
    UPPER_PRG_ROM_BANK = 0xC000,
    PRG_ROM_BANK_SIZE = 0x4000 # 16KiB,

    NMI_VECTOR = 0xFFFA,
    RESET_VECTOR = 0xFFFC,
    IRQ_VECTOR = 0xFFFE,

    # PPU

    CHR_ROM_BANK = 0x0000,
    CHR_ROM_BANK_SIZE = 0x2000  # 8KiB,
    PPU_IMAGE_PALETTE_BASE = 0x3F00,
    PPU_IMAGE_PALETTE_BACKGROUND_OFFSET = 0x4,
    PPU_IMAGE_PALETTE_GENERAL_OFFSET = 0x20,

    OAMDMA = 0x4014,

    # APU and peripherals:
    
    APU_REGISTERS_REGION_BEGIN = 0x4000
    APU_REGISTERS_REGION_END = 0x4018

    FIRST_PULSE_CONTROL = 0x4000,
    FIRST_PULSE_SWEEP_CONTROL = 0x4001,
    FIRST_PULSE_LOW_BITS_TIMER = 0x4002,
    FIRST_PULSE_HI_BITS_TIMER = 0x4003,

    SECOND_PULSE_CONTROL = 0x4004,
    SECOND_PULSE_SWEEP_CONTROL = 0x4005,
    SECOND_PULSE_LOW_BITS_TIMER = 0x4006,
    SECOND_PULSE_HI_BITS_TIMER = 0x4007,

    TRIANGLE_WAVE_LINEAR_COUNTER = 0x4008,
    TRIANGLE_WAVE_UNUSED_REGISTER = 0x4009,
    TRIANGLE_WAVE_LOW_BITS_PERIOD = 0x400A,
    TRIANGLE_WAVE_HI_BITS_PERIOD = 0x400B,

    NOISE_VOLUME_CONTROL = 0x400C,
    NOISE_UNUSED_REGISTER = 0x400D,
    NOISE_PERIOD_AND_WAVEFORM_SHAPE = 0x400E,
    NOISE_LENGTH_COUNTER_LOAD_AND_ENVELOPE_RESTART = 0x400F,

    DMC_FREQ = 0x4010,
    DMC_RAW = 0x4011,
    DMC_START = 0x4012,
    DMC_LEN = 0x4013,

    # OAMDMA
    APU_STATUS = 0x4015,
    JOYPAD_1 = 0x4016,
    JOYPAD_2_AND_APU_FRAME_COUNTER = 0x4017




cdef int cpu_unmirrored_address(int addr) except *

cdef int ppu_unmirrored_address(int addr) except *

cdef inline bint is_palette_addr(int addr):
    addr %= 0x4000
    return addr >= PPU_IMAGE_PALETTE_BASE


cdef class MemoryMapper():

    cdef uint8_t cpu_memory_[MEMORY_SIZE]

    cdef uint8_t ppu_memory_[MEMORY_SIZE]

    cdef int prg_rom_size # in 16KB units
    cdef int chr_rom_size # in 8KB units
    cdef int ppu_nametable_mirroring
    cdef int has_cartridge_ram
    cdef int has_trainer
    cdef int has_four_screen_vram
    cdef int mapper_id

    cdef object cpu_
    cdef object ppu_
    cdef object apu_
    cdef object controller_1_
    cdef object controller_2_

    cdef dict register_writers_
    cdef dict register_readers_

    cdef inline object cpu(self):
        return self.cpu_

    cdef inline int ppu_read_byte(self, int addr) except *:
        return self.ppu_memory_[ppu_unmirrored_address(addr)]

    cdef inline void ppu_write_byte(self, int addr, int value) except *:
        # TODO: Prevent writing to read-only memory and memory that doesn't exist.
        self.ppu_memory_[ppu_unmirrored_address(addr)] = value % 256


    cdef inline void cpu_force_write_byte(self, int addr, int value) except *:
        """Write a byte to memory, even if it corresponds to a special region like ROM or the PPU registers."""
        self.cpu_memory_[cpu_unmirrored_address(addr)] = value % 256

    # cdef void cpu_write_byte_to_mapped_memory(self, int addr, int value)
    cdef void cpu_write_byte(self, int addr, int value) except *

    cdef int cpu_read_byte(self, int addr) except *

    cdef inline int cpu_read_word(self, int addr) except *:
        """Return the contents of a 2-byte word located in the CPU address space given by @param addr.
           The read wraps around to zero at 64KiB.
        """
        return self.cpu_read_byte(addr) + (self.cpu_read_byte(addr + 1) << 8)
