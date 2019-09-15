import os

MOD_ABSOLUTE = 0x10000
MOD_ZERO_PAGE = 0x100

def is_overflow(addend1, addend2, sum):
    assert 0 <= addend1 < 256
    assert 0 <= addend2 < 256
    assert 0 <= sum < 256

    return ((is_negative(addend1) and is_negative(addend2) and is_positive(sum)) or
            (is_positive(addend1) and is_positive(addend2) and is_negative(sum)))

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

