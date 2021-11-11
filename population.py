import random
import copy
import multiprocessing as mp
import time
import numpy as np
#from pygame import math

import colors
import groups
import settings
from rect import Rect
from player import Player

def update_players(players):
        for p in players:
            p.update()

class Population:

    def __init__(self, size):
        self.size = size
        self.generation = 1
        self.total_fitness = 0
        self.gens_till_swap = settings.SWAP_FITNESS
        groups.players_group.clear()
        for i in range(size):
            rec = Rect(settings.PLAYER_SPAWN_X, settings.PLAYER_SPAWN_Y, settings.TILE_SIZE, settings.TILE_SIZE)
            p = Player(colors.GREEN, settings.GRAVITY, True, settings.OPTIMIZATION_FITNESS, rec)
            groups.players_group.append(p)

    def update(self): # this should work with multiprocessing
        if settings.CONCURRENT:
            # divide players for processes
            splits = np.array_split(groups.players_group, settings.PROCESSES)

            # create processes
            processes = []
            for i in range(settings.PROCESSES):
                p = mp.Process(target=update_players, args=(splits[i],))
                processes.append(p)
                processes[i].start()
            
            # join processes (wait for 'em to finish)
            for p in processes:
                p.join()
        
        else:
            for p in groups.players_group:
                p.update()
        
    
    def tickSwap(self):
        self.gens_till_swap -= 1
        if self.gens_till_swap == 0:
            settings.OPTIMIZATION_FITNESS = not settings.OPTIMIZATION_FITNESS
            self.gens_till_swap = settings.SWAP_FITNESS

        
    def calculateFitness(self):
        for p in groups.players_group:
            p.calculateFitness()
        
    def allFinished(self):
        for p in groups.players_group:
            if not p.finished:
                return False
        return True

    def setBestInstance(self):
        # get all fitnesses in a list
        fitness_list = []
        for p in groups.players_group:
            fitness_list.append(p.fitness)
        
        fitness_list.sort(reverse=True)
        best_fitness = fitness_list[0]
        for p in groups.players_group:
            if p.fitness == best_fitness:
                settings.BEST_X = p.rect.x
                settings.BEST_Y = p.rect.y
                settings.BEST_FITNESS = p.fitness
                settings.BEST_DIST = p.dist_to_goal
                break

    def naturalSelection(self):
        new_players = []
        self.getTotalFitness()

        for i in range(self.size - settings.ELITISM_RATIO):
            # choose parent based on fitness
            parent1 = self.chooseParent()
            parent2 = self.chooseParent()

            # get child
            child = self.getChildFromParents(parent1, parent2)
            groups.players_group.append(child)
            new_players.append(child)
        
        # mutate this new players
        self.mutateChildren(new_players)

        # keep best players from previous generation
        top_players = self.getBestN()
        for p in top_players:
            new_players.append(p)
            groups.players_group.append(p)
        
        #groups.players_group.clear()
        groups.players_group = new_players
        self.generation += 1
        if settings.PRINT_DEBUG:
            print(f'Gen: {self.generation}.\tFitness: {self.getAvgFitness()}.\tBest: {settings.BEST_DIST}.\tOpt: {settings.OPTIMIZATION_FITNESS}')
    
    def getTotalFitness(self):
        self.total_fitness = 0
        for p in groups.players_group:
            self.total_fitness += p.fitness

    def getAvgFitness(self):
        return self.total_fitness / len(groups.players_group)

    def getBestN(self):
        # get all fitnesses in a list
        fitness_list = []
        for p in groups.players_group:
            fitness_list.append(p.fitness)
        
        fitness_list.sort(reverse=True)
        topN = []
        for i in range(settings.ELITISM_RATIO):
            topN.append(fitness_list[i])

        ret = []
        to_add = settings.ELITISM_RATIO
        for p in groups.players_group: # get N top players
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
            
        for p in groups.players_group:
            pos += p.fitness
            if pos > r:
                return p

        print(f"Choose parent got to a really weird point")
    
    def getChildFromParents(self, par1: Player, par2: Player):
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