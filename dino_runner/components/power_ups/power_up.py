import random
from dino_runner.utils.constants import *
import pygame


class PowerUp(object):
    def __init__(self, image, type_power_up, space_gap_to_spawn, durantion):

        self.image = image
        self.type_power_up = type_power_up
        self.rect = self.image.get_rect()
        self.x = random.randint(
            SCREEN_WIDTH, SCREEN_WIDTH + space_gap_to_spawn)
        self.y = POSITION_Y_ENTITIES - \
            RUNNING[0].get_height() + SHIELD.get_height() * \
            random.randint(0, 2) - 10
        self.duration = durantion
        self.start_time = 0

    def draw(self, screen, game_vel):
        self.x -= game_vel
        screen.blit(self.image, (self.x, self.y))
