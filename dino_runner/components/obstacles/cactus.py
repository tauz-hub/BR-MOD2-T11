from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, SCREEN_WIDTH, POSITION_Y_ENTITIES, RUNNING
import random


class Cactus:
    def __init__(self, type):
        self.type = "smallCactus" if type == "smallCactus" else "largeCactus"
        listImageConstant = SMALL_CACTUS if self.type == "smallCactus" else LARGE_CACTUS

        self.image = listImageConstant[random.randint(
            0, len(listImageConstant) - 1)]
        self.rect = self.image.get_rect()
        self.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 2000)
        self.y = POSITION_Y_ENTITIES + \
            (RUNNING[1].get_height() - listImageConstant[0].get_height())

    def draw(self, screen, game_vel):

        self.x -= game_vel
        screen.blit(self.image, (self.x, self.y))
