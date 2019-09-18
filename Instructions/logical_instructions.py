from Instructions.address_getters import get_zeropage


BIT_ZEROPAGE = 0x24
def bit_zeropage(cpu, logger):
    op2 = get_zeropage(cpu)
    cpu.set_A(cpu.A() & op2)

    cpu.set_negative_iff(op2 & 0b10000000)
    cpu.set_overflow_iff(op2 & 0b01000000)
    cpu.set_zero_iff(cpu.A() == 0)
