from dino_runner.utils.constants import SMALL_CACTUS, SCREEN_WIDTH, POSITION_Y_ENTITIES, RUNNING
import random


class SmallCactus:
    def __init__(self):

        self.image = SMALL_CACTUS[random.randint(0, len(SMALL_CACTUS) - 1)]
        self.rect = self.image.get_rect()
        self.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 2000)
        self.y = POSITION_Y_ENTITIES + \
            (RUNNING[1].get_height() - SMALL_CACTUS[0].get_height())

    def draw(self, screen, game_vel):

        self.x -= game_vel
        screen.blit(self.image, (self.x, self.y))


# TODO turn into a single class
