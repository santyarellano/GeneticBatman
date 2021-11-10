import random
import copy

import colors
import settings
import groups
from player import Player

class Population:

    def __init__(self, size):
        self.size = size
        self.players = []
        self.generation = 1
        self.total_fitness = 0
        groups.players_group.empty()
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
            if not p.finished:
                return False
        return True

    def setBestPosition(self):
        # get all fitnesses in a list
        fitness_list = []
        for p in self.players:
            fitness_list.append(p.fitness)
        
        fitness_list.sort(reverse=True)
        best_fitness = fitness_list[0]
        for p in self.players:
            if p.fitness == best_fitness:
                settings.BEST_X = p.rect.x
                settings.BEST_Y = p.rect.y
                break

    def naturalSelection(self):
        new_players = []
        groups.players_group.empty()
        self.getTotalFitness()

        for i in range(self.size - settings.ELITISM_RATIO):
            # choose parent based on fitness
            parent1 = self.chooseParent()
            parent2 = self.chooseParent()

            # get child
            child = self.getChildFromParents(parent1, parent2)
            groups.players_group.add(child)
            new_players.append(child)
        
        # mutate this new players
        self.mutateChildren(new_players)

        # keep best players from previous generation
        top_players = self.getBestN()
        for p in top_players:
            new_players.append(p)
            groups.players_group.add(p)
        
        self.players = new_players
        self.generation += 1
        print(f'generation: {self.generation}.\tAvg fitness: {self.getAvgFitness()}.\tBest: ({settings.BEST_X}, {settings.BEST_Y})')
    
    def getTotalFitness(self):
        self.total_fitness = 0
        for p in self.players:
            self.total_fitness += p.fitness

    def getAvgFitness(self):
        return self.total_fitness / len(self.players)

    def getBestN(self):
        # get all fitnesses in a list
        fitness_list = []
        for p in self.players:
            fitness_list.append(p.fitness)
        
        fitness_list.sort(reverse=True)
        topN = []
        for i in range(settings.ELITISM_RATIO):
            topN.append(fitness_list[i])

        ret = []
        to_add = settings.ELITISM_RATIO
        for p in self.players: # get N top players
            if p.fitness in topN and to_add > 0:
                new_p = Player(colors.RED, settings.TILE_SIZE, settings.GRAVITY, True)
                new_p.brain = p.brain.clone()
                new_p.rect.x = settings.PLAYER_SPAWN_X
                new_p.rect.y = settings.PLAYER_SPAWN_Y
                ret.append(new_p)
                to_add -= 1
        
        return ret

    def chooseParent(self):
        r = random.uniform(0.0, self.total_fitness)
        
        pos = 0
        for p in self.players:
            pos += p.fitness
            if pos > r:
                return p
    
    def getChildFromParents(self, par1, par2):
        child = Player(colors.GREEN, settings.TILE_SIZE, settings.GRAVITY, True)
        child.rect.x = settings.PLAYER_SPAWN_X
        child.rect.y = settings.PLAYER_SPAWN_Y
        child.brain = par1.brain.crossover(par2.brain)

        #child.brain = self.brain.clone()
        return child
        
    def mutateChildren(self, players):
        for p in players:
            old = copy.copy(p.brain.instructions)
            p.brain.mutate()
            if old == p.brain.instructions:
                #print("not mutated")
                pass
            else:
                #print("mutated")
                pass