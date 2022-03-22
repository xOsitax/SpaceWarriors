import pygame
from os import path
import sys
from random import choice
import random
from menu import *
from models import Player, EasyEnemy, MediumEnemy, HardEnemy, EnemyBullet
pygame.init()
pygame.font.init()
pygame.mixer.init()


class Game:
    # Initialize the game
    def __init__(self):

        #start up the menu

        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 960, 540
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.font_name = pygame.font.Font("8bit.ttf", 20)
        self.BLACK, self.WHITE = (0,0,0), (255,255,255)
        self.background = pygame.image.load('bg.jpg')
        self.main_menu = MainMenu(self)
        self.multiplayer = Multiplayer(self)
        self.leaderboard = Leaderboard(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.screen = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.curr_menu = self.main_menu
        self.counter = 0
        self.hs = 80
        self.initial = "LS"
        self.HS = "highscore.txt"
        self.load_scores()


        # Set up the player
        player_sprite = Player((self.DISPLAY_W / 2, self.DISPLAY_H - 50), self.DISPLAY_W, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Set up the enemies
        self.enemies = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.score_value = 0
        self.spawn = True
        self.spawn_delay = 1800
        self.spawn_time = 0
        self.enemy_max = 0

        # Set up the player health
        self.health = 3
        self.health_surface = pygame.image.load("heart.png").convert_alpha()
        self.health_x_start_pos = self.DISPLAY_W - (self.health_surface.get_size()[0] * 3 + 620)

        # Set up the three rows
        self.toprow = self.DISPLAY_H - 560
        self.midrow = self.DISPLAY_H - 500
        self.botrow = self.DISPLAY_H - 440

        # Declare the explosion sound effect
        #self.explode_sound = pygame.mixer.Sound("explosion.wav")
        #self.explode_sound.set_volume(0.3)

    # Sets up the enemies
    def enemy_spawn(self):
        # The first level of difficulty: spawns in only easy enemies
        if self.counter <= 15 and self.spawn is True and self.enemy_max < 20:
            easy_enemy_sprite = EasyEnemy(random.randint(10, self.DISPLAY_W - 10),
                                          random.choice([self.toprow, self.midrow, self.botrow]), 3, self.DISPLAY_W)
            self.enemies.add(easy_enemy_sprite)
            self.spawn_time = pygame.time.get_ticks()
            self.spawn = False
            self.enemy_max += 1
        # The second level of difficulty: spawns in easy and medium enemies at a slightly faster pace
        elif 45 >= self.counter > 15 and self.spawn is True and self.enemy_max < 20:
            easy_enemy_sprite = EasyEnemy(random.randint(10, self.DISPLAY_W - 10),
                                          random.choice([self.toprow, self.midrow, self.botrow]), 3, self.DISPLAY_W)
            medium_enemy_sprite = MediumEnemy(random.randint(10, self.DISPLAY_W - 10),
                                              random.choice([self.toprow, self.midrow, self.botrow]), 4, self.DISPLAY_W)
            self.enemies.add(random.choice([medium_enemy_sprite, easy_enemy_sprite]))
            self.spawn_time = pygame.time.get_ticks()
            self.spawn = False
            self.enemy_max += 1
            self.spawn_delay = 1400
        # The final lever of difficulty: spawns in easy, medium, and hard enemies at a rapid pace
        elif self.counter > 45 and self.spawn is True and self.enemy_max < 20:
            easy_enemy_sprite = EasyEnemy(random.randint(10, self.DISPLAY_W - 10),
                                          random.choice([self.toprow, self.midrow, self.botrow]), 3, self.DISPLAY_W)
            medium_enemy_sprite = MediumEnemy(random.randint(10, self.DISPLAY_W - 10),
                                              random.choice([self.toprow, self.midrow, self.botrow]), 4, self.DISPLAY_W)
            hard_enemy_sprite = HardEnemy(random.randint(10, self.DISPLAY_W - 10),
                                          random.choice([self.toprow, self.midrow, self.botrow]), 5, self.DISPLAY_W)
            self.enemies.add(random.choice([hard_enemy_sprite, medium_enemy_sprite, easy_enemy_sprite]))
            self.spawn_time = pygame.time.get_ticks()
            self.spawn = False
            self.enemy_max += 1
            self.spawn_delay = 1200

    def respawn_timer(self):
        if not self.spawn:
            current_time = pygame.time.get_ticks()
            if current_time - self.spawn_time >= self.spawn_delay:
                self.spawn = True

    # Checks if the bullet collides with an enemy or player
    def collision_checks(self):
        # Check for player bullets
        if self.player.sprite.bullets:
            for bullet in self.player.sprite.bullets:
                # After a collision with an enemy, delete the bullet
                if pygame.sprite.spritecollide(bullet, self.enemies, True):
                    bullet.kill()
                    self.score_value += 10
                    self.enemy_max -= 1
                    pygame.mixer.Sound.play(self.explode_sound)

        # Check for enemy bullets
        if self.enemy_bullets:
            for bullet in self.enemy_bullets:
                # After a collision with the player, delete the bullet and register hit
                if pygame.sprite.spritecollide(bullet, self.player, False):
                    bullet.kill()
                    self.health -= 1
                    if self.health <= 0:
                        pygame.quit()
                        sys.exit()

    # Enemy shoot
    def enemy_shoot(self):
        if self.enemies.sprites():
            random_enemy = choice(self.enemies.sprites())
            enemy_bullet_sprite = EnemyBullet(random_enemy.rect.center, 6, self.DISPLAY_H)
            self.enemy_bullets.add(enemy_bullet_sprite)
            self.enemy_bullet_sprite = pygame.USEREVENT + 1
            pygame.time.set_timer(self.enemy_bullet_sprite, 750)

    # load the highscores
    def load_scores(self):
        self.dir = path.dirname(__file__)
        try:
            # try to read the file
            with open(path.join(self.dir, self.HS), 'r+') as f:
                self.highscore = int(f.read())
        except:
            # create the file
            with open(path.join(self.dir, self.HS), 'w'):
                self.highscore = 0

    # Display the score
    def show_score(self):
        pygame.font.init()
        font = pygame.font.SysFont("Grobold", 20)
        score = font.render("Score: " + str(self.score_value), True, (255, 255, 255))
        self.screen.blit(score, (0, 0))

    # Display player health
    def show_health(self):
        for heart in range(self.health):
            x = self.health_x_start_pos + (heart * self.health_surface.get_size()[0] + 10)
            self.screen.blit(self.health_surface, (x, self.DISPLAY_H - 60))

    def timer(self):
        self.clock = pygame.time.Clock()
        time_delay = 1000
        TIMER_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(TIMER_EVENT, time_delay)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    # Method that runs the game
    def run(self):
        self.player.sprite.bullets.draw(self.screen)
        # self.enemies.sprite.bullets.draw(self.screen)
        self.player.update()
        self.player.draw(self.screen)
        self.enemies.draw(self.screen)
        self.enemy_bullets.update()
        self.enemy_bullets.draw(self.screen)
        self.collision_checks()
        self.enemies.update()
        self.show_score()
        self.show_health()
        self.enemy_spawn()
        self.respawn_timer()
        self.timer()

    def game_loop(self):
        while self.playing:
            self.check_events()
            self.run()

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font("8bit.ttf", 25)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False







