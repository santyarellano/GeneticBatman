
class Rect:
    
    def __init__ (self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def getCenterY(self):
        return self.y + self.height/2

    def getCenterX(self):
        return self.x + self.width/2

    def getCenter(self):
        centerx = self.getCenterX()
        centery = self.getCenterY()
        return [centerx, centery]

    def getTopLeft(self):
        return (self.x, self.y)
    
    def getBottomRight(self):
        return (self.x + self.width, self.y + self.height)