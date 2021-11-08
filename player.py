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
        for tile in groups.floor_tiles:
            if pygame.sprite.collide_rect(self, tile):
                # check vertical collision
                if self.rect.centery < tile.rect.y: # from top
                    self.y_spd = 0
                    self.rect.y = tile.rect.y - self.rect.height + 1
                    self.is_jumping = False
                elif self.rect.centery > (tile.rect.y + tile.rect.height): # from bottom
                    self.y_spd = 0
                    self.rect.y = tile.rect.y + tile.rect.height

                # check horizontal collision
                #   should be within same vertical space
                if self.rect.centery >= (tile.rect.centery - tile.rect.height/3): 
                    if self.rect.centery <= (tile.rect.centery + tile.rect.height/3): 
                        # now we can check the horizontal collision
                        if self.rect.centerx < tile.rect.x: # from left
                            self.right = 0
                            self.rect.x = tile.rect.x - self.rect.width
                        elif self.rect.centerx > (tile.rect.x + tile.rect.width): # from right
                            self.left = 0
                            self.rect.x = tile.rect.x + tile.rect.width

        self.dir = (self.right - self.left)
        self.rect.x += self.dir * self.walk_spd