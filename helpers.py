import pygame
import math

def dist(spr1, spr2):
    deltaX = spr1.rect.x - spr2.rect.x
    deltaY = spr1.rect.y - spr2.rect.y
    return math.hypot(deltaX, deltaY)

def dist_modular(x1, x2, y1, y2):
    deltaX = x1 - x2
    deltaY = y1 - y2
    return math.hypot(deltaX, deltaY)