#!/usr/bin/env python3

import argparse
import sys
import math

from log import CpuLogger
from nes import Nes, run_for_n_cycles, execute_instruction_at_PC
from nes_cpu_utils import CpuHalt
from ppu import SCREEN_WIDTH, SCREEN_HEIGHT, print_sprites

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

def print_acopalices_state(nes):
    print('joypad_1_keypress_flags = {0:08b}'.format(nes.cpu.memory_mapper.cpu_memory_[0x0D]))
    print()
    print('time_to_update_game_state = {0:d}'.format(nes.cpu.memory_mapper.cpu_memory_[0x0E]))
    print('time_to_render = {0:d}'.format(nes.cpu.memory_mapper.cpu_memory_[0x0F]))
    print()
    print('main_character_x = {0:d}'.format(nes.cpu.memory_mapper.cpu_memory_[0x10]))
    print('main_character_y = {0:d}'.format(nes.cpu.memory_mapper.cpu_memory_[0x11]))
    print('main_character_life = {0:d}'.format(nes.cpu.memory_mapper.cpu_memory_[0x12]))
    print()
    print('num_meteors_on_screen = {0:d}'.format(nes.cpu.memory_mapper.cpu_memory_[0x13]))
    print('num_powerups_on_screen = {0:d}'.format(nes.cpu.memory_mapper.cpu_memory_[0x14]))
    print('num_flying_objects_on_screen = {0:d}'.format(nes.cpu.memory_mapper.cpu_memory_[0x15]))
    print()
    print('flying_objects_on_screen:')
    for i, addr in enumerate(range(0x16, 0x52, 5)):
        print('flying object {0:d}: x = {1:d}, y = {2:d}, delta_x = {3:d}, delta_y = {4:d}, type = {5:d}'.format(
            i,
            nes.cpu.memory_mapper.cpu_memory_[addr],
            nes.cpu.memory_mapper.cpu_memory_[addr+1],
            nes.cpu.memory_mapper.cpu_memory_[addr+2],
            nes.cpu.memory_mapper.cpu_memory_[addr+3],
            nes.cpu.memory_mapper.cpu_memory_[addr+4]))
    print()
    print('next_flying_object_addr = {0:#04x}'.format(nes.cpu.memory_mapper.cpu_memory_[0x52] + (nes.cpu.memory_mapper.cpu_memory_[0x53] << 8)))
    print('frames_until_next_flying_object_spawn = {0:d}'.format(nes.cpu.memory_mapper.cpu_memory_[0x54]))
    print()
    print('OAM_DMA_TransferPage:')
    print_sprites(nes.cpu.memory_mapper.cpu_memory_[0x200 : 0x300])


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
            pygame.event.pump()
            # TODO: Consider if pygame.event.KEYDOWN is a better way to handle keyboard input.
            key_pressed = pygame.key.get_pressed()
            # TODO: Consider a config mechanism for setting the key bindings.
            nes.controller.set_A_iff(key_pressed[pygame.K_a])
            nes.controller.set_B_iff(key_pressed[pygame.K_b])
            nes.controller.set_Select_iff(key_pressed[pygame.K_c])
            nes.controller.set_Start_iff(key_pressed[pygame.K_s])
            nes.controller.set_Up_iff(key_pressed[pygame.K_UP])
            nes.controller.set_Down_iff(key_pressed[pygame.K_DOWN])
            nes.controller.set_Left_iff(key_pressed[pygame.K_LEFT])
            nes.controller.set_Right_iff(key_pressed[pygame.K_RIGHT])

            if is_time_to_quit(pygame):
                break

            nes.ppu.begin_vblank()
            run_for_n_cycles(nes.cpu, NUM_CYCLES_VBLANK, logger)
            nes.ppu.end_vblank()

            render(pygame, gameDisplay, nes.ppu.render(), display_width, display_height)
            
            run_for_n_cycles(nes.cpu, NUM_CYCLES_OUTSIDE_VBLANK, logger)

            print('Game running at FPS = {0:f}'.format(clock.get_fps()))

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
            execute_instruction_at_PC(nes.cpu, logger)
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
