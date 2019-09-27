
"""NES memory related constants"""

MEMORY_SIZE = 0x10000 # 64KiB CPU and PPU address spaces

# CPU

STACK_PAGE_ADDR = 0x0100

LOWER_PRG_ROM_BANK = 0x8000
UPPER_PRG_ROM_BANK = 0xC000
PRG_ROM_BANK_SIZE = 0x4000 # 16KiB

NMI_VECTOR = 0xFFFA
RESET_VECTOR = 0xFFFC
IRQ_VECTOR = 0xFFFE

# PPU

CHR_ROM_BANK = 0x0000
CHR_ROM_BANK_SIZE = 0x2000 # 8KiB



"""iNES format related constants"""

NROM_128_PRG_ROM_ADDR = 0xC000 # 1 bank of 16KiB program ROM
NROM_256_PRG_ROM_ADDR = 0x8000 # 2 banks of 16KiB program ROM


iNES_HEADER_MAGIC_NUMBER = b'NES\x1A'
iNES_HEADER_LENGTH = 16

HORIZONTAL_NAMETABLE_MIRRORING = 0b0
VERTICAL_NAMETABLE_MIRRORING = 0b1

NROM_MAPPER = 0


"""Emulator support classes"""

class Invalid_iNES_FileException(Exception):
    pass

class NoEmulatorSupportException(Exception):
    pass

class MemoryMapper():
    """Represent the memory access logic as seen by the CPU and PPU.
       Note: some accesses may have side effects (for example, I/O registers).
    """

    def __init__(self, iNES_file):
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

        self.init_NROM_mapper(iNES_file)

    def init_NROM_mapper(self, iNES_file):
        """Initialize the CPU and PPU address spaces, 
           supporting both NROM-128 (1 16KiB bank of PRG ROM) and NROM-256 (2 16KiB banks of PRG ROM).
        """

        self.cpu_memory = bytearray(MEMORY_SIZE)
        self.ppu_memory = bytearray(MEMORY_SIZE)

        iNES_file_index = iNES_HEADER_LENGTH

        # set up PRG ROM banks
        if self.prg_rom_size == 1:
            if len(iNES_file) < iNES_file_index + PRG_ROM_BANK_SIZE:
                raise Invalid_iNES_FileException('Couldnt read first bank of PRG ROM as the file was too short (length %d)' % len(iNES_file))
            self.cpu_memory[LOWER_PRG_ROM_BANK : LOWER_PRG_ROM_BANK + PRG_ROM_BANK_SIZE] = iNES_file[iNES_file_index : iNES_file_index + PRG_ROM_BANK_SIZE]
            # mirrored second bank:
            self.cpu_memory[UPPER_PRG_ROM_BANK : UPPER_PRG_ROM_BANK + PRG_ROM_BANK_SIZE] = self.cpu_memory[LOWER_PRG_ROM_BANK : LOWER_PRG_ROM_BANK + PRG_ROM_BANK_SIZE]
            iNES_file_index += PRG_ROM_BANK_SIZE
        elif self.prg_rom_size == 2:
            if len(iNES_file) < iNES_file_index + 2*PRG_ROM_BANK_SIZE:
                raise Invalid_iNES_FileException('Couldnt read 2 banks of PRG ROM as the file was too short (length %d)' % len(iNES_file))
            self.cpu_memory[LOWER_PRG_ROM_BANK : LOWER_PRG_ROM_BANK + 2*PRG_ROM_BANK_SIZE] = iNES_file[iNES_file_index : iNES_file_index + 2*PRG_ROM_BANK_SIZE]
            iNES_file_index += 2*PRG_ROM_BANK_SIZE
        else:
            raise Invalid_iNES_FileException('Only NROM-128 and NROM-256 variants are supported by the NROM mapper (selected number of 16KB PRG ROM banks = %d)' % self.prg_rom_size)
        
        # set CHR ROM bank
        if self.chr_rom_size == 1:
            if len(iNES_file) < iNES_file_index + CHR_ROM_BANK_SIZE:
                raise Invalid_iNES_FileException('Couldnt read bank of CHR ROM as the file was too short (length %d)' % len(iNES_file))
            self.ppu_memory[CHR_ROM_BANK : CHR_ROM_BANK + CHR_ROM_BANK_SIZE] = iNES_file[iNES_file_index : iNES_file_index + CHR_ROM_BANK_SIZE]
            iNES_file_index += CHR_ROM_BANK_SIZE
        else:
            raise Invalid_iNES_FileException('NROM mapper supports only 8KB of CHR ROM (selected number of 8KB CHR ROM banks = %d)' % self.chr_rom_size)


    def cpu_read_byte(self, addr):
        return self.cpu_memory[addr % MEMORY_SIZE]

    def cpu_write_byte(self, addr, value):
        self.cpu_memory[addr % MEMORY_SIZE] = value % 256

    def cpu_read_word(self, addr):
        """Return the contents of a 2-byte word located in the CPU address space given by @param addr.
           The read wraps around to zero at 64KiB.
        """
        return self.cpu_memory[addr % MEMORY_SIZE] + (self.cpu_memory[(addr + 1) % MEMORY_SIZE] << 8)
