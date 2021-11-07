import pygame

BLACK = (0, 0, 0)


class Player(pygame.sprite.Sprite):

    def __init__(self, color, size, gravity):
        super().__init__()

        self.image = pygame.Surface([size, size])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, size, size])

        self.rect = self.image.get_rect()

        self.y_spd = 0
        self.jump_power = 10
        self.gravity = gravity
        self.is_jumping = False

    def update(self):
        self.rect.y += self.y_spd
        self.y_spd += self.gravity
