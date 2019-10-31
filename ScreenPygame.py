import pygame
from ppu import Ppu
# from nes import Nes
from nes_ppu_test_utils import CreateTestPpu
from nes_test_utils import CreateTestNes

nes = CreateTestNes()
pygame.init()

pygame.display.set_caption('HightMulator')

black = (0,0,0)
white = (255,255,255)
renderimg = nes.ppu.render()
display_height = nes.ppu.fakeRender().shape[0]
display_width = nes.ppu.fakeRender().shape[1]
gameDisplay = pygame.display.set_mode((display_width,display_height))

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    spritImg = pygame.surfarray.make_surface(nes.ppu.render())
    gameDisplay.blit(spritImg, (0,0))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
