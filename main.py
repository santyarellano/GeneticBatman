# main imports
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
pygame.init()

# custom file imports
import level_reader
import colors
import settings
import groups
import renderer
from rect import Rect
from player import Player
from floor import Floor
from goal import Goal
from population import Population

if __name__ == '__main__':

    # setup
    level = level_reader.getLevel(settings.LEVEL_NAME)
    settings.SCR_W = len(level[0]) * settings.TILE_SIZE
    settings.SCR_H = len(level) * settings.TILE_SIZE
    SCR_DIMENSIONS = (settings.SCR_W, settings.SCR_H)
    settings.SCR = pygame.display.set_mode(SCR_DIMENSIONS)
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)

    level = level_reader.getLevel(settings.LEVEL_NAME)

    pygame.display.set_caption(settings.TITLE)

    clock = pygame.time.Clock()
    start = time.time()

    # load level
    x = 0
    y = 0
    for row in level:
        x = 0
        for cell in row:
            if cell == 0:
                pass
            elif cell == 1:  # static floor tile
                tile = Floor(colors.BROWN, settings.TILE_SIZE, settings.TILE_SIZE)
                tile.rect.x = x * settings.TILE_SIZE
                tile.rect.y = y * settings.TILE_SIZE
                groups.floor_tiles.append(tile)
                settings.floor_tiles += 1
            elif cell == 8: # goal
                goal = Goal(colors.YELLOW, settings.TILE_SIZE, settings.TILE_SIZE)
                goal.rect.x = x * settings.TILE_SIZE
                goal.rect.y = y * settings.TILE_SIZE
                settings.goal = goal
                settings.goals += 1
            elif cell == 9:  # player
                settings.PLAYER_SPAWN_X = x * settings.TILE_SIZE
                settings.PLAYER_SPAWN_Y = y * settings.TILE_SIZE

                if settings.HUMAN_CONTROL:
                    rec = Rect(settings.PLAYER_SPAWN_X, settings.PLAYER_SPAWN_Y, settings.TILE_SIZE, settings.TILE_SIZE)
                    player = Player(colors.GREEN, settings.GRAVITY, False, False, rec)
                    player.rect.x = settings.PLAYER_SPAWN_X
                    player.rect.y = settings.PLAYER_SPAWN_Y
                    groups.players_group.append(player)
                else:
                    population = Population(settings.POPULATION_SIZE)
                
            else:
                print("there's an error in the level data")

            x += 1
        y += 1

    # MAIN LOOP
    quit = False
    while not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True

        #groups.players_group.update()
        if settings.HUMAN_CONTROL:
            groups.players_group[0].update()
        else:
            population.update()

        # Key events (ONLY ALLOWED WHEN A HUMAN IS PLAYING)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            quit = True

        if settings.HUMAN_CONTROL:
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
        elif not settings.HUMAN_CONTROL:
            if keys[pygame.K_RETURN]:
                if settings.GENERATIONS_WITHOUT_RENDER >= 10000:
                    settings.GENERATIONS_WITHOUT_RENDER = 0
                else:
                    settings.GENERATIONS_WITHOUT_RENDER = 10000

        # draw in screen
        if settings.HUMAN_CONTROL or (population.generation > settings.GENERATIONS_WITHOUT_RENDER):
            
            renderer.drawByLayers()

            # show generation
            if not settings.HUMAN_CONTROL:
                txt = f'Generation: {population.generation}. Population: {len(groups.players_group)}'
                text_renderer = font.render(txt, False, colors.WHITE)
                settings.SCR.blit(text_renderer, (20,20))

            pygame.display.flip()

            clock.tick(settings.FPS)

        # genetic algorithm
        if not settings.HUMAN_CONTROL:
            if population.allFinished():
                if population.generation == settings.TIME_N_GENS:
                    print_time = time.time() - start
                    print(f'{settings.TIME_N_GENS} generations took: {print_time} secs.')
                population.tickSwap()
                population.calculateFitness()
                if not settings.OPTIMIZATION_FITNESS:
                    population.setBestInstance()
                population.naturalSelection()

    pygame.quit()
