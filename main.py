# main imports
import groups
import level_reader
from player import Player
from bckg_obj import BackgroundObject
from floor import Floor
from typing import Match
import pygame
pygame.init()

# custom file imports

# color definitions
BLACK = (0, 0, 0)
BLUE = (57, 177, 235)
BROWN = (194, 130, 52)
GREEN = (15, 227, 11)
RED = (189, 9, 42)


# constants
TITLE = "Genetic Level Checker"
GRAVITY = 0.5
HUMAN_CONTROL = True
TILE_SIZE = 30
LEVEL_NAME = 'level.csv'
level = level_reader.getLevel(LEVEL_NAME)
SCR_W = len(level[0]) * TILE_SIZE
SCR_H = len(level) * TILE_SIZE
SCR_DIMENSIONS = (SCR_W, SCR_H)
SCR = pygame.display.set_mode(SCR_DIMENSIONS)

level = level_reader.getLevel(LEVEL_NAME)

pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()

'''
sprite_group = pygame.sprite.Group()
floor_tiles = pygame.sprite.Group()
top_layer = pygame.sprite.Group()
player = None
'''

# load level
x = 0
y = 0
for row in level:
    x = 0
    for cell in row:
        if cell == 0:
            pass
        elif cell == 1:  # static floor tile
            tile = Floor(BROWN, TILE_SIZE, TILE_SIZE)
            tile.rect.x = x * TILE_SIZE
            tile.rect.y = y * TILE_SIZE
            groups.sprite_group.add(tile)
            groups.floor_tiles.add(tile)
        elif cell == 9:  # player
            player = Player(GREEN, TILE_SIZE, GRAVITY)
            player.rect.x = x * TILE_SIZE
            player.rect.y = y * TILE_SIZE
            groups.sprite_group.add(player)
            groups.top_layer.add(player)
        else:
            print("there's an error in the level data")

        x += 1
    y += 1

# MAIN LOOP
quit = False
while not quit and player is not None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True

    groups.sprite_group.update()

    # Key events (ONLY ALLOWED WHEN A HUMAN IS PLAYING)
    if HUMAN_CONTROL:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.jump()

        if keys[pygame.K_a]:
            player.pressLeft()
        else:
            player.releaseLeft()

        if keys[pygame.K_d]:
            player.pressRight()
        else:
            player.releaseRight()

    # draw in screen
    SCR.fill(BLACK)
    # groups.sprite_group.draw(SCR) <- commented this to move to a layered structure
    groups.floor_tiles.draw(SCR)
    groups.top_layer.draw(SCR)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
