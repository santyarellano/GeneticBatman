import pygame
import groups

BLACK = (0, 0, 0)


class Player(pygame.sprite.Sprite):

    def __init__(self, color, size, gravity):
        super().__init__()

        self.image = pygame.Surface([size, size])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, size, size])

        self.rect = self.image.get_rect()

        self.left = 0
        self.right = 0
        self.dir = 0
        self.y_spd = 0
        self.walk_spd = 5
        self.jump_power = 10
        self.gravity = gravity
        self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.y_spd = -self.jump_power
            self.is_jumping = True

    def pressLeft(self):
        self.left = 1

    def pressRight(self):
        self.right = 1

    def releaseLeft(self):
        self.left = 0

    def releaseRight(self):
        self.right = 0

    def update(self):
        self.rect.y += self.y_spd
        self.y_spd += self.gravity
        
        # check if player is colliding with floor
        hits_floor = pygame.sprite.spritecollideany(self, groups.floor_tiles)
        if hits_floor:
            # vertical hit
            if self.rect.y < hits_floor.rect.y:
                self.y_spd = 0
                self.is_jumping = False
                self.rect.y = hits_floor.rect.y - self.rect.height + 1
            elif self.y_spd < 0:
                self.y_spd = 0
            
            # horizontal hit 
            #   from left
            if self.rect.x < hits_floor.rect.x:
                self.right = 0

        self.dir = (self.right - self.left)
        self.rect.x += self.dir * self.walk_spd