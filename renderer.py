
import pygame
from pygame.transform import flip

import colors
import settings
import groups
import math

# load images
bckg_tile_img = pygame.image.load('assets/Green.png')
floor_img = pygame.image.load('assets/land.png')
goal_img = pygame.image.load('assets/trophy.png')

player_run_frames = 12
player_run_img = []
player_folder = 'frog'
player_jump_img = pygame.image.load(f'assets/{player_folder}/Jump.png')
player_fall_img = pygame.image.load(f'assets/{player_folder}/Fall.png')
for i in range(player_run_frames):
    temp = pygame.image.load(f'assets/{player_folder}/{i}.png')
    player_run_img.append(temp)

def drawImg(img, x, y, width, height):
    img = pygame.transform.scale(img, (width, height))
    settings.SCR.blit(img, (x, y))

def drawFloors():
    for tile in groups.floor_tiles:
        #pygame.draw.rect(settings.SCR, tile.color, (tile.rect.x, tile.rect.y, tile.rect.width, tile.rect.height))
        drawImg(floor_img, tile.rect.x, tile.rect.y, tile.rect.width, tile.rect.height)

def drawGoal():
    #pygame.draw.rect(settings.SCR, settings.goal.color, (settings.goal.rect.x, settings.goal.rect.y, settings.goal.rect.width, settings.goal.rect.height))
    drawImg(goal_img, settings.goal.rect.x, settings.goal.rect.y, settings.TILE_SIZE, settings.TILE_SIZE)

def drawPlayers():
    if not settings.SHOW_ONLY_BEST and not settings.HUMAN_CONTROL: # draw rectangles
        for player in groups.players_group:
            pygame.draw.rect(settings.SCR, player.color, (player.rect.x, player.rect.y, player.rect.width, player.rect.height))
    else: # draw from imgs
        player = None
        if settings.HUMAN_CONTROL:
            player = groups.players_group[0]
        elif not settings.HUMAN_CONTROL and not settings.population.champion == None:
            player = settings.population.champion
        
        if not player == None:
            img = None
            #pygame.draw.rect(settings.SCR, p.color, (p.rect.x, p.rect.y, p.rect.width, p.rect.height))
            if player.y_spd < 0: # going up
                img = player_jump_img
                settings.player_run_pos = 0
            elif player.y_spd > 0: # falling
                img = player_fall_img
                settings.player_run_pos = 0
            elif player.y_spd == 0:
                img = player_run_img[settings.player_run_pos]
                if settings.player_frame_timer == 0:
                    settings.player_run_pos += 1
                    settings.player_frame_timer = settings.player_frame_time_def
                if settings.player_run_pos >= player_run_frames:
                    settings.player_run_pos = 0
                settings.player_frame_timer -= 1

            
            # flip image according to direction
            if not settings.flip_player_img and player.dir == -1:
                settings.flip_player_img = True
            elif settings.flip_player_img and player.dir == 1:
                settings.flip_player_img = False

            img = pygame.transform.flip(img, settings.flip_player_img, False)
            drawImg(img, player.rect.x, player.rect.y, settings.TILE_SIZE, settings.TILE_SIZE)

def drawBckg():
    #settings.SCR.fill(colors.BLACK)
    t_size = settings.TILE_SIZE * settings.BCKG_TILE_SCALE
    rows = math.ceil(settings.LEVEL_ROWS / settings.BCKG_TILE_SCALE)
    cols = math.ceil(settings.LEVEL_COLS / settings.BCKG_TILE_SCALE)
    for i in range(rows):
        for j in range(cols):
            drawImg(bckg_tile_img, j * t_size, i * t_size, t_size, t_size)
    

def drawByLayers():
    drawBckg()
    drawFloors()
    drawGoal()
    drawPlayers()