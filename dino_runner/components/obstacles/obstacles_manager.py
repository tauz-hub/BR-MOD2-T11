from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import RUNNING, DUCKING


class ObstacleManager:
    def __init__(self, parent):
        self.parent = parent
        self.obstacles = {"smallCactus": Cactus(
            "smallCactus"), "largeCactus":  Cactus("largeCactus"), "bird":  Bird()}

    def update(self):
        self.obstacles['bird'].update()
        self.checkCollision()
        self.generateNewObstacles()

    def generateNewObstacles(self):
        for key, obstacle in self.obstacles.items():

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

    def checkCollision(self):
        rate_ajust = 0
        for key, obstacle in self.obstacles.items():
            current_y = obstacle.y - rate_ajust

            if self.parent.player.dino_duck:
                rate_ajust = RUNNING[0].get_height() - DUCKING[0].get_height()

            area = (obstacle.x, current_y), (obstacle.x, current_y + obstacle.rect.height), (obstacle.x +
                                                                                             obstacle.rect.width, current_y + obstacle.rect.height), (obstacle.x + obstacle.rect.width, current_y)
            discount = 10

            for vertex in area:
                if (self.parent.player.dino_rect.x <= vertex[0] <= self.parent.player.dino_rect.x - discount + self.parent.player.image.get_width()) and (self.parent.player.dino_rect.y <= vertex[1] <= self.parent.player.dino_rect.y - discount + self.parent.player.image.get_height()):
                    print(key)

                    self.parent.death_count += 1
                    self.parent.playing = False
                    break

    def reset_obstacles(self):
        self.obstacles = {"smallCactus": Cactus(
            "smallCactus"), "largeCactus":  Cactus("largeCactus"), "bird":  Bird()}

    def area(self):
        return (self.x, self.y), (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), (self.x + self.width, self.y)

    def draw(self):

        for obstacle in self.obstacles.values():
            obstacle.draw(self.parent.screen, self.parent.game_speed)
