
cdef inline bint is_adc_overflow(int addend1, int addend2, int result) except *:
    assert 0 <= addend1 < 256
    assert 0 <= addend2 < 256
    assert 0 <= result < 256

    return ((is_negative(addend1) and is_negative(addend2) and is_positive(result)) or
            (is_positive(addend1) and is_positive(addend2) and is_negative(result)))

cdef inline bint is_sbc_overflow(int op1, int op2, int result) except *:
    assert 0 <= op1 < 256
    assert 0 <= op2 < 256
    assert 0 <= result < 256

    return ((is_negative(op1) and is_positive(op2) and is_positive(result)) or
            (is_positive(op1) and is_negative(op2) and is_negative(result)))

cdef inline bint is_negative(int number) except *:
    assert 0 <= number < 256
    
    return number & 0b10000000

cdef inline bint is_positive(int number) except *: # or zero
    assert 0 <= number < 256

    return number & 0b10000000 == 0

cdef inline int twos_comp(int val, int bits) except *:
    if (val & (1 << (bits - 1))) != 0:      # if sign bit is set 
        val = val - (1 << bits)             # compute negative value
    return val 