from pygame.sprite import groupcollide
import colors
import settings
import groups
from player import Player

class Population:

    def __init__(self, size):
        self.players = []
        for i in range(size):
            p = Player(colors.GREEN, settings.TILE_SIZE, settings.GRAVITY, True)
            p.rect.x = settings.PLAYER_SPAWN_X
            p.rect.y = settings.PLAYER_SPAWN_Y
            groups.sprite_group.add(p)
            groups.top_layer.add(p)

            self.players.append(p)