
from enum import Enum
import nes_ppu_utils as ppu_utils

# include "memory_mapper.pxi"

"""iNES format related constants"""

NROM_128_PRG_ROM_ADDR = 0xC000 # 1 bank of 16KiB program ROM
NROM_256_PRG_ROM_ADDR = 0x8000 # 2 banks of 16KiB program ROM


iNES_HEADER_MAGIC_NUMBER = b'NES\x1A'
iNES_HEADER_LENGTH = 16

HORIZONTAL_NAMETABLE_MIRRORING = 0b0
VERTICAL_NAMETABLE_MIRRORING = 0b1

NROM_MAPPER = 0


"""Helper functions"""

cdef int cpu_unmirrored_address(int addr) except *:
    cdef int register
    addr %= MEMORY_SIZE
    if addr < RAM_REGION_END:
        addr %= RAM_SIZE
    elif addr < PPU_REGISTERS_REGION_END:
        register = addr % PPU_NUM_REGISTERS # Note that PPU_REGISTERS_REGION_BEGIN is divisble by PPU_NUM_REGISTERS.
        addr = PPU_REGISTERS_REGION_BEGIN + register
    # TODO: Implement mirroring of PRG ROM banks for NROM-128 mapper cartridges.
    # In that case, which is the "real" address, the bank at 0x8000 or the one at 0xC000 ??
    return addr

cdef int ppu_unmirrored_address(int addr) except *:
    addr = addr % 0x4000
    if addr < 0x2000:
        return addr
    elif addr < 0x3000:  # TODO: nametable mirroring
        return addr
    elif ppu_utils.is_universal_background_palette(addr):
        return PPU_IMAGE_PALETTE_BASE
    else:
        return PPU_IMAGE_PALETTE_BASE + addr % PPU_IMAGE_PALETTE_GENERAL_OFFSET

cdef void copy_to_c_array(uint8_t *c_array, bytearray b_array) except *:
    cdef int i
    cdef uint8_t byte
    for i, byte in enumerate(b_array):
        c_array[i] = byte


"""Emulator support classes"""

class CpuMemoryRegion(Enum):
    ram = 1
    ppu_registers = 2

class Invalid_iNES_FileException(Exception):
    pass

class NoEmulatorSupportException(Exception):
    pass

cdef class MemoryMapper():
    """Represent the memory access logic as seen by the CPU and PPU.
       Note: some accesses may have side effects (for example, I/O registers).
    """

    def __init__(self, iNES_file, test_mode=True):
        """Initialize a MemoryMapper based on the contents of an iNES cartridge file.
           iNES_file can be a string filename or a bytes object with the contents of the file.
        """

        if type(iNES_file) is str: # filename of an iNES cartridge file
            with open(iNES_file, 'rb') as f:
                iNES_file = f.read()
        assert(type(iNES_file) is bytes)

        if len(iNES_file) < iNES_HEADER_LENGTH:
            raise Invalid_iNES_FileException('iNES file has length %d and cannot possibly have a complete header' % len(iNES_file))
        if iNES_file[0:4] != iNES_HEADER_MAGIC_NUMBER:
            raise Invalid_iNES_FileException('Invalid value for iNES file magic number: %s' % iNES_file[0:4])
        
        self.prg_rom_size = iNES_file[4] # in 16KB units
        self.chr_rom_size = iNES_file[5] # in 8KB units
        self.ppu_nametable_mirroring = iNES_file[6] & 0b1
        self.has_cartridge_ram = iNES_file[6] & 0b10 # battery-backed cartridge RAM at [$6000, $8000)
        self.has_trainer = iNES_file[6] & 0b100 # trainer at [$7000, $7200)
        self.has_four_screen_vram = iNES_file[6] & 0b1000 # no mirroring: all four PPU nametables are distinct
        self.mapper_id = (iNES_file[7] & 0b11110000) | (iNES_file[6] >> 4)

        if self.mapper_id != NROM_MAPPER:
            raise NoEmulatorSupportException('Only the NROM mapper is supported by this emulator (selected mapper = %d)' % self.mapper_id)
        if self.has_cartridge_ram:
            raise NoEmulatorSupportException('Cartridge RAM is not supported by this emulator')
        if self.has_trainer:
            raise NoEmulatorSupportException('Trainer is not supported by this emulator')
        if self.has_four_screen_vram:
            raise NoEmulatorSupportException('Four screen VRAM is not supported by this emulator')

        # TODO: Find a way to break the somewhat odd circular dependency between cpu/ppu and memory mapper.
        self.cpu_ = None
        self.ppu_ = None
        self.apu_ = None
        self.controller_1_ = None
        self.controller_2_ = None

        self.init_NROM_mapper(iNES_file)

        # if test_mode is True:
        #     self.cpu_write_byte = self.cpu_force_write_byte # No regard for memory mapping of CPU address space. Pure write through to memory.
        # else:
        #     self.cpu_write_byte = self.cpu_write_byte_to_mapped_memory

    def init_NROM_mapper(self, iNES_file):
        """Initialize the CPU and PPU address spaces, 
           supporting both NROM-128 (1 16KiB bank of PRG ROM) and NROM-256 (2 16KiB banks of PRG ROM).
        """

        cpu_memory = bytearray(MEMORY_SIZE)
        ppu_memory = bytearray(MEMORY_SIZE)

        iNES_file_index = iNES_HEADER_LENGTH

        # set up PRG ROM banks
        if self.prg_rom_size == 1:
            if len(iNES_file) < iNES_file_index + PRG_ROM_BANK_SIZE:
                raise Invalid_iNES_FileException('Couldnt read first bank of PRG ROM as the file was too short (length %d)' % len(iNES_file))
            cpu_memory[LOWER_PRG_ROM_BANK : LOWER_PRG_ROM_BANK + PRG_ROM_BANK_SIZE] = iNES_file[iNES_file_index : iNES_file_index + PRG_ROM_BANK_SIZE]
            # mirrored second bank:
            cpu_memory[UPPER_PRG_ROM_BANK : UPPER_PRG_ROM_BANK + PRG_ROM_BANK_SIZE] = cpu_memory[LOWER_PRG_ROM_BANK : LOWER_PRG_ROM_BANK + PRG_ROM_BANK_SIZE]
            iNES_file_index += PRG_ROM_BANK_SIZE
        elif self.prg_rom_size == 2:
            if len(iNES_file) < iNES_file_index + 2*PRG_ROM_BANK_SIZE:
                raise Invalid_iNES_FileException('Couldnt read 2 banks of PRG ROM as the file was too short (length %d)' % len(iNES_file))
            cpu_memory[LOWER_PRG_ROM_BANK : LOWER_PRG_ROM_BANK + 2*PRG_ROM_BANK_SIZE] = iNES_file[iNES_file_index : iNES_file_index + 2*PRG_ROM_BANK_SIZE]
            iNES_file_index += 2*PRG_ROM_BANK_SIZE
        else:
            raise Invalid_iNES_FileException('Only NROM-128 and NROM-256 variants are supported by the NROM mapper (selected number of 16KB PRG ROM banks = %d)' % self.prg_rom_size)
        
        # set CHR ROM bank
        if self.chr_rom_size == 1:
            if len(iNES_file) < iNES_file_index + CHR_ROM_BANK_SIZE:
                raise Invalid_iNES_FileException('Couldnt read bank of CHR ROM as the file was too short (length %d)' % len(iNES_file))
            ppu_memory[CHR_ROM_BANK : CHR_ROM_BANK + CHR_ROM_BANK_SIZE] = iNES_file[iNES_file_index : iNES_file_index + CHR_ROM_BANK_SIZE]
            iNES_file_index += CHR_ROM_BANK_SIZE
        else:
            raise Invalid_iNES_FileException('NROM mapper supports only 8KB of CHR ROM (selected number of 8KB CHR ROM banks = %d)' % self.chr_rom_size)

        copy_to_c_array(self.cpu_memory_, cpu_memory)
        copy_to_c_array(self.ppu_memory_, ppu_memory)


    def setup_memory_mapping(self, cpu, ppu, apu, controller_1, controller_2):
        self.cpu_ = cpu
        self.ppu_ = ppu
        self.apu_ = apu
        self.controller_1_ = controller_1
        self.controller_2_ = controller_2

        self.register_writers_ = {
            FIRST_PULSE_CONTROL: self.apu_.write_p1_control,
            FIRST_PULSE_SWEEP_CONTROL: self.apu_.write_p1_sweep_control,
            FIRST_PULSE_LOW_BITS_TIMER: self.apu_.write_p1_low_bits_timer,
            FIRST_PULSE_HI_BITS_TIMER: self.apu_.write_p1_hi_bits_timer,
            SECOND_PULSE_CONTROL: self.apu_.write_p2_control,
            SECOND_PULSE_SWEEP_CONTROL: self.apu_.write_p2_sweep_control,
            SECOND_PULSE_LOW_BITS_TIMER: self.apu_.write_p2_low_bits_timer,
            SECOND_PULSE_HI_BITS_TIMER: self.apu_.write_p2_hi_bits_timer,
            TRIANGLE_WAVE_LINEAR_COUNTER: self.apu_.write_triangle_wave_linear_counter,
            TRIANGLE_WAVE_UNUSED_REGISTER: self.apu_.write_dummy,
            TRIANGLE_WAVE_LOW_BITS_PERIOD: self.apu_.write_triangle_wave_low_bits_period,
            TRIANGLE_WAVE_HI_BITS_PERIOD: self.apu_.write_triangle_wave_hi_bits_period,
            NOISE_VOLUME_CONTROL: self.apu_.write_noise_volume_control,
            NOISE_UNUSED_REGISTER: self.apu_.write_dummy,
            NOISE_PERIOD_AND_WAVEFORM_SHAPE: self.apu_.write_noise_period_and_waveform_shape,
            NOISE_LENGTH_COUNTER_LOAD_AND_ENVELOPE_RESTART: self.apu_.write_noise_length_counter_load_and_envelope_restart,
            DMC_FREQ: self.apu_.write_dmc_freq,
            DMC_RAW: self.apu_.write_dmc_raw,
            DMC_START: self.apu_.write_dmc_start,
            DMC_LEN: self.apu_.write_dmc_len,
            OAMDMA: self.ppu_.write_oamdma,
            APU_STATUS: self.apu_.write_apu_control,
            JOYPAD_1: self.write_joypad_1,
            JOYPAD_2_AND_APU_FRAME_COUNTER: self.apu_.write_apu_frame_counter
        }

        # Note that the only readable APU register is APU_STATUS.
        self.register_readers_ = {
            FIRST_PULSE_CONTROL: self.apu_.read_p1_control,
            FIRST_PULSE_SWEEP_CONTROL: self.apu_.read_p1_sweep_control,
            FIRST_PULSE_LOW_BITS_TIMER: self.apu_.read_p1_low_bits_timer,
            FIRST_PULSE_HI_BITS_TIMER: self.apu_.read_p1_hi_bits_timer,
            SECOND_PULSE_CONTROL: self.apu_.read_p1_control,
            SECOND_PULSE_SWEEP_CONTROL: self.apu_.read_p2_sweep_control,
            SECOND_PULSE_LOW_BITS_TIMER: self.apu_.read_p2_low_bits_timer,
            SECOND_PULSE_HI_BITS_TIMER: self.apu_.read_p2_hi_bits_timer,
            TRIANGLE_WAVE_LINEAR_COUNTER: self.apu_.read_triangle_wave_linear_counter,
            TRIANGLE_WAVE_UNUSED_REGISTER: self.apu_.read_dummy,
            TRIANGLE_WAVE_LOW_BITS_PERIOD: self.apu_.read_triangle_wave_low_bits_period,
            TRIANGLE_WAVE_HI_BITS_PERIOD: self.apu_.read_triangle_wave_hi_bits_period,
            NOISE_VOLUME_CONTROL: self.apu_.read_noise_volume_control,
            NOISE_UNUSED_REGISTER: self.apu_.read_dummy,
            NOISE_PERIOD_AND_WAVEFORM_SHAPE: self.apu_.read_noise_period_and_waveform_shape,
            NOISE_LENGTH_COUNTER_LOAD_AND_ENVELOPE_RESTART: self.apu_.read_noise_length_counter_load_and_envelope_restart,
            DMC_FREQ: self.apu_.read_dmc_freq,
            DMC_RAW: self.apu_.read_dmc_raw,
            DMC_START: self.apu_.read_dmc_start,
            DMC_LEN: self.apu_.read_dmc_len,
            OAMDMA: self.ppu_.read_oamdma,
            APU_STATUS: self.apu_.read_apu_status,
            JOYPAD_1: self.read_joypad_1,
            JOYPAD_2_AND_APU_FRAME_COUNTER: self.read_joypad_2
        }
    
    def write_joypad_1(self, value):
        """Write a value to the JOYPAD_1 I/O port, which affects the state of both controller 1 and 2."""
        if value & 0b1: 
            self.controller_1_.load_shift_register()
            self.controller_2_.load_shift_register()
        else:
            self.controller_1_.set_serial_read_mode()
            self.controller_2_.set_serial_read_mode()

    def read_joypad_1(self):
        return self.controller_1_.read_shift_register()

    def read_joypad_2(self):
        return self.controller_2_.read_shift_register()

    cdef int cpu_read_byte(self, int addr) except *:
        cdef int register
        addr %= MEMORY_SIZE
        if addr >= APU_REGISTERS_REGION_END: # ROM or non-existing memory which returns 0.
            return self.cpu_memory_[addr]
        elif addr < RAM_REGION_END:
            addr %= RAM_SIZE
            return self.cpu_memory_[addr]
        elif addr < PPU_REGISTERS_REGION_END:
            register = addr % PPU_NUM_REGISTERS # Note that PPU_REGISTERS_REGION_BEGIN is divisble by PPU_NUM_REGISTERS.
            addr = PPU_REGISTERS_REGION_BEGIN + register
            return self.ppu_.read_register(addr)
        else: # Only case left is: addr < APU_REGISTERS_REGION_END:
            return self.register_readers_[addr]()

    cdef void cpu_write_byte(self, int addr, int value) except *:
        """Write a byte to memory taking into account the proper regions of the CPU address space."""
        cdef int register
        addr %= MEMORY_SIZE
        if addr < RAM_REGION_END:
            addr %= RAM_SIZE
            self.cpu_memory_[addr] = value % 256
        elif addr < PPU_REGISTERS_REGION_END:
            register = addr % PPU_NUM_REGISTERS # Note that PPU_REGISTERS_REGION_BEGIN is divisble by PPU_NUM_REGISTERS.
            addr = PPU_REGISTERS_REGION_BEGIN + register
            self.ppu_.write_register(addr, value % 256)
        elif addr < APU_REGISTERS_REGION_END:
            self.register_writers_[addr](value % 256)
        # else: write nothing: non-existing memory or ROM.

