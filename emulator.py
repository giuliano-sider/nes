#!/usr/bin/env python3

import argparse
import sys

from log import CpuLogger
from memory_mapper import MemoryMapper
from cpu import Cpu
from ppu import Ppu
from nes_cpu_utils import CpuHalt

def run_game(iNES_file):

    memory_mapper = MemoryMapper(iNES_file)
    cpu = Cpu(memory_mapper)
    ppu = Ppu(memory_mapper)
    logger = CpuLogger(sys.stdout)

    while 1:

        try:
            cpu.execute_instruction_at_PC(logger)
        except CpuHalt:
            break


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run NES games with this emulator.')
    parser.add_argument('iNES_file', type=str, help='Provide the path to an iNES file to run a program.')
    args = parser.parse_args()

    run_game(args.iNES_file)