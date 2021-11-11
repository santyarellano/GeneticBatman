from game_object import GameObject
from rect import Rect
import math

def dist(spr1, spr2):
    deltaX = spr1.rect.x - spr2.rect.x
    deltaY = spr1.rect.y - spr2.rect.y
    return math.hypot(deltaX, deltaY)

def dist_modular(x1, x2, y1, y2):
    deltaX = x1 - x2
    deltaY = y1 - y2
    return math.hypot(deltaX, deltaY)

def objectsColliding(obj1: GameObject, obj2: GameObject):
    return rectsColliding(obj1.rect, obj2.rect)

def rectsColliding(rect1: Rect, rect2: Rect):
    if rect1.x < rect2.x + rect2.width and rect1.x + rect1.width > rect2.x and rect1.y < rect2.y + rect2.height and rect1.height + rect1.y > rect2.y:
        # collision detected!
        return True
    else:
        # no collision
        return False
    