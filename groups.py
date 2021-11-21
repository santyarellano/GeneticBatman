import multiprocessing as mp

import settings
from floor import Floor

manager = mp.Manager()

floor_tiles = []
players_group = manager.list()