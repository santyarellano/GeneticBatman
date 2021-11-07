# main imports
import builtins
import pygame

# custom file imports
from floor import Floor
from bckg_obj import BackgroundObject

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

# platforms
floor = Floor(GREEN, SCR_W, 100)
floor.rect.x = 0
floor.rect.y = SCR_H - floor.rect.height
sprite_group.add(floor)

middleFloor = Floor(GREEN, SCR_W / 2, 30)
middleFloor.rect.x = (SCR_W / 2) - (middleFloor.rect.width / 2)
middleFloor.rect.y = (SCR_H / 2) - (middleFloor.rect.height / 2)
sprite_group.add(middleFloor)

# buildings
building1 = BackgroundObject(BROWN, 150, SCR_H/3*2)
building1.rect.x = 0
building1.rect.y = SCR_H - building1.rect.height - floor.rect.height
sprite_group.add(building1)

building2 = BackgroundObject(BROWN, 150, SCR_H/3*2)
building2.rect.x = SCR_W - building2.rect.width
building2.rect.y = SCR_H - building2.rect.height - floor.rect.height
sprite_group.add(building2)


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
