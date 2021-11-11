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

def rectsColliding(rec1: Rect, rec2: Rect):
    if (rec1.getTopLeft()[0] == rec1.getBottomRight()[0] 
        or rec1.getTopLeft()[1] == rec1.getBottomRight()[1] 
        or rec2.getTopLeft()[0] == rec2.getBottomRight()[0] 
        or rec2.getTopLeft()[1] == rec2.getBottomRight()[1]):
        # the line cannot have positive overlap
        return False
       
     
    # If one rectangle is on left side of other
    if(rec1.getTopLeft().x >= rec2.getBottomRight().x 
        or rec2.getTopLeft().x >= rec1.getBottomRight().x):
        return False
 
    # If one rectangle is above other
    if(rec1.getBottomRight().y >= rec2.getTopLeft().y or rec2.getBottomRight().y >= rec1.getTopLeft().y):
        return False
 
    return True