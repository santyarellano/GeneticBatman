from game_object import GameObject
import settings
import helpers
import colors
import groups
from rect import Rect
from brain import Options
from brain import Brain

BLACK = (0, 0, 0)


class Player(GameObject):

    def __init__(self, color, gravity, is_ai, optimization_fitness, rect):
        super().__init__()

        self.rect = rect

        self.left = 0
        self.right = 0
        self.dir = 0
        self.y_spd = 0
        self.walk_spd = 5
        self.jump_power = 10
        self.gravity = gravity
        self.color = color
        self.is_jumping = False
        self.is_ai = is_ai
        self.is_dead = False
        self.reached_goal = False
        self.finished = False
        self.dist_to_goal = 0
        self.run_optimization_fitness = optimization_fitness

        self.fitness = 0

        if is_ai:
            self.brain_step = 0
            self.brain = Brain()

    def jump(self):
        if not self.is_jumping:
            self.y_spd = -self.jump_power
            self.is_jumping = True

    def pressLeft(self):
        self.left = 1

    def pressRight(self):
        self.right = 1

    def releaseLeft(self):
        self.left = 0

    def releaseRight(self):
        self.right = 0
    
    def distWithGoal(self):
        self.dist_to_goal = helpers.dist(self, settings.goal)

    def calculateFitness(self):
        self.distWithGoal()
        if not self.reached_goal:
            if not self.run_optimization_fitness:
                if self.is_dead:
                    self.fitness = 0
                else:
                    d = self.dist_to_goal
                    d *= d * d
                    self.fitness = 1000/d
            else:
                if self.is_dead:
                    self.fitness = 0
                else:
                    d = self.dist_to_goal
                    d *= d * d
                    self.fitness = 1000/d
        else:
            self.fitness = 10000 / (self.brain_step * self.brain_step * self.brain_step)

    def getChild(self):
        rec = Rect(settings.PLAYER_SPAWN_X, settings.PLAYER_SPAWN_Y, settings.TILE_SIZE, settings.TILE_SIZE)
        child = Player(colors.GREEN, settings.GRAVITY, True, settings.OPTIMIZATION_FITNESS, rec)
        child.brain = self.brain.clone()
        return child

    def executeNextBrainStep(self):
        # process brain step
        if self.brain.instructions[self.brain_step] == Options.none:
            pass
        elif self.brain.instructions[self.brain_step] == Options.jump:
            self.jump()
        elif self.brain.instructions[self.brain_step] == Options.left:
            self.pressLeft()
        elif self.brain.instructions[self.brain_step] == Options.right:
            self.pressRight()

        self.brain_step += 1

    def isMoving(self):
        if self.y_spd != 0 or self.dir != 0 or self.is_jumping:
            return True
        return False

    def update(self, floor_tiles, goal, scr_w, scr_h):
        if not self.is_dead and not self.reached_goal and not self.finished:
            # act according to brain if necessary
            if self.is_ai:
                # reset movements
                self.releaseLeft()
                self.releaseRight()
                if self.brain_step >= len(self.brain.instructions):
                    if not self.reached_goal and not self.isMoving():
                        self.finished = True
                else:
                    self.executeNextBrainStep()

            
            self.rect.y += self.y_spd
            self.y_spd += self.gravity

            # check if player is colliding with floor
            for tile in floor_tiles:
                if helpers.rectsColliding(self.rect, tile.rect):
                    # check vertical collision
                    if self.rect.getCenterY() < tile.rect.y:  # from top
                        self.y_spd = 0
                        self.rect.y = tile.rect.y - self.rect.height + 1
                        self.is_jumping = False
                    # from bottom
                    elif self.rect.getCenterY() > (tile.rect.y + tile.rect.height):
                        self.y_spd = 0
                        self.rect.y = tile.rect.y + tile.rect.height

                    # check horizontal collision
                    #   should be within same vertical space
                    if self.rect.getCenterY() >= (tile.rect.getCenterY() - tile.rect.height/3):
                        if self.rect.getCenterY() <= (tile.rect.getCenterY() + tile.rect.height/3):
                            # now we can check the horizontal collision
                            if self.rect.getCenterX() < tile.rect.x:  # from left
                                self.right = 0
                                self.rect.x = tile.rect.x - self.rect.width
                            # from right
                            elif self.rect.getCenterX() > (tile.rect.x + tile.rect.width):
                                self.left = 0
                                self.rect.x = tile.rect.x + tile.rect.width

            self.dir = (self.right - self.left)
            self.rect.x += self.dir * self.walk_spd

            # check if dead
            if self.rect.x > scr_w or (self.rect.x + self.rect.width) < 0:
                self.is_dead = True
                self.finished = True
            if self.rect.y > scr_h or (self.rect.y + self.rect.height) < 0:
                self.is_dead = True
                self.finished = True

            # if optimizing, check if should stop
            if settings.OPTIMIZATION_FITNESS:
                self_dist = helpers.dist_modular(self.rect.x, goal.rect.x, self.rect.y, goal.rect.y)
                best_dist = helpers.dist_modular(settings.BEST_X, goal.rect.x, settings.BEST_Y, goal.rect.y)
                if self_dist < best_dist:
                    self.finished = True
                    self.reached_goal = True

            # check if reached goal
            if helpers.objectsColliding(self, goal):
                self.reached_goal = True
                self.finished = True
                if not settings.HUMAN_CONTROL and settings.REACHED_GOAL_AT_GEN == -1:
                    settings.REACHED_GOAL_AT_GEN = settings.population.generation
                    print(f"Reached goal at gen: {settings.REACHED_GOAL_AT_GEN}")

