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