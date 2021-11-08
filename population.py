from pygame.sprite import groupcollide
import random

import colors
import settings
import groups
from player import Player

class Population:

    def __init__(self, size):
        self.size = size
        self.players = []
        self.generation = 1
        for i in range(size):
            p = Player(colors.GREEN, settings.TILE_SIZE, settings.GRAVITY, True)
            p.rect.x = settings.PLAYER_SPAWN_X
            p.rect.y = settings.PLAYER_SPAWN_Y
            groups.players_group.add(p)

            self.players.append(p)
        
    def calculateFitness(self):
        for p in self.players:
            p.calculateFitness()
        
    def allFinished(self):
        for p in self.players:
            if not p.is_dead and not p.reached_goal:
                return False
        return True

    def naturalSelection(self):
        new_players = []
        groups.players_group.empty()
        
        for i in range(self.size):
            # choose parent based on fitness
            parent = self.chooseParent()

            # get child
            child = parent.getChild()
            groups.players_group.add(child)
            new_players.append(child)
        
        self.players = new_players
        self.generation += 1
        print(f'generation: {self.generation} done.')
    
    def getTotalFitness(self):
        total = 0
        for p in self.players:
            total += p.fitness
        return total

    def chooseParent(self):
        random.seed()
        total_fitness = self.getTotalFitness()
        r = random.uniform(0.0, total_fitness)

        pos = 0
        for p in self.players:
            pos += p.fitness
            if pos > r:
                return p
        
    def mutateChildren(self):
        for p in self.players:
            p.brain.mutate()