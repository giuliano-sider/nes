
import os
import sys
from memory_mapper cimport STACK_PAGE_ADDR, cpu_unmirrored_address
from cpu cimport Cpu


cdef class CpuLogger():

    def __init__(self, output_file, enable_logging=True):
        self.output_file = output_file
        self.enable_logging = enable_logging

    cdef void log_instruction(self, Cpu cpu) except *:
        if self.enable_logging is True:
            self.printLog(cpu.PC(), cpu.A(), cpu.X(), cpu.Y(), STACK_PAGE_ADDR + cpu.SP(), cpu.P())

    cdef void log_memory_access_instruction(self, Cpu cpu, int mem_addr, int data) except *:
        if self.enable_logging is True:
            self.printLogLoadStore(cpu.PC(), cpu.A(), cpu.X(), cpu.Y(), STACK_PAGE_ADDR + cpu.SP(), cpu.P(), cpu_unmirrored_address(mem_addr), data)

    def printLog(self, regPC, regA, regX, regY, regSP,  regP):
        print("| pc = 0x%04x | a = 0x%04x | x = 0x%04x | y = 0x%04x | sp = 0x%04x | p[NV-BDIZC] = %s |" % (regPC,
            regA, regX, regY, regSP, '{0:08b}'.format(regP)), file=self.output_file)

    def printLogLoadStore(self, regPC, regA, regX, regY, regSP, regP, memAddr, data):
        print("| pc = 0x%04x | a = 0x%04x | x = 0x%04x | y = 0x%04x | sp = 0x%04x | p[NV-BDIZC] = %s | MEM[0x%04x] = 0x%04x |" % (regPC,
            regA, regX, regY, regSP, '{0:08b}'.format(regP), memAddr, data), file=self.output_file)


FAKE_LOGGER = CpuLogger(open(os.devnull, 'w'), enable_logging=False)


if __name__ == '__main__':
    CpuLogger(sys.stdout).printLog(1,1,1,1,0xFFC,'08b');
