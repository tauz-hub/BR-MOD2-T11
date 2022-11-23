import pygame
from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING, POSITION_Y_ENTITIES, GAME_VEL
from datetime import time

X_POS = 80
Y_POS = 310
JUMP_VEL = 8.5


class Dinosaur:
    def __init__(self, parent) -> None:
        self.image = RUNNING[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = 80
        self.dino_rect.y = POSITION_Y_ENTITIES
        self.step_index = 0
        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False
        self.dino_dash_load = 100

        self.jump_vel = JUMP_VEL
        self.parent = parent

    def run(self):
        self.image = RUNNING[0] if self.step_index < 5 else RUNNING[1]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = 80
        self.dino_rect.y = POSITION_Y_ENTITIES
        self.step_index += 1

    def update(self, user_input):
        if self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()

        if (user_input[pygame.K_UP] or user_input[pygame.K_SPACE]) and not self.dino_jump and not self.dino_duck:
            self.dino_jump = True
            self.dino_run = False

        elif not self.dino_jump:
            self.dino_jump = False
            self.dino_run = True

        if user_input[pygame.K_RIGHT]:
            self.dash()

            # TODO load dash in time periods
            # print(self.dino_dash_load)
            #time1 = datetime.time()
            # if self.dino_dash_load == 0:
            # self.dino_dash_load = 1
            # elif self.dino_dash_load == 100:
            #self.dino_dash_load = 0

        else:
            self.parent.game_speed = GAME_VEL
            self.dino_duck = False

        if self.step_index >= 10:
            self.step_index = 0

        if user_input[pygame.K_DOWN]:

            if self.dino_jump:
                self.finish_jump()
            else:
                self.duck()

        else:
            self.dino_duck = False

    def duck(self):
        self.dino_duck = True
        self.image = DUCKING[0] if self.step_index < 5 else DUCKING[1]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = 80
        self.dino_rect.y = POSITION_Y_ENTITIES + \
            (RUNNING[0].get_height() - DUCKING[0].get_height())
        self.step_index += 1

    def finish_jump(self):
        self.dino_rect.y -= 0 if self.jump_vel > 0 else self.jump_vel * 8
        if self.dino_rect.y > Y_POS:
            self.dino_rect.y = Y_POS
            self.dino_jump = False
            self.jump_vel = JUMP_VEL
        self.jump_vel -= 0.8

    def dash(self):
        self.parent.game_speed = GAME_VEL + 10
        self.image = DUCKING[0]
        self.dino_duck = True
        if not self.dino_jump:
            self.dino_rect.y = POSITION_Y_ENTITIES + \
                (RUNNING[0].get_height() - DUCKING[0].get_height())

    def jump(self):
        self.image = JUMPING
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8

        if self.jump_vel < -JUMP_VEL or self.dino_rect.y > Y_POS:
            self.dino_rect.y = Y_POS
            self.dino_jump = False
            self.jump_vel = JUMP_VEL

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
