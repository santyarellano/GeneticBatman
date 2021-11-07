# main imports
import pygame

# custom file imports
from floor import Floor

pygame.init()

# color constants
BLUE = (57, 177, 235)
BROWN = (145, 56, 49)
GREEN = (14, 112, 12)
RED = (189, 9, 42)

TITLE = "GENETIC BATMAN"
SCR_W = 700
SCR_H = 700
SCR_DIMENSIONS = (SCR_W, SCR_H)
SCR = pygame.display.set_mode(SCR_DIMENSIONS)
pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()

sprite_group = pygame.sprite.Group()

floor = Floor(GREEN, SCR_W, 100)
floor.rect.x = 0
floor.rect.y = SCR_H - floor.rect.height
sprite_group.add(floor)

quit = False
while not quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True

    SCR.fill(BLUE)

    sprite_group.draw(SCR)

    pygame.display.flip()

    clock.tick(60)


pygame.quit()
