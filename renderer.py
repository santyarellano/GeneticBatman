
import pygame

import colors
import settings
import groups
import math

# load images
bckg_tile_img = pygame.image.load('assets/Green.png')
floor_img = pygame.image.load('assets/land.png')
goal_img = pygame.image.load('assets/trophy.png')

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
    if not settings.SHOW_ONLY_BEST:
        for player in groups.players_group:
            pygame.draw.rect(settings.SCR, player.color, (player.rect.x, player.rect.y, player.rect.width, player.rect.height))
    else:
        if not settings.population.champion == None:
            p = settings.population.champion
            pygame.draw.rect(settings.SCR, p.color, (p.rect.x, p.rect.y, p.rect.width, p.rect.height))

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