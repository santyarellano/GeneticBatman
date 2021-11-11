
import pygame

import colors
import settings
import groups

def drawFloors():
    for tile in groups.floor_tiles:
        pygame.draw.rect(settings.SCR, tile.color, (tile.rect.x, tile.rect.y, tile.rect.width, tile.rect.height))

def drawTopLayer():
    for obj in groups.top_layer:
        pygame.draw.rect(settings.SCR, obj.color, (obj.rect.x, obj.rect.y, obj.rect.width, obj.rect.height))

def drawPlayers():
    print(f"drawing {len(groups.players_group)}")
    for player in groups.players_group:
        pygame.draw.rect(settings.SCR, player.color, (player.rect.x, player.rect.y, player.rect.width, player.rect.height))

def drawByLayers():
    settings.SCR.fill(colors.BLACK)
    drawFloors()
    drawTopLayer()
    drawPlayers()