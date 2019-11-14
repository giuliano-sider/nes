from cpu cimport Cpu
from memory_mapper cimport MemoryMapper
from log import FAKE_LOGGER
from instructions cimport instructions
import os

cdef (int, int) _dummy_declaration # Cython bug 2745


DEFAULT_iNES_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test_utils', 'brk')


def CreateTestCpu(iNES_file=DEFAULT_iNES_FILE):
    """Return a valid Cpu for testing purposes. Any valid iNES file name or valid sequence of bytes read from such a file will work."""
    return Cpu(MemoryMapper(iNES_file))

def insert_instruction(Cpu cpu, addr, opcode, op2_lo_byte=None, op2_hi_byte=None):

    cpu.memory_mapper.cpu_force_write_byte(addr, opcode)
    # assert cpu.memory(addr) == opcode, 'addr = %s, cpu.memory(addr) = %s, opcode = %s' % (addr, cpu.memory(addr), opcode)
    if op2_lo_byte is not None:
        cpu.memory_mapper.cpu_force_write_byte(addr + 1, op2_lo_byte)
    if op2_hi_byte is not None:
        cpu.memory_mapper.cpu_force_write_byte(addr + 2, op2_hi_byte)

def execute_instruction(Cpu cpu, opcode, op2_lo_byte=None, op2_hi_byte=None, logger=FAKE_LOGGER):

    insert_instruction(cpu, cpu.PC(), opcode, op2_lo_byte, op2_hi_byte)
    instructions[opcode](cpu, logger)
