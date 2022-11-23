import pygame

from dino_runner.utils.constants import *
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.largeCactus import LargeCactus
from dino_runner.components.smallCactus import SmallCactus
from dino_runner.components.bird import Bird


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = GAME_VEL
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur(self)

        self.obstacles = {"smallCactus": SmallCactus(
        )}

    def run(self):

        self.playing = True

        while self.playing:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def area(self) -> tuple:
        return (self.x, self.y), (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), (self.x + self.width, self.y)

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)

        for key, obstacle in self.obstacles.items():

            area = (obstacle.x, obstacle.y), (obstacle.x, obstacle.y + obstacle.rect.height), (obstacle.x +
                                                                                               obstacle.rect.width, obstacle.y + obstacle.rect.height), (obstacle.x + obstacle.rect.width, obstacle.y)
            discount = 10
            for vertex in area:
                if (self.player.dino_rect.x <= vertex[0] <= self.player.dino_rect.x - discount + self.player.image.get_width()) and (self.player.dino_rect.y <= vertex[1] <= self.player.dino_rect.y - discount + self.player.image.get_height()):
                    print(key)

                    self.playing = False

            if self.x_pos_bg < self.game_speed and obstacle.x <= 0:
                match key:
                    case "smallCactus":
                        self.obstacles[key] = SmallCactus()

                self.obstacles[key].draw(self.screen, self.game_speed)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)

        # obstacles
        self.obstacles['smallCactus'].draw(self.screen, self.game_speed)

        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
