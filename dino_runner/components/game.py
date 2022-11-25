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
        self.timer_power_up_time()

    def update_score(self):
        self.score += 1

        if self.score % 100 == 0 and self.game_speed < MAX_GAME_VEL:
            self.game_speed += 2

    def timer_power_up_time(self):
        if self.player.has_power_up:

            self.time_to_show = round(
                (self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)

            if self.time_to_show < 0:
                self.power_up_manager.reset_power_ups()
                self.power_up_manager.remove_player_power_up()

    def put_power_up(self, power_up):
        self.screen.blit(
            power_up, (50, SCREEN_HEIGHT - 130))

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw()
        self.power_up_manager.draw()
        self.draw_score()
        self.draw_dash_bar()

        if self.player.has_power_up:
            self.put_power_up(self.player.active_power_up.image)
            self.draw_timer_power_up()

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

    def draw_timer_power_up(self):

        self.draw_texts(f"{round(self.time_to_show)}s",
                        100, SCREEN_HEIGHT - 120, 24)

    def draw_dash_bar(self):
        percentage = self.player.dino_dash_load
        bar_dash = "|" * percentage
        self.draw_texts(f"Dash bar: {bar_dash}", 50, SCREEN_HEIGHT - 50, 24)

    def draw_score(self):
        self.draw_texts(
            f"Score: {self.score} | Best Score: {self.best_score}", 900, 50, 24, True)

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

    def draw_texts(self, text_message, set_position_x, set_position_y, font_size=22, ally_with_center=False):
        font = pygame.font.Font(FONT_STYLE, font_size)
        text = font.render(text_message, False, (0, 0, 0))

        text_rect = (set_position_x, set_position_y)
        if ally_with_center:
            text_rect = text.get_rect()
            text_rect.center = (set_position_x,
                                set_position_y)
        self.screen.blit(text, text_rect)

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        position_x_text = self.position_for_text_screen_width
        position_y_text = self.position_for_text_screen_height - 50

        if self.score > self.best_score:
            self.best_score = self.score

        if self.death_count == 0:
            self.draw_texts("Press any key to start",
                            position_x_text, position_y_text, 30, True)

            self.screen.blit(
                SHIELD, (position_x_text - 150, position_y_text + 80))
            self.draw_texts(" | protect you for a while",
                            position_x_text - 100, position_y_text + 90, 22)

            self.screen.blit(
                HAMMER, (position_x_text - 150, position_y_text + 140))
            self.draw_texts(" | can destroy an obstacle",
                            position_x_text - 100, position_y_text + 150, 22)

            self.screen.blit(
                SWORD, (position_x_text - 150, position_y_text + 200))
            self.draw_texts(" | earn points by killing birds",
                            position_x_text - 100, position_y_text + 210, 22)
        else:
            self.power_up_manager.remove_player_power_up()
            self.draw_texts(
                f"Score: {self.score}", position_x_text, position_y_text - 40, 22, True)
            self.screen.blit(RESET, (self.position_for_text_screen_width -
                                     20, self.position_for_text_screen_height + 80))

            self.draw_texts(
                f"Deaths: {self.death_count}", position_x_text, position_y_text, 22, True)

            self.draw_texts(
                f"Press any key to restart", position_x_text, position_y_text + 40, 22, True)

        pygame.display.update()
        self.handle_events_on_menu()
