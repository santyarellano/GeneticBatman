# main imports
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import multiprocessing as mp
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
    settings.mem_manager = mp.Manager()
    settings.ret_players = settings.mem_manager.list() # shared memory list to use in processes
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

    if settings.HUMAN_CONTROL:
        settings.MODE = settings.Modes.sequential

    # load level
    x = 0
    y = 0
    settings.LEVEL_ROWS = len(level)
    settings.LEVEL_COLS = len(level[0])
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
                    settings.population = Population(settings.POPULATION_SIZE)
                
            else:
                print("there's an error in the level data")

            x += 1
        y += 1

    # MAIN LOOP
    quit = False
    should_move_to_sequential = False
    k_return_down = False
    while not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True

        if settings.HUMAN_CONTROL:
            groups.players_group[0].update(groups.floor_tiles, settings.goal)
        elif not settings.MODE == settings.Modes.parallel:
            settings.population.update()
        elif settings.MODE == settings.Modes.parallel:
            settings.population.parallel_lifetime()

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
            if keys[pygame.K_s] and not should_move_to_sequential:
                should_move_to_sequential = True
                print("Moving to sequential mode")

            if keys[pygame.K_RETURN] and not k_return_down:
                k_return_down = True
                if settings.GENERATIONS_WITHOUT_RENDER >= 10000:
                    settings.GENERATIONS_WITHOUT_RENDER = 0
                else:
                    settings.GENERATIONS_WITHOUT_RENDER = 10000
            elif k_return_down and not keys[pygame.K_RETURN]:
                k_return_down = False

        # check if parallelism should stop so we can render
        if settings.population.generation > settings.GENERATIONS_WITHOUT_RENDER:
            if settings.MODE == settings.Modes.parallel:
                should_move_to_sequential = True

        # draw in screen
        if settings.HUMAN_CONTROL or (settings.population.generation > settings.GENERATIONS_WITHOUT_RENDER):
            
            renderer.drawByLayers()

            # show generation
            if not settings.HUMAN_CONTROL:
                txt = f'Generation: {settings.population.generation}. Population: {len(groups.players_group)}'
                text_renderer = font.render(txt, False, colors.WHITE)
                settings.SCR.blit(text_renderer, (20,20))

            pygame.display.flip()

            clock.tick(settings.FPS)

        # genetic algorithm
        if not settings.HUMAN_CONTROL:
            if settings.population.allFinished():
                if settings.population.generation == settings.TIME_N_GENS:
                    print_time = time.time() - start
                    print(f'{settings.TIME_N_GENS} generations took: {print_time} secs.')
                settings.population.tickSwap()
                settings.population.calculateFitness()
                if not settings.OPTIMIZATION_FITNESS:
                    settings.population.setBestInstance()
                settings.population.naturalSelection()

                if settings.MODE == settings.Modes.parallel:
                    if not settings.MODE == settings.Modes.sequential and should_move_to_sequential:
                        settings.MODE = settings.Modes.sequential
                    else:
                        settings.population.parallel_lifetime()

    pygame.quit()
