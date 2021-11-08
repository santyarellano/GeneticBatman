import random
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
        clone = Brain()
        clone.instructions = list(self.instructions)
        return clone
    
    def mutate(self):
        for step in self.instructions:
            r = random.random()
            if r < settings.MUTATION_RATE:
                step = random.choice(list(Options))