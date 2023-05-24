import pygame, sys
from player import Player
import obstacle
from alien import Alien, Extra
from random import choice, randint
from laser import Laser
from button import Button

pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
pygame.display.set_caption("Space-Invaders")

ALIENLASER = pygame.USEREVENT + 1
pygame.time.set_timer(ALIENLASER, 800)

bg = pygame.image.load('game_data/background.png')
game_over = pygame.image.load('game_data/game_over.png')
win = pygame.image.load('game_data/win.png')
menu_bg = pygame.image.load('game_data/menu_bg.png')
options_bg = pygame.image.load('game_data/options_bg.png')

class Game:
    def __init__(self):
        # Player setup
        player_sprite = Player((SCREEN_WIDTH / 2, SCREEN_HEIGHT), SCREEN_WIDTH, 10)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Health and Score setup
        self.lives = 3
        self.live_surf = pygame.image.load('game_data/player_lives.png').convert_alpha()
        self.live_x_start_pos = SCREEN_WIDTH - (self.live_surf.get_size()[0] * 2 +20)
        self.score = 0
        self.font = pygame.font.Font('game_data/space_invaders.ttf', 30)

        # Obstacle setup
        self.shape = obstacle.shape
        self.block_size = 10
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (SCREEN_WIDTH / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start=SCREEN_WIDTH/ 15, y_start=480)

        # Alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows=4, cols=12)
        self.alien_direction = 1

        # Extra setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(400, 800)

        # Audio
        self.music = pygame.mixer.Sound('game_data/audio/music.wav')
        self.music.set_volume(0.2)
        self.music.play(loops=-1)

        self.laser_sound = pygame.mixer.Sound('game_data/audio/laser.wav')
        self.laser_sound.set_volume(0.3)
        self.explosion_sound = pygame.mixer.Sound('game_data/audio/explosion.wav')
        self.explosion_sound.set_volume(0.2)

    def get_font(self,size):
        return pygame.font.Font("game_data/space_invaders.ttf", size)

    def main_menu(self):
        while True:
            screen.blit(menu_bg, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()
            MENU_TEXT = self.get_font(100).render("SPACE INVADERS", True, "green")
            MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH / 2, 100))

            PLAY_BUTTON = Button(image=pygame.image.load("game_data/Play Rect.png"), pos=(640, 250),
                                 text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4", hovering_color="green")
            OPTIONS_BUTTON = Button(image=pygame.image.load("game_data/Options Rect.png"), pos=(640, 400),
                                    text_input="OPTIONS", font=self.get_font(75), base_color="#d7fcd4",
                                    hovering_color="green")
            QUIT_BUTTON = Button(image=pygame.image.load("game_data/Quit Rect.png"), pos=(640, 550),
                                 text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="green")

            screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.run()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def options(self):
        while True:
            screen.blit(options_bg, (0, 0))

            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()


            OPTIONS_TEXT = self.get_font(45).render("This is the OPTIONS screen.", True, "white")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 50))
            screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

            MUSIC_ON = Button(image=None, pos=(640, 150), text_input="MUSIC ON", font=self.get_font(75),
                                 base_color="white", hovering_color="Green")
            MUSIC_OFF = Button(image=None, pos=(640, 250), text_input="MUSIC OFF", font=self.get_font(75),
                                  base_color="white", hovering_color="Green")
            SFX_ON = Button(image=None, pos=(640, 450), text_input="SFX ON", font=self.get_font(75),
                                 base_color="white", hovering_color="Green")
            SFX_OFF = Button(image=None, pos=(640, 550), text_input="SFX OFF", font=self.get_font(75),
                                 base_color="white", hovering_color="Green")
            OPTIONS_BACK = Button(image=None, pos=(640, 650), text_input="BACK", font=self.get_font(75),
                                  base_color="white", hovering_color="Green")

            MUSIC_ON.changeColor(OPTIONS_MOUSE_POS)
            MUSIC_ON.update(screen)

            MUSIC_OFF.changeColor(OPTIONS_MOUSE_POS)
            MUSIC_OFF.update(screen)

            SFX_ON.changeColor(OPTIONS_MOUSE_POS)
            SFX_ON.update(screen)

            SFX_OFF.changeColor(OPTIONS_MOUSE_POS)
            SFX_OFF.update(screen)

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if MUSIC_ON.checkForInput(OPTIONS_MOUSE_POS):
                        self.music.set_volume(0.2)
                    if MUSIC_OFF.checkForInput(OPTIONS_MOUSE_POS):
                        self.music.set_volume(0)
                    if SFX_ON.checkForInput(OPTIONS_MOUSE_POS):
                        self.laser_sound.set_volume(0.3)
                        self.explosion_sound.set_volume(0.2)
                    if SFX_OFF.checkForInput(OPTIONS_MOUSE_POS):
                        self.laser_sound.set_volume(0)
                        self.explosion_sound.set_volume(0)
                        # Player.laser_volume(self, 0)


                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        self.main_menu()

            pygame.display.update()

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def alien_setup(self, rows, cols, x_distance=80, y_distance=60, x_offset=150, y_offset=100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0:
                    alien_sprite = Alien('yellow', x, y)
                elif 1 <= row_index <= 2:
                    alien_sprite = Alien('green', x, y)
                else:
                    alien_sprite = Alien('red', x, y)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= SCREEN_WIDTH:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6, SCREEN_HEIGHT)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play()

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right', 'left']), SCREEN_WIDTH))
            self.extra_spawn_time = randint(400, 800)

    def collision_checks(self):
        # player laser
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # obstacle collision
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                # alien collision
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()
                    self.explosion_sound.play()
                # extra collision
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    self.score += 500
                    laser.kill()

        # alien laser
        if self.alien_lasers:
            for laser in self.alien_lasers:
                # obstacle collision
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                # player collision
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1

        # aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf,(x, 5))

    def display_score(self):
        score_surf = self.font.render(f'Score: {self.score}', True, 'white')
        score_rect = score_surf.get_rect(topleft=(5,5))
        screen.blit(score_surf, score_rect)

    def victory_message(self):
        if not self.aliens.sprites():
            victory_surf = self.font.render(f'You won! Final Score: {self.score}', True, 'white')
            victory_rect = victory_surf.get_rect(center=(SCREEN_WIDTH / 2, 200))
            self.laser_sound.set_volume(0)
            screen.blit(win, (0, 0))
            screen.blit(victory_surf, victory_rect)

            VICTORY_MOUSE_POS = pygame.mouse.get_pos()
            BACK_TO_MENU = Button(image=pygame.image.load("game_data/Play Rect.png"), pos=(640, 650),
                                       text_input="BACK TO MENU", font=self.get_font(75), base_color="#d7fcd4",
                                       hovering_color="green")
            BACK_TO_MENU.changeColor(VICTORY_MOUSE_POS)
            BACK_TO_MENU.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_TO_MENU.checkForInput(VICTORY_MOUSE_POS):
                        self.blocks.empty()
                        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start=SCREEN_WIDTH / 15,
                                                       y_start=480)
                        self.alien_setup(rows=4, cols=12)
                        self.lives = 3
                        self.score = 0
                        screen.fill((0, 0, 0))
                        self.main_menu()

            pygame.display.flip()
            pygame.display.update()

    def game_over(self):
        if self.lives <= 0:
            defeat_surf = self.font.render(f'You lost! Final Score: {self.score}', True, 'white')
            defeat_rect = defeat_surf.get_rect(center=(SCREEN_WIDTH / 2, 200))
            self.laser_sound.set_volume(0)
            self.explosion_sound.set_volume(0)
            screen.blit(game_over, (0, 0))
            screen.blit(defeat_surf, defeat_rect)

            GAME_OVER_MOUSE_POS = pygame.mouse.get_pos()
            BACK_TO_MENU = Button(image=pygame.image.load("game_data/Play Rect.png"), pos=(640, 650),
                                 text_input="BACK TO MENU", font=self.get_font(75), base_color="#d7fcd4",
                                 hovering_color="green")
            BACK_TO_MENU.changeColor(GAME_OVER_MOUSE_POS)
            BACK_TO_MENU.update(screen)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_TO_MENU.checkForInput(GAME_OVER_MOUSE_POS):
                        self.blocks.empty()
                        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start=SCREEN_WIDTH / 15,
                                                       y_start=480)
                        self.aliens.empty()
                        self.alien_setup(rows=4, cols=12)
                        self.lives = 3
                        self.score = 0
                        screen.fill((0, 0, 0))
                        self.main_menu()


            pygame.display.flip()
            pygame.display.update()

    def run(self):
        while True:
            screen.fill((0, 0, 0))
            screen.blit(bg, (0, 0))
            bg.set_alpha(200)
            # self.main_menu()
            self.player.update()
            self.aliens.update(self.alien_direction)
            self.extra.update()
            self.alien_lasers.update()

            self.extra_alien_timer()
            self.collision_checks()
            self.alien_position_checker()

            self.player.sprite.lasers.draw(screen)
            self.player.draw(screen)
            self.blocks.draw(screen)
            self.aliens.draw(screen)
            self.alien_lasers.draw(screen)
            self.extra.draw(screen)

            self.display_lives()
            self.display_score()
            self.victory_message()
            self.game_over()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == ALIENLASER:
                    game.alien_shoot()

            pygame.display.flip()
            clock.tick(90)
            pygame.display.update()


class CRT:
    def __init__(self):
        self.tv = pygame.image.load('game_data/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def create_crt_lines(self):
        line_height = 3
        line_amount = int(SCREEN_HEIGHT / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, 'black', (0, y_pos), (SCREEN_WIDTH, y_pos) ,1)

    def draw(self):
        self.tv.set_alpha(randint(75, 90))
        self.create_crt_lines()
        screen.blit(self.tv, (0, 0))

    def disabled(self):
        self.tv.set_alpha(0)
        screen.blit(self.tv, (0, 0))


if __name__ == '__main__':

    game = Game()
    crt = CRT()
    game.main_menu()





