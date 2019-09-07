#!/usr/bin/env python3

import argparse
import sys

from instructions import BRK, handlers
from log import CpuLogger
from memory_mapper import MemoryMapper
from cpu import Cpu


def run_game(memory_mapper):

    cpu = Cpu(memory_mapper)
    logger = CpuLogger(sys.stdout)

    while 1:

        opcode = memory_mapper.cpu_read_byte(cpu.PC)
        handlers[opcode](cpu, logger)
        if opcode == BRK:
            break




if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run NES games with this emulator.')
    parser.add_argument('iNES_file', type=str, help='Provide an iNES file path to run a program.')
    args = parser.parse_args()

    run_game(MemoryMapper(args.iNES_file))