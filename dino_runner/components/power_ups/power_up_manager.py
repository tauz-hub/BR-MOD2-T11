from dino_runner.components.power_ups.shield import Shield
from dino_runner.utils.constants import *
import pygame
from dino_runner.components.power_ups.hammer import Hammer
from dino_runner.components.power_ups.sword import Sword


class PowerUpManager:
    def __init__(self, parent):
        self.parent = parent
        self.power_ups = {
            "shield": Shield(), "hammer": Hammer(), "sword": Sword()}
        self.when_appears = 0

    def update(self):
        self.generateNewPowerUps()
        self.checkCollision()

    def generateNewPowerUps(self):
        for key, power_up in self.power_ups.items():

            if self.parent.x_pos_bg < self.parent.game_speed and power_up.x <= 0:
                self.reset_power_up(key)
                self.remove_player_power_up()

                self.power_ups[key].draw(
                    self.parent.screen, self.parent.game_speed)

    def checkCollision(self):
        rate_ajust = 0

        if len(self.power_ups) > 0:
            for key, power_up in self.power_ups.items():
                stop_checks = False
                current_y = power_up.y
                if self.parent.player.dino_duck:
                    rate_ajust = RUNNING[0].get_height() - \
                        DUCKING[0].get_height()
                current_y = power_up.y - rate_ajust

                area = (power_up.x, current_y), (power_up.x, current_y + power_up.rect.height), (power_up.x +
                                                                                                 power_up.rect.width, current_y + power_up.rect.height), (power_up.x + power_up.rect.width, current_y)
                discount = 10

                for vertex in area:
                    if (self.parent.player.dino_rect.x <= vertex[0] <= self.parent.player.dino_rect.x - discount + self.parent.player.image.get_width()) and (self.parent.player.dino_rect.y <= vertex[1] <= self.parent.player.dino_rect.y - discount + self.parent.player.image.get_height()):

                        self.remove_player_power_up()
                        self.parent.player.has_power_up = True
                        self.parent.player.active_power_up = power_up
                        self.parent.player.type = power_up.type_power_up
                        self.parent.player.power_up_time = pygame.time.get_ticks() + \
                            (power_up.duration * 1000)

                        self.remove_power_up_from_map()
                        stop_checks = True
                        break

                if stop_checks:
                    break

    def remove_player_power_up(self):
        self.parent.player.has_power_up = False
        self.parent.player.active_power_up = any
        self.parent.player.power_up_time = 0
        self.parent.player.type = DEFAULT_TYPE

    def remove_power_up_from_map(self):
        self.power_ups.clear()

    def reset_power_ups(self):
        self.power_ups = {
            "shield": Shield(), "hammer": Hammer(), "sword": Sword()}

    def reset_power_up(self, key):
        match key:
            case "shield":
                self.power_ups[key] = Shield()
            case "hammer":
                self.power_ups[key] = Hammer()
            case "sword":
                self.power_ups[key] = Sword()

    def area(self):
        return (self.x, self.y), (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), (self.x + self.width, self.y)

    def draw(self):

        for power_up in self.power_ups.values():
            power_up.draw(self.parent.screen, self.parent.game_speed)
