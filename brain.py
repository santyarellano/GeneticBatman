import random
import copy
from enum import Enum, auto

import settings

class Options(Enum):
    none = auto()
    jump = auto()
    left = auto()
    right = auto()

class Brain:

    def __init__(self):
        self.instructions = []
        self.size = settings.DEFAULT_BRAIN_SIZE
        self.randomize()

    def randomize(self):
        random.seed()
        for i in range(self.size):
            action = random.choice(list(Options))
            self.instructions.append(action)

    def clone(self):
        return copy.deepcopy(self)

    def crossover(self, other):
        new_brain = Brain()
        cross_point = random.randint(0, len(self.instructions))
        for i in range(len(self.instructions)):
            if i < cross_point:
                new_brain.instructions[i] = self.instructions[i]
            else:
                new_brain.instructions[i] = other.instructions[i]
        
        return new_brain
    
    def mutate(self):
        new_instructions = []
        for step in self.instructions:
            r = random.random()
            if r < settings.MUTATION_RATE:
                new_step = random.choice(list(Options))
                new_instructions.append(new_step)
            else:
                new_instructions.append(step)
                
        self.instructions = new_instructions