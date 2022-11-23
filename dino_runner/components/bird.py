from dino_runner.utils.constants import BIRD, SCREEN_WIDTH, POSITION_Y_ENTITIES, RUNNING
import random


class Bird:
    def __init__(self):
        self.step_index = 0
        self.image = BIRD[0]
        self.rect = self.image.get_rect()

        self.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 2000)
        position_fly = POSITION_Y_ENTITIES - \
            RUNNING[0].get_height() + BIRD[0].get_height() * \
            random.randint(0, 2) - 10
        self.y = position_fly

    def update(self):
        self.fly()
        if self.step_index >= 10:
            self.step_index = 0

    def fly(self):
        self.image = BIRD[0] if self.step_index < 5 else BIRD[1]

        self.step_index += 1

    def draw(self, screen, game_vel):

        self.x -= game_vel + 5
        screen.blit(self.image, (self.x, self.y))
