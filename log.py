import os
import sys


class CpuLogger():

    def __init__(self, output_file):
        self.output_file = output_file

    def log_instruction(self, cpu):
        self.printLog(cpu.PC(), cpu.A(), cpu.X(), cpu.Y(), cpu.SP(), cpu.P())

    def log_memory_access_instruction(self, cpu, mem_addr, data):
        self.printLogLoadStore(cpu.PC(), cpu.A(), cpu.X(), cpu.Y(), cpu.SP(), cpu.P(), mem_addr, data)

    def printLog(self, regPC, regA, regX, regY, regSP,  regP):
        print("| pc = 0x%04x | a = 0x%04x | x = 0x%04x | y = 0x%04x | sp = 0x%04x | p[NV-BDIZC] = %s |" % (regPC,
            regA, regX, regY, regSP, '{0:08b}'.format(regP)), file=self.output_file)

    def printLogLoadStore(self, regPC, regA, regX, regY, regSP, regP, memAddr, data):
        print("| pc = 0x%04x | a = 0x%04x | x = 0x%04x | y = 0x%04x | sp = 0x%04x | p[NV-BDIZC] = %s | MEM[0x%04x] = 0x%04x |" % (regPC,
            regA, regX, regY, regSP, '{0:08b}'.format(regP), memAddr, data), file=self.output_file)


FAKE_LOGGER = CpuLogger(open(os.devnull, 'w'))


if __name__ == '__main__':
    CpuLogger(sys.stdout).printLog(1,1,1,1,0xFFC,'08b');
