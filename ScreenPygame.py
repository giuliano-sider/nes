import pygame
from ppu import Ppu, SCREEN_WIDTH, SCREEN_HEIGHT
# from nes import Nes
from nes_ppu_test_utils import CreateTestPpu
from nes_test_utils import CreateTestNes

nes = CreateTestNes()
pygame.init()

pygame.display.set_caption('HightMulator')

# black = (0,0,0)
# white = (255,255,255)
# renderimg = nes.ppu.render()
# display_height = nes.ppu.fakeRender().shape[0]
# display_width = nes.ppu.fakeRender().shape[1]
display_width = int(3 * SCREEN_WIDTH)
display_height = int(3 * SCREEN_HEIGHT)
gameDisplay = pygame.display.set_mode((display_width, display_height))

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    frame = pygame.transform.scale(pygame.surfarray.make_surface(nes.ppu.render().swapaxes(0, 1)),
                                   (display_width, display_height))
    gameDisplay.blit(frame, (0,0))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
