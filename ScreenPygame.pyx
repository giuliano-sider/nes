import pygame
from nes import Nes
from ppu import SCREEN_WIDTH, SCREEN_HEIGHT
from ppu cimport Ppu, NAME_TABLE_0_ADDRESS, ATTRIBUTE_TABLE_0_ADDRESS, SHOW_SPRITES, SHOW_BACKGROUND, PPUMASK
# from nes import Nes
from nes_ppu_test_utils import CreateTestPpu, insert_sprite, insert_background_palette, insert_sprite_palette, hide_all_sprites
from nes_test_utils import CreateTestNes

cdef (int, int) _dummy_declaration # Cython bug 2745


def prepare_nes_for_test_frame(nes):
    """Setup the Nes state in order to draw a test frame onto the pygame surface."""

    nes_image_palette = [0, 0x02, 0x05, 0x0A, 0, 0x07, 0x14, 0x27, 0, 0x29, 0x2C, 0x0D, 0, 0x13, 0x39, 0x1B]
    insert_background_palette((<Ppu> (nes.ppu)), nes_image_palette)
    insert_sprite_palette((<Ppu> (nes.ppu)), nes_image_palette)

    for i in range(NAME_TABLE_0_ADDRESS + 960 // 2, NAME_TABLE_0_ADDRESS + 960):
        (<Ppu> (nes.ppu)).memory[i] = 0xFF # Empty tile in Acopalices pattern table.
    for i in range(ATTRIBUTE_TABLE_0_ADDRESS, ATTRIBUTE_TABLE_0_ADDRESS + 64):
        (<Ppu> (nes.ppu)).memory[i] = 0b11100100 # Use one of each of the four background palettes at every tile group.

    hide_all_sprites((<Ppu> (nes.ppu)))

    # Slipper
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=0, y=112, x=128, tile_index=0x04, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=1, y=112, x=136, tile_index=0x05, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=2, y=120, x=128, tile_index=0x14, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=3, y=120, x=136, tile_index=0x15, palette_index=0)

    # Big roach
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=4, y=100, x=108, tile_index=0x00, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=5, y=100, x=116, tile_index=0x01, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=6, y=100, x=124, tile_index=0x02, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=7, y=108, x=108, tile_index=0x10, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=8, y=108, x=116, tile_index=0x11, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=9, y=108, x=124, tile_index=0x12, palette_index=0)

    # Slipper 2
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=10, y=212, x=128, tile_index=0x04, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=11, y=212, x=136, tile_index=0x05, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=12, y=220, x=128, tile_index=0x14, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=13, y=220, x=136, tile_index=0x15, palette_index=0)
    
    # Big roach 2
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=14, y=200, x=108, tile_index=0x00, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=15, y=200, x=116, tile_index=0x01, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=16, y=200, x=124, tile_index=0x02, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=17, y=208, x=108, tile_index=0x10, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=18, y=208, x=116, tile_index=0x11, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=19, y=208, x=124, tile_index=0x12, palette_index=0)

    # Slipper 3
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=20, y=22, x=128, tile_index=0x04, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=21, y=22, x=136, tile_index=0x05, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=22, y=30, x=128, tile_index=0x14, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=23, y=30, x=136, tile_index=0x15, palette_index=0)
    
    # Big roach 3
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=24, y=10, x=108, tile_index=0x00, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=25, y=10, x=116, tile_index=0x01, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=26, y=10, x=124, tile_index=0x02, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=27, y=18, x=108, tile_index=0x10, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=28, y=18, x=116, tile_index=0x11, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=29, y=18, x=124, tile_index=0x12, palette_index=0)

    # Slipper 4
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=30, y=112, x=158, tile_index=0x04, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=31, y=112, x=166, tile_index=0x05, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=32, y=120, x=158, tile_index=0x14, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=33, y=120, x=166, tile_index=0x15, palette_index=0)

    # Big roach 4
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=34, y=100, x=138, tile_index=0x00, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=35, y=100, x=146, tile_index=0x01, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=36, y=100, x=154, tile_index=0x02, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=37, y=108, x=138, tile_index=0x10, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=38, y=108, x=146, tile_index=0x11, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=39, y=108, x=154, tile_index=0x12, palette_index=0)

    # Slipper 5
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=40, y=212, x=158, tile_index=0x04, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=41, y=212, x=166, tile_index=0x05, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=42, y=220, x=158, tile_index=0x14, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=43, y=220, x=166, tile_index=0x15, palette_index=0)
    
    # Big roach 5
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=44, y=200, x=138, tile_index=0x00, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=45, y=200, x=146, tile_index=0x01, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=46, y=200, x=154, tile_index=0x02, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=47, y=208, x=138, tile_index=0x10, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=48, y=208, x=146, tile_index=0x11, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=49, y=208, x=154, tile_index=0x12, palette_index=0)

    # Slipper 6
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=50, y=22, x=158, tile_index=0x04, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=51, y=22, x=166, tile_index=0x05, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=52, y=30, x=158, tile_index=0x14, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=53, y=30, x=166, tile_index=0x15, palette_index=0)
    
    # Big roach 6
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=54, y=10, x=138, tile_index=0x00, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=55, y=10, x=146, tile_index=0x01, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=56, y=10, x=154, tile_index=0x02, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=57, y=18, x=138, tile_index=0x10, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=58, y=18, x=146, tile_index=0x11, palette_index=0)
    insert_sprite((<Ppu> (nes.ppu)), sprite_index=59, y=18, x=154, tile_index=0x12, palette_index=0)


    (<Ppu> (nes.ppu)).ppumask = SHOW_SPRITES | SHOW_BACKGROUND


nes = CreateTestNes()
pygame.init()

pygame.display.set_caption('HightMulator')

# black = (0,0,0)
# white = (255,255,255)
# renderimg = (<Ppu> (nes.ppu)).render()
# display_height = (<Ppu> (nes.ppu)).fakeRender().shape[0]
# display_width = (<Ppu> (nes.ppu)).fakeRender().shape[1]
display_width = int(3 * SCREEN_WIDTH)
display_height = int(3 * SCREEN_HEIGHT)
gameDisplay = pygame.display.set_mode((display_width, display_height))

clock = pygame.time.Clock()
running = True

prepare_nes_for_test_frame(nes)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    frame = pygame.transform.scale(pygame.surfarray.make_surface((<Ppu> (nes.ppu)).render().swapaxes(0, 1)),
                                   (display_width, display_height))
    gameDisplay.blit(frame, (0,0))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
