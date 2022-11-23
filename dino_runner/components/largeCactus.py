from dino_runner.utils.constants import LARGE_CACTUS, SCREEN_WIDTH, POSITION_Y_ENTITIES, RUNNING
import random


class LargeCactus:
    def __init__(self):

        self.image = LARGE_CACTUS[random.randint(0, len(LARGE_CACTUS) - 1)]
        self.rect = self.image.get_rect()
        self.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 2000)
        self.y = POSITION_Y_ENTITIES + \
            (RUNNING[0].get_height() - LARGE_CACTUS[0].get_height())

    def draw(self, screen, game_vel):

        self.x -= game_vel
        screen.blit(self.image, (self.x, self.y))


# TODO turn into a single class
