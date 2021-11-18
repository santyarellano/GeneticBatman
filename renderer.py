
import pygame

import colors
import settings
import groups

# load images
floor_img = pygame.image.load('assets/land.png')

def drawFloors():
    for tile in groups.floor_tiles:
        pygame.draw.rect(settings.SCR, tile.color, (tile.rect.x, tile.rect.y, tile.rect.width, tile.rect.height))

def drawGoal():
    pygame.draw.rect(settings.SCR, settings.goal.color, (settings.goal.rect.x, settings.goal.rect.y, settings.goal.rect.width, settings.goal.rect.height))

def drawPlayers():
    if not settings.SHOW_ONLY_BEST:
        for player in groups.players_group:
            pygame.draw.rect(settings.SCR, player.color, (player.rect.x, player.rect.y, player.rect.width, player.rect.height))
    else:
        if not settings.population.champion == None:
            p = settings.population.champion
            pygame.draw.rect(settings.SCR, p.color, (p.rect.x, p.rect.y, p.rect.width, p.rect.height))

def blackScreen():
    settings.SCR.fill(colors.BLACK)

def drawByLayers():
    blackScreen()
    drawFloors()
    drawGoal()
    drawPlayers()