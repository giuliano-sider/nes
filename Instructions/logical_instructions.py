from Instructions.address_getters import get_zeropage, get_absolute


BIT_ZEROPAGE = 0x24
def bit_zeropage(cpu, logger):
    bit(cpu, logger, get_zeropage(cpu))

BIT_ABSOLUTE = 0x2C
def bit_absolute(cpu, logger):
    bit(cpu, logger, get_absolute(cpu))

def bit(cpu, logger, op2):
    cpu.set_A(cpu.A() & op2)

    cpu.set_negative_iff(op2 & 0b10000000)
    cpu.set_overflow_iff(op2 & 0b01000000)
    cpu.set_zero_iff(cpu.A() == 0)
