from enum import Enum, auto

class Modes(Enum):
    sequential = auto()
    concurrent = auto()
    parallel = auto()

TITLE = "Genetic Level Checker"
SCR_W = 0
SCR_H = 0
SCR = None
FPS = 60
MODE = Modes.parallel
PROCESSES = 2
PRINT_DEBUG = True

GRAVITY = 0.5
HUMAN_CONTROL = False
TILE_SIZE = 30
LEVEL_NAME = 'level.csv'
DEFAULT_BRAIN_SIZE = 400
MUTATION_RATE = 0.03
ELITISM_RATIO = 3
POPULATION_SIZE = 100

TIME_N_GENS = 5
GENERATIONS_WITHOUT_RENDER = 1000

OPTIMIZATION_FITNESS = False
SWAP_FITNESS = 10

PLAYER_SPAWN_X = 0
PLAYER_SPAWN_Y = 0

BEST_X = 0
BEST_Y = 0
BEST_DIST = 0
BEST_FITNESS = 0

# data globals
goal = None
floor_tiles = 0
goals = 0
