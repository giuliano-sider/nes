#!/usr/bin/env python3

import sys
import os
import unittest
from datetime import datetime

sys.path += os.pardir
from nes_cpu_test_utils import CreateTestCpu, execute_instruction
from log import FAKE_LOGGER
from instructions import *


valid_opcodes = {
    ADC_IMMEDIATE: 'ADC_IMMEDIATE',
    ADC_ZEROPAGE: 'ADC_ZEROPAGE',
    ADC_ZEROPAGEX: 'ADC_ZEROPAGEX',
    ADC_ABSOLUTE: 'ADC_ABSOLUTE',
    ADC_ABSOLUTE_X: 'ADC_ABSOLUTE_X',
    ADC_ABSOLUTE_Y: 'ADC_ABSOLUTE_Y',
    ADC_INDIRECT_X: 'ADC_INDIRECT_X',
    ADC_INDIRECT_Y: 'ADC_INDIRECT_Y',

    AND_IMMEDIATE: 'AND_IMMEDIATE',
    AND_ZERO_PAGE: 'AND_ZERO_PAGE',
    AND_ZERO_PAGE_X: 'AND_ZERO_PAGE_X',
    AND_ABSOLUTE: 'AND_ABSOLUTE',
    AND_ABSOLUTE_X: 'AND_ABSOLUTE_X',
    AND_ABSOLUTE_Y: 'AND_ABSOLUTE_Y',
    AND_INDIRECT_X: 'AND_INDIRECT_X',
    AND_INDIRECT_Y: 'AND_INDIRECT_Y',

    ASL_ACCUMULATOR: 'ASL_ACCUMULATOR',
    ASL_ZERO_PAGE: 'ASL_ZERO_PAGE',
    ASL_ZERO_PAGE_X: 'ASL_ZERO_PAGE_X',
    ASL_ABSOLUTE: 'ASL_ABSOLUTE',
    ASL_ABSOLUTE_X: 'ASL_ABSOLUTE_X',

    BCC: 'BCC', BCS: 'BCS', BEQ: 'BEQ',

    BIT_ZEROPAGE: 'BIT_ZEROPAGE',
    BIT_ABSOLUTE: 'BIT_ABSOLUTE',

    BMI: 'BMI', BNE: 'BNE', BPL: 'BPL', 

    # BRK: 'BRK', 

    BVC: 'BVC', BVS: 'BVS',
    
    CLC: 'CLC', CLD: 'CLD', CLI: 'CLI', CLV: 'CLV',

    CMP_IMMEDIATE: 'CMP_IMMEDIATE',
    CMP_ZEROPAGE: 'CMP_ZEROPAGE',
    CMP_ZEROPAGE_X: 'CMP_ZEROPAGE_X',
    CMP_ABSOLUTE: 'CMP_ABSOLUTE',
    CMP_ABSOLUTE_X: 'CMP_ABSOLUTE_X',
    CMP_ABSOLUTE_Y: 'CMP_ABSOLUTE_Y',
    CMP_INDIRECT_X: 'CMP_INDIRECT_X',
    CMP_INDIRECT_Y: 'CMP_INDIRECT_Y',

    CPX_IMMEDIATE: 'CPX_IMMEDIATE',
    CPX_ZEROPAGE: 'CPX_ZEROPAGE',
    CPX_ABSOLUTE: 'CPX_ABSOLUTE',

    CPY_IMMEDIATE: 'CPY_IMMEDIATE',
    CPY_ZEROPAGE: 'CPY_ZEROPAGE',
    CPY_ABSOLUTE: 'CPY_ABSOLUTE',

    DEC_ZEROPAGE: 'DEC_ZEROPAGE',
    DEC_ZEROPAGE_X: 'DEC_ZEROPAGE_X',
    DEC_ABSOLUTE: 'DEC_ABSOLUTE',
    DEC_ABSOLUTE_X: 'DEC_ABSOLUTE_X',
    
    DEX: 'DEX', DEY: 'DEY', 

    EOR_IMMEDIATE: 'EOR_IMMEDIATE',
    EOR_ZERO_PAGE: 'EOR_ZERO_PAGE',
    EOR_ZERO_PAGE_X: 'EOR_ZERO_PAGE_X',
    EOR_ABSOLUTE: 'EOR_ABSOLUTE',
    EOR_ABSOLUTE_X: 'EOR_ABSOLUTE_X',
    EOR_ABSOLUTE_Y: 'EOR_ABSOLUTE_Y',
    EOR_INDIRECT_X: 'EOR_INDIRECT_X',
    EOR_INDIRECT_Y: 'EOR_INDIRECT_Y',

    INC_ZEROPAGE: 'INC_ZEROPAGE',
    INC_ZEROPAGE_X: 'INC_ZEROPAGE_X',
    INC_ABSOLUTE: 'INC_ABSOLUTE',
    INC_ABSOLUTE_X: 'INC_ABSOLUTE_X',

    INX: 'INX', INY: 'INY',

    JMP_ABSOLUTE: 'JMP_ABSOLUTE',
    JMP_INDIRECT: 'JMP_INDIRECT',

    JSR: 'JSR', 

    LDA_IMMEDIATE: 'LDA_IMMEDIATE',
    LDA_ZEROPAGE: 'LDA_ZEROPAGE',
    LDA_ABSOLUTE: 'LDA_ABSOLUTE',
    LDA_INDIRECT_Y: 'LDA_INDIRECT_Y',
    LDA_INDIRECT_X: 'LDA_INDIRECT_X',
    LDA_ABSOLUTE_Y: 'LDA_ABSOLUTE_Y',
    LDA_ABSOLUTE_X: 'LDA_ABSOLUTE_X',
    LDA_ZEROPAGE_X: 'LDA_ZEROPAGE_X',

    LDX_IMMEDIATE: 'LDX_IMMEDIATE',
    LDX_ZEROPAGE: 'LDX_ZEROPAGE',
    LDX_ABSOLUTE: 'LDX_ABSOLUTE',
    LDX_ZEROPAGE_Y: 'LDX_ZEROPAGE_Y',
    LDX_ABSOLUTE_Y: 'LDX_ABSOLUTE_Y',

    LDY_IMMEDIATE: 'LDY_IMMEDIATE',
    LDY_ZEROPAGE: 'LDY_ZEROPAGE',
    LDY_ABSOLUTE: 'LDY_ABSOLUTE',
    LDY_ZEROPAGE_X: 'LDY_ZEROPAGE_X',
    LDY_ABSOLUTE_X: 'LDY_ABSOLUTE_X',

    LSR_ACCUMULATOR: 'LSR_ACCUMULATOR',
    LSR_ZERO_PAGE: 'LSR_ZERO_PAGE',
    LSR_ZERO_PAGE_X: 'LSR_ZERO_PAGE_X',
    LSR_ABSOLUTE: 'LSR_ABSOLUTE',
    LSR_ABSOLUTE_X: 'LSR_ABSOLUTE_X',

    NOP: 'NOP',

    ORA_IMMEDIATE: 'ORA_IMMEDIATE',
    ORA_ZERO_PAGE: 'ORA_ZERO_PAGE',
    ORA_ZERO_PAGE_X: 'ORA_ZERO_PAGE_X',
    ORA_ABSOLUTE: 'ORA_ABSOLUTE',
    ORA_ABSOLUTE_X: 'ORA_ABSOLUTE_X',
    ORA_ABSOLUTE_Y: 'ORA_ABSOLUTE_Y',
    ORA_INDIRECT_X: 'ORA_INDIRECT_X',
    ORA_INDIRECT_Y: 'ORA_INDIRECT_Y',

    PHA: 'PHA', PHP: 'PHP', PLA: 'PLA', PLP: 'PLP',

    ROL_ACCUMULATOR: 'ROL_ACCUMULATOR',
    ROL_ZERO_PAGE: 'ROL_ZERO_PAGE',
    ROL_ZERO_PAGE_X: 'ROL_ZERO_PAGE_X',
    ROL_ABSOLUTE: 'ROL_ABSOLUTE',
    ROL_ABSOLUTE_X: 'ROL_ABSOLUTE_X',

    ROR_ACCUMULATOR: 'ROR_ACCUMULATOR',
    ROR_ZERO_PAGE: 'ROR_ZERO_PAGE',
    ROR_ZERO_PAGE_X: 'ROR_ZERO_PAGE_X',
    ROR_ABSOLUTE: 'ROR_ABSOLUTE',
    ROR_ABSOLUTE_X: 'ROR_ABSOLUTE_X',

    RTI: 'RTI',
    RTS: 'RTS', 

    SBC_IMMEDIATE: 'SBC_IMMEDIATE',
    SBC_ZEROPAGE: 'SBC_ZEROPAGE',
    SBC_ZEROPAGE_X: 'SBC_ZEROPAGE_X',
    SBC_ABSOLUTE: 'SBC_ABSOLUTE',
    SBC_ABSOLUTE_X: 'SBC_ABSOLUTE_X',
    SBC_ABSOLUTE_Y: 'SBC_ABSOLUTE_Y',
    SBC_INDIRECT_X: 'SBC_INDIRECT_X',
    SBC_INDIRECT_Y: 'SBC_INDIRECT_Y',

    SEC: 'SEC', SED: 'SED', SEI: 'SEI',

    STA_INDIRECT_X: 'STA_INDIRECT_X',
    STA_ZEROPAGE: 'STA_ZEROPAGE',
    STA_ABSOLUTE: 'STA_ABSOLUTE',
    STA_INDIRECT_Y: 'STA_INDIRECT_Y',
    STA_ZEROPAGE_X: 'STA_ZEROPAGE_X',
    STA_ABSOLUTE_Y: 'STA_ABSOLUTE_Y',
    STA_ABSOLUTE_X: 'STA_ABSOLUTE_X',

    STX_ZEROPAGE: 'STX_ZEROPAGE',
    STX_ABSOLUTE: 'STX_ABSOLUTE',
    STX_ZEROPAGE_Y: 'STX_ZEROPAGE_Y',

    STY_ZEROPAGE: 'STY_ZEROPAGE',
    STY_ABSOLUTE: 'STY_ABSOLUTE',
    STY_ZEROPAGE_X: 'STY_ZEROPAGE_X',

    TAX: 'TAX', TAY: 'TAY', TSX: 'TSX', TXA: 'TXA', TXS: 'TXS', TYA: 'TYA'
}


class TestEmulatorTiming(unittest.TestCase):

    def test_timing_for_each_valid_instruction(self):

        cpu = CreateTestCpu()
        logger = FAKE_LOGGER
        for opcode, opcode_name in valid_opcodes.items():
            instruction_count = 0
            start_time = datetime.now()
            while 1:
                cpu.memory[cpu.PC()] = opcode
                cpu.execute_instruction_at_PC(logger)
                # execute_instruction(cpu, opcode=opcode, op2_lo_byte=0xDC, op2_hi_byte=0xDC)
                instruction_count += 1
                if instruction_count % 1000 == 0:
                    time_elapsed_in_seconds = (datetime.now() - start_time).total_seconds()
                    if time_elapsed_in_seconds >= 1:
                        print('%s executed %d times in %lf seconds' % (opcode_name, instruction_count, time_elapsed_in_seconds))
                        break

if __name__ == '__main__':
    unittest.main()
