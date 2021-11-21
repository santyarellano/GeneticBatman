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
PRINT_DEBUG = True
SHOW_ONLY_BEST = True

MODE = Modes.concurrent
SPLITS_N = 1

GRAVITY = 0.5
HUMAN_CONTROL = False
TILE_SIZE = 30
LEVEL_NAME = 'level.csv'
DEFAULT_BRAIN_SIZE = 400
MUTATION_RATE = 0.03
ELITISM_RATIO = 3
POPULATION_SIZE = 100

LEVEL_ROWS = 0
LEVEL_COLS = 0
BCKG_TILE_SCALE = 4

TIME_N_GENS = 10
GENERATIONS_WITHOUT_RENDER = 10 # this should always be greater than 0

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
population = None
flip_player_img = False
player_run_pos = 0
player_frame_time_def = 6
player_frame_timer = player_frame_time_def