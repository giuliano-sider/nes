from cpu import Cpu
from memory_mapper import MemoryMapper
from log import FAKE_LOGGER
from instructions import instructions
import os


def CreateTestCpu(iNES_file='/bin/brk', absolute_path=False):
    """Return a valid Cpu for testing purposes. Any valid iNES file name or valid sequence of bytes read from such a file will work."""
    iNES_file_path = ""
    if absolute_path :
        iNES_file_path = os.getcwd()
        print(iNES_file_path)
    iNES_file_path = iNES_file_path + iNES_file
    return Cpu(MemoryMapper(iNES_file_path))

def insert_instruction(cpu, addr, opcode, op2_lo_byte=None, op2_hi_byte=None):

    cpu.memory[addr] = opcode
    if op2_lo_byte is not None:
        cpu.memory[addr + 1] = op2_lo_byte
    if op2_hi_byte is not None:
        cpu.memory[addr + 2] = op2_hi_byte

def execute_instruction(cpu, opcode, op2_lo_byte=None, op2_hi_byte=None, logger=FAKE_LOGGER):

    insert_instruction(cpu, cpu.PC(), opcode, op2_lo_byte, op2_hi_byte)
    instructions[opcode](cpu, logger)
