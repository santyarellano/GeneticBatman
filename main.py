# main imports
import pygame
pygame.init()

# custom file imports
import groups
import level_reader
import colors
from player import Player
from floor import Floor
from goal import Goal


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

# load level
x = 0
y = 0
for row in level:
    x = 0
    for cell in row:
        if cell == 0:
            pass
        elif cell == 1:  # static floor tile
            tile = Floor(colors.BROWN, TILE_SIZE, TILE_SIZE)
            tile.rect.x = x * TILE_SIZE
            tile.rect.y = y * TILE_SIZE
            groups.sprite_group.add(tile)
            groups.floor_tiles.add(tile)
        elif cell == 8: # goal
            goal = Goal(colors.YELLOW, TILE_SIZE, TILE_SIZE)
            goal.rect.x = x * TILE_SIZE
            goal.rect.y = y * TILE_SIZE
            groups.sprite_group.add(goal)
            groups.top_layer.add(goal)
        elif cell == 9:  # player
            player = Player(colors.GREEN, TILE_SIZE, GRAVITY)
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
    SCR.fill(colors.BLACK)
    # groups.sprite_group.draw(SCR) <- commented this to move to a layered structure
    groups.floor_tiles.draw(SCR)
    groups.top_layer.draw(SCR)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
