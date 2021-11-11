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

def rectsColliding(rec1: Rect, rec2: Rect):
    if (rec1.getTopLeft()[0] == rec1.getBottomRight()[0] 
        or rec1.getTopLeft()[1] == rec1.getBottomRight()[1] 
        or rec2.getTopLeft()[0] == rec2.getBottomRight()[0] 
        or rec2.getTopLeft()[1] == rec2.getBottomRight()[1]):
        # the line cannot have positive overlap
        return False
       
     
    # If one rectangle is on left side of other
    if(rec1.getTopLeft()[0] >= rec2.getBottomRight()[0] 
        or rec2.getTopLeft()[0] >= rec1.getBottomRight()[0]):
        return False
 
    # If one rectangle is above other
    if(rec1.getBottomRight()[1] >= rec2.getTopLeft()[1] 
        or rec2.getBottomRight()[1] >= rec1.getTopLeft()[1]):
        return False
 
    return True