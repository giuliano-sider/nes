#!/usr/bin/env python3

import argparse
import sys

from log import CpuLogger
from nes import Nes
from nes_cpu_utils import CpuHalt
# from ScreenPygame import render_ppu, init_render

def run_game(iNES_file, enable_logging):
    init_render()
    NUM_CYCLES_VBLANCK = 2266.6
    NUM_CYCLES_OUTSIDE_VBLANCK = 61440
    nes = Nes(iNES_file, test_mode=False)
    logger = CpuLogger(sys.stdout, enable_logging)

    while 1:
        try:
            cycles = nes.cpu.clock_ticks_since_reset
            while cycles < NUM_CYCLES_VBLANCK:
                nes.cpu.execute_instruction_at_PC(logger)
            render_ppu()
            cycles = nes.cpu.clock_ticks_since_reset
            while cycles < NUM_CYCLES_OUTSIDE_VBLANCK:
                nes.cpu.execute_instruction_at_PC(logger)

        except CpuHalt:
            break

def run_game_no_window(iNES_file, enable_logging):

    nes = Nes(iNES_file, test_mode=False)
    logger = CpuLogger(sys.stdout, enable_logging)

    while 1:
        try:
            nes.cpu.execute_instruction_at_PC(logger)
        except CpuHalt:
            break



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run NES games with this emulator.')
    parser.add_argument('iNES_file', type=str, help='Provide the path to an iNES file to run a program.')
    parser.add_argument('--log',
                        help='Log CPU and instruction related state at every executed instruction',
                        action='store_true')
    parser.add_argument('--nowindow',
                        help='Simply run CPU instructions until a BRK is reached.',
                        action='store_true')
    args = parser.parse_args()

    if args.nowindow:
        run_game_no_window(args.iNES_file, args.log)
    else:
        run_game(args.iNES_file, enable_logging=args.log)