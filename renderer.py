
import pygame

import colors
import settings
import groups

def drawFloors():
    for tile in groups.floor_tiles:
        pygame.draw.rect(settings.SCR, tile.color, (tile.rect.x, tile.rect.y, tile.rect.width, tile.rect.height))

def drawGoal():
    pygame.draw.rect(settings.SCR, settings.goal.color, (settings.goal.rect.x, settings.goal.rect.y, settings.goal.rect.width, settings.goal.rect.height))

def drawPlayers():
    for player in groups.players_group:
        pygame.draw.rect(settings.SCR, player.color, (player.rect.x, player.rect.y, player.rect.width, player.rect.height))

def blackScreen():
    settings.SCR.fill(colors.BLACK)

def drawByLayers():
    blackScreen()
    drawFloors()
    drawGoal()
    drawPlayers()