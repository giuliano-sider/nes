from nes_cpu_utils import is_negative, is_overflow, twos_comp

ADC_IMMEDIATE = 0x69
def adc_immediate(cpu, logger):
    op2 = cpu.memory[cpu.PC() + 1]
    cpu.set_PC(cpu.PC() + 2)
    adc(cpu, logger, op2)

ADC_ZEROPAGE = 0x65
def adc_zeropage(cpu, logger):
    op2 = cpu.memory[cpu.memory[cpu.PC() + 1]]
    cpu.set_PC(cpu.PC() + 2)
    adc(cpu, logger, op2)

ADC_ZEROPAGEX = 0x75
def adc_zeropage_x(cpu, logger):
    #TODO: wrap zeropage if carry
    op2 = cpu.memory[(cpu.memory[cpu.PC() + 1] + cpu.X()) % 256]
    cpu.set_PC(cpu.PC() + 3)
    adc(cpu, logger, op2)

ADC_ABSOLUTE = 0x6D
def adc_absolute(cpu, logger):
    print("addr ", cpu.memory_mapper.cpu_read_word(cpu.PC() + 1))
    op2 = cpu.memory[cpu.memory_mapper.cpu_read_word(cpu.PC() + 1)]
    cpu.set_PC(cpu.PC() + 3)
    adc(cpu, logger, op2)

def adc(cpu, logger, op2):
    op1 = cpu.A()
    result = cpu.A() + op2 + cpu.carry()
    cpu.set_A(result)

    cpu.set_negative_iff(is_negative(cpu.A()))
    cpu.set_overflow_iff(is_overflow(op1, op2, cpu.A()))
    cpu.set_zero_iff(cpu.A() == 0)
    cpu.set_carry_iff(result >= 256)

    logger.log_instruction(cpu)