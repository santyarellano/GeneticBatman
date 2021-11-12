from rect import Rect
from game_object import GameObject

BLACK = (0, 0, 0)


class Floor(GameObject):

    def __init__(self, color, width, height):
        super().__init__()

        self.rect = Rect(0, 0, width, height)
        self.color = color
