#!/usr/bin/env python3

import argparse
import sys
import math

from log import CpuLogger
from nes import Nes
from nes_cpu_utils import CpuHalt
from ppu import SCREEN_WIDTH, SCREEN_HEIGHT

def init_pygame(pygame, display_width, display_height):
    pygame.init()
    pygame.display.set_caption('HightMulator')
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    clock = pygame.time.Clock()
    return gameDisplay, clock

def is_time_to_quit(pygame):
    time_to_quit = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            time_to_quit = True
    return time_to_quit

def render(pygame, gameDisplay, frame, display_width, display_height):
    frame_to_render = pygame.transform.scale(pygame.surfarray.make_surface(frame.swapaxes(0, 1)),
                                             (display_width, display_height))
    gameDisplay.blit(frame_to_render, (0,0))
    pygame.display.update()

def run_game(iNES_file, enable_logging):

    nes = Nes(iNES_file, test_mode=False)
    logger = CpuLogger(sys.stdout, enable_logging)

    import pygame
    # init_render()
    NUM_CYCLES_VBLANK = math.ceil(2266.6)
    NUM_CYCLES_OUTSIDE_VBLANK = math.ceil(242 * 113.33)
    display_width = int(3 * SCREEN_WIDTH)
    display_height = int(3 * SCREEN_HEIGHT)
    gameDisplay, clock = init_pygame(pygame, display_width, display_height)

    while 1:
        try:
            if is_time_to_quit(pygame):
                break

            nes.ppu.begin_vblank()
            nes.cpu.run_for_n_cycles(NUM_CYCLES_VBLANK, logger)
            nes.ppu.end_vblank()

            render(pygame, gameDisplay, nes.ppu.render(), display_width, display_height)
            
            nes.cpu.run_for_n_cycles(NUM_CYCLES_OUTSIDE_VBLANK, logger)

            clock.tick(60)

        except CpuHalt:
            break

    pygame.quit()
    quit()

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
