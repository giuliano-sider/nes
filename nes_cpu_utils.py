import os

MOD_ABSOLUTE = 0x10000
MOD_ZERO_PAGE = 0x100

def is_adc_overflow(addend1, addend2, result):
    assert 0 <= addend1 < 256
    assert 0 <= addend2 < 256
    assert 0 <= result < 256

    return ((is_negative(addend1) and is_negative(addend2) and is_positive(result)) or
            (is_positive(addend1) and is_positive(addend2) and is_negative(result)))

def is_sbc_overflow(op1, op2, result):
    assert 0 <= op1 < 256
    assert 0 <= op2 < 256
    assert 0 <= result < 256

    return ((is_negative(op1) and is_positive(op2) and is_positive(result)) or
            (is_positive(op1) and is_negative(op2) and is_negative(result)))

def is_negative(number):
    assert 0 <= number < 256
    
    return number & 0b10000000

def is_positive(number): # or zero
    assert 0 <= number < 256

    return number & 0b10000000 == 0

def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:      # if sign bit is set 
        val = val - (1 << bits)             # compute negative value
    return val  

