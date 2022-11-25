import pygame
from dino_runner.utils.constants import *
X_POS = 80
Y_POS = 310
JUMP_VEL = 8.5


DUCK_IMG = {DEFAULT_TYPE: DUCKING,
            SHIELD_TYPE: DUCKING_SHIELD, HAMMER_TYPE: DUCKING_HAMMER,  SWORD_TYPE: DUCKING_SWORD}
JUMP_IMG = {DEFAULT_TYPE: JUMPING,
            SHIELD_TYPE: JUMPING_SHIELD, HAMMER_TYPE: JUMPING_HAMMER, SWORD_TYPE: JUMPING_SWORD}
RUN_IMG = {DEFAULT_TYPE: RUNNING,
           SHIELD_TYPE: RUNNING_SHIELD, HAMMER_TYPE: RUNNING_HAMMER, SWORD_TYPE:  RUNNING_SWORD}


class Dinosaur:
    def __init__(self, parent) -> None:
        self.type = DEFAULT_TYPE
        self.image = RUN_IMG[self.type][0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = 80
        self.dino_rect.y = POSITION_Y_ENTITIES
        self.step_index = 0
        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False
        self.has_power_up = False
        self.active_power_up = any
        self.power_up_time = 0
        self.dino_dash_load = 100

        self.jump_vel = JUMP_VEL
        self.parent = parent

        self.ant_vel = 0
        self.setup_state()

    def setup_state(self):
        self.has_power_up = False
        self.shield = False
        self.show_text = False
        self.shield_time_up = 0

    def update(self, user_input):
        if self.dino_run:
            self.run()
            self.dino_jump = False
            self.dino_duck = False

        elif self.dino_jump:
            self.jump()
            self.dino_run = False
            self.dino_duck = False

        if (user_input[pygame.K_UP] or user_input[pygame.K_SPACE]) and not self.dino_jump and not self.dino_duck:
            self.dino_jump = True
            self.dino_run = False

        elif not self.dino_jump:
            self.dino_jump = False
            self.dino_run = True

        if user_input[pygame.K_RIGHT]:
            if self.ant_vel == 0:
                self.ant_vel = self.parent.game_speed
            self.dash()

            # TODO load dash in time periods

        else:
            if not self.ant_vel == 0:
                self.parent.game_speed = self.ant_vel
                self.ant_vel = 0

            self.dino_duck = False

        if self.step_index >= 9:
            self.step_index = 0

        if user_input[pygame.K_DOWN]:

            if self.dino_jump:
                self.finish_jump()
            else:
                self.duck()

        if self.has_power_up:
            power_up_name = self.active_power_up.type_power_up

            if power_up_name == "shield":
                self.put_power_up(SHIELD)
            elif power_up_name == "hammer":
                self.put_power_up(HAMMER)
            elif power_up_name == "sword":
                self.put_power_up(SWORD)

    def expand_vision(self):
        self.parent.screen = pygame.display.set_mode(
            (SCREEN_WIDTH + 2000, SCREEN_HEIGHT))

    def put_power_up(self, power_up):
        self.parent.screen.blit(power_up, (self.dino_rect.x, self.dino_rect.y))

    def run(self):
        self.dino_run = True
        self.image = RUN_IMG[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = 80
        self.dino_rect.y = POSITION_Y_ENTITIES
        self.step_index += 1

    def duck(self):
        self.dino_duck = True
        self.image = DUCK_IMG[self.type][self.step_index // 5]
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

        self.parent.game_speed = self.ant_vel + 15
        self.image = DUCK_IMG[self.type][self.step_index // 5]
        self.dino_duck = True
        if not self.dino_jump:
            self.dino_rect.y = POSITION_Y_ENTITIES + \
                (RUNNING[0].get_height() - DUCKING[0].get_height())

    def jump(self):
        self.image = JUMP_IMG[self.type]
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8

        if self.jump_vel < -JUMP_VEL or self.dino_rect.y > Y_POS:
            self.dino_rect.y = Y_POS
            self.dino_jump = False
            self.jump_vel = JUMP_VEL

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
