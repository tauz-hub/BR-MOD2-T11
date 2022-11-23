import pygame

from dino_runner.utils.constants import SMALL_CACTUS
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird


class ObstacleManager:
    def __init__(self, parent):
        self.parent = parent
        self.obstacles = {"smallCactus": Cactus(
            "smallCactus"), "largeCactus":  Cactus("largeCactus"), "bird":  Bird()}

    def update(self):
        self.obstacles['bird'].update()
        for key, obstacle in self.obstacles.items():

            area = (obstacle.x, obstacle.y), (obstacle.x, obstacle.y + obstacle.rect.height), (obstacle.x +
                                                                                               obstacle.rect.width, obstacle.y + obstacle.rect.height), (obstacle.x + obstacle.rect.width, obstacle.y)
            discount = 10

            for vertex in area:
                if (self.parent.player.dino_rect.x <= vertex[0] <= self.parent.player.dino_rect.x - discount + self.parent.player.image.get_width()) and (self.parent.player.dino_rect.y <= vertex[1] <= self.parent.player.dino_rect.y - discount + self.parent.player.image.get_height()):
                    print(key)

                    self.parent.playing = False

            if self.parent.x_pos_bg < self.parent.game_speed and obstacle.x <= 0:
                match key:
                    case "smallCactus":
                        self.obstacles[key] = Cactus("smallCactus")
                    case "largeCactus":
                        self.obstacles[key] = Cactus("largeCactus")
                    case "bird":
                        self.obstacles[key] = Bird()

                self.obstacles[key].draw(
                    self.parent.screen, self.parent.game_speed)
        pass

    def area(self):
        return (self.x, self.y), (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), (self.x + self.width, self.y)

    def draw(self):

        for obstacle in self.obstacles.values():
            obstacle.draw(self.parent.screen, self.parent.game_speed)
