from rect import Rect
from game_object import GameObject

BLACK = (0, 0, 0)


class Goal(GameObject):

    def __init__(self, color, width, height):
        super().__init__()

        '''
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])
        '''

        self.rect = Rect(0, 0, width, height)
        self.color = color