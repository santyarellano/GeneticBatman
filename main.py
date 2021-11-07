# main imports
import builtins
import pygame

# custom file imports
from floor import Floor
from bckg_obj import BackgroundObject
from player import Player

pygame.init()

# color definitions
BLACK = (0, 0, 0)
BLUE = (57, 177, 235)
BROWN = (194, 130, 52)
GREEN = (15, 227, 11)
RED = (189, 9, 42)

# constants
TITLE = "Genetic Level Checker"
SCR_W = 700
SCR_H = 700
SCR_DIMENSIONS = (SCR_W, SCR_H)
SCR = pygame.display.set_mode(SCR_DIMENSIONS)
pygame.display.set_caption(TITLE)

# game constants
GRAVITY = 0.5

clock = pygame.time.Clock()

sprite_group = pygame.sprite.Group()

# platforms
floor = Floor(BROWN, SCR_W, 100)
floor.rect.x = 0
floor.rect.y = SCR_H - floor.rect.height
sprite_group.add(floor)

middleFloor = Floor(BROWN, SCR_W / 2, 30)
middleFloor.rect.x = (SCR_W / 2) - (middleFloor.rect.width / 2)
middleFloor.rect.y = (SCR_H / 2) - (middleFloor.rect.height / 2)
sprite_group.add(middleFloor)

# player
player = Player(GREEN, 30, GRAVITY)
player.rect.x = 50
player.rect.y = floor.rect.y - (player.rect.width * 2)
sprite_group.add(player)

# MAIN LOOP
quit = False
while not quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True

    sprite_group.update()

    # check if player is touching the floor (to do: modify this to apply it to all physical objs)
    if pygame.sprite.collide_mask(player, floor):
        player.y_spd = 0
        player.is_jumping = True
    else:
        player.is_jumping = False

    # Key events
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if player.is_jumping:
            player.y_spd = -player.jump_power

    # draw in screen
    SCR.fill(BLACK)
    sprite_group.draw(SCR)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
