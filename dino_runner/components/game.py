import pygame

from dino_runner.utils.constants import *
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacles_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
FONT_STYLE = "freesansbold.ttf"


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = GAME_VEL
        self.score = 0
        self.best_score = 0
        self.death_count = 0
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur(self)
        self.position_for_text_screen_height = SCREEN_HEIGHT // 2
        self.position_for_text_screen_width = SCREEN_WIDTH // 2
        self.obstacle_manager = ObstacleManager(self)
        self.power_up_manager = PowerUpManager(self)

    def execute(self):
        self.running = True

        while self.running:
            if not self.playing:
                self.show_menu()

        pygame.display.quit()
        pygame.quit()

    def run(self):

        self.playing = True

        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        while self.playing:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):

        user_input = pygame.key.get_pressed()
        self.player.update(user_input)

        self.obstacle_manager.update()

        self.power_up_manager.update()
        self.update_score()
        self.draw_power_up_time()

    def update_score(self):
        self.score += 1

        if self.score % 100 == 0 and self.game_speed < MAX_GAME_VEL:
            self.game_speed += 2

    def draw_power_up_time(self):
        if self.player.has_power_up:

            time_to_show = round(
                (self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)

            if time_to_show >= 0:

                text_message = f"{round(time_to_show)}s"
                self.draw_texts(text_message, self.position_for_text_screen_width,
                                100, 40)
                pygame.display.update()
            else:
                self.power_up_manager.reset_power_ups()
                self.power_up_manager.remove_player_power_up()

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw()
        self.power_up_manager.draw()
        self.draw_score()

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

    def draw_score(self):
        font = pygame.font.Font(FONT_STYLE, 22)
        text = font.render(
            f"Score: {self.score} | Best Score: {self.best_score}", False, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 50)
        self.screen.blit(text, text_rect)

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self.reset_values()
                self.run()

    def reset_values(self):
        self.score = 0
        self.game_speed = GAME_VEL

    def draw_texts(self, text_message, set_position_x, set_position_y, font_size=22):
        font = pygame.font.Font(FONT_STYLE, font_size)
        text = font.render(text_message, False, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (set_position_x,
                            set_position_y)
        self.screen.blit(text, text_rect)

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        position_x_text = self.position_for_text_screen_width
        position_y_text = self.position_for_text_screen_height

        if self.score > self.best_score:
            self.best_score = self.score

        if self.death_count == 0:
            self.draw_texts("Press any key to start",
                            position_x_text, position_y_text)

        else:
            self.power_up_manager.remove_player_power_up()
            self.draw_texts(
                f"Press any key to restart | Score: {self.score} | Deaths: {self.death_count}", position_x_text, position_y_text - 40)
            self.screen.blit(RESET, (self.position_for_text_screen_width -
                                     20, self.position_for_text_screen_height))

        pygame.display.update()
        self.handle_events_on_menu()
