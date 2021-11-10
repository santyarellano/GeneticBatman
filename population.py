import random
import copy
import multiprocessing as mp
import time
import numpy as np

from pygame import math

import colors
import settings
import groups
from rect import Rect
from player import Player

def update_players(players):
        for p in players:
            p.update()

class Population:

    def __init__(self, size):
        self.size = size
        self.players = []
        self.generation = 1
        self.total_fitness = 0
        self.gens_till_swap = settings.SWAP_FITNESS
        groups.players_group.empty()
        for i in range(size):
            rec = Rect(settings.PLAYER_SPAWN_X, settings.PLAYER_SPAWN_Y, settings.TILE_SIZE, settings.TILE_SIZE)
            p = Player(colors.GREEN, settings.GRAVITY, True, settings.OPTIMIZATION_FITNESS, rec)
            groups.players_group.add(p)

            self.players.append(p)

    def update(self): # this should work with multiprocessing
        # divide players for processes
        p_size = len(self.players)
        splits = np.array_split(self.players, settings.PROCESSES)

        # create processes
        processes = []
        for i in range(settings.PROCESSES):
            p = mp.Process(target=update_players, args=(splits[i],))
            processes.append(p)
            processes[i].start()
        
        # join processes (wait for 'em to finish)
        for p in processes:
            p.join()

        '''
        for p in self.players:
            p.update()
        '''
    
    def tickSwap(self):
        self.gens_till_swap -= 1
        if self.gens_till_swap == 0:
            settings.OPTIMIZATION_FITNESS = not settings.OPTIMIZATION_FITNESS
            self.gens_till_swap = settings.SWAP_FITNESS

        
    def calculateFitness(self):
        for p in self.players:
            p.calculateFitness()
        
    def allFinished(self):
        for p in self.players:
            if not p.finished:
                return False
        return True

    def setBestInstance(self):
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
                settings.BEST_FITNESS = p.fitness
                settings.BEST_DIST = p.dist_to_goal
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
        if settings.PRINT_DEBUG:
            print(f'generation: {self.generation}.\tAvg fitness: {self.getAvgFitness()}.\tBest: {settings.BEST_DIST}.\tOptimizing: {settings.OPTIMIZATION_FITNESS}')
    
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
                rec = Rect(settings.PLAYER_SPAWN_X, settings.PLAYER_SPAWN_Y, settings.TILE_SIZE, settings.TILE_SIZE)
                new_p = Player(colors.RED, settings.GRAVITY, True, settings.OPTIMIZATION_FITNESS, rec)
                new_p.brain = p.brain.clone()
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
        rec = Rect(settings.PLAYER_SPAWN_X, settings.PLAYER_SPAWN_Y, settings.TILE_SIZE, settings.TILE_SIZE)
        child = Player(colors.GREEN, settings.GRAVITY, True, settings.OPTIMIZATION_FITNESS, rec)
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