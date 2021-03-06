import pygame
import sys
from random import choice
import random
import json
import io

from models import Player, EasyEnemy, MediumEnemy, HardEnemy, EnemyBullet, Asteroid, Boom, screen_height, \
    screen_width

pygame.mixer.init()

# Declare the sound effects
explode_sound = pygame.mixer.Sound("assets/sounds/sfx_explosion.wav")
hit_sound = pygame.mixer.Sound("assets/sounds/sfx_hit.mp3")
crack_sound = pygame.mixer.Sound("assets/sounds/sfx_crack.wav")
break_sound = pygame.mixer.Sound("assets/sounds/sfx_break.wav")
menu_move_up = pygame.mixer.Sound("assets/sounds/sfx_menu_move1.wav")
menu_move_down = pygame.mixer.Sound("assets/sounds/sfx_menu_move2.wav")
menu_select = pygame.mixer.Sound("assets/sounds/sfx_menu_select2.wav")
pause_sound = pygame.mixer.Sound("assets/sounds/sfx_sounds_pause3_in.wav")
unpause_sound = pygame.mixer.Sound("assets/sounds/sfx_sounds_pause3_out.wav")
death_sound = pygame.mixer.Sound("assets/sounds/sfx_exp_double3.wav")
count_sound = pygame.mixer.Sound("assets/sounds/sfx_count.wav")
go_sound = pygame.mixer.Sound("assets/sounds/sfx_go.wav")
ready_sound = pygame.mixer.Sound("assets/sounds/sfx_ready.wav")


# Sets the volume for the sounds effects
def volume_sfx(level=0.2):
    explode_sound.set_volume(level)
    hit_sound.set_volume(level)
    crack_sound.set_volume(level)
    break_sound.set_volume(level)
    menu_select.set_volume(level)
    menu_move_down.set_volume(level)
    menu_move_up.set_volume(level)
    pause_sound.set_volume(level)
    unpause_sound.set_volume(level)
    death_sound.set_volume(level)
    count_sound.set_volume(level)
    go_sound.set_volume(level)
    ready_sound.set_volume(level)
    game.player_sprite.shoot_sound.set_volume(level)
    multi.player_1_sprite.shoot_sound.set_volume(level)
    multi.player_2_sprite.shoot_sound.set_volume(level)


# Sets the volume for the music
volume_music = 0.2


# Class that handles singleplayer gameplay
class Game:
    # Initialize the game
    def __init__(self):

        # Set up the player
        self.player_sprite = Player("assets/player.png", (screen_width / 2, screen_height - 60), screen_width,
                                    screen_height, 5)
        self.player = pygame.sprite.GroupSingle(self.player_sprite)
        self.initial = ''
        self.hs = 0
        self.score_value = 0
        self.iframe = False
        self.iframe_duration = 1000
        self.iframe_time = 0
        self.flash = True

        # Set up the enemies
        self.enemies = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.spawn = True
        self.spawn_delay = 1800
        self.spawn_time = 0
        self.enemy_count = 0
        self.enemy_max = 10

        self.start_delay = True

        # Set up the asteroids
        self.asteroids = pygame.sprite.Group()
        self.a_spawn = True
        self.a_spawn_delay = 3000
        self.a_spawn_time = 0

        # Kill animations
        self.boom = pygame.sprite.Group()

        # Set up the player health
        self.health = 3
        self.health_surface = pygame.image.load("assets/heart.png").convert_alpha()
        self.health_x_start_pos = screen_width - (self.health_surface.get_size()[0] * 3 + 600)

        # Set up the three rows
        self.toprow = screen_height - 560
        self.midrow = screen_height - 500
        self.botrow = screen_height - 440

    # Asteroid spawns
    def asteroid_spawn(self):
        if self.a_spawn is True:
            asteroid_sprite = Asteroid(random.randint(75, screen_width - 75), -50, 3, random.choice([-1, 1]))
            self.asteroids.add(asteroid_sprite)
            self.a_spawn_time = pygame.time.get_ticks()
            self.a_spawn = False

    # Sets up the enemies
    def enemy_spawn(self):
        # The first level of difficulty: spawns in only easy enemies
        if counter <= 15 and self.spawn is True and self.enemy_count < self.enemy_max:
            easy_enemy_sprite = EasyEnemy(random.randint(10, screen_width - 10),
                                          random.choice([self.toprow, self.midrow, self.botrow]), 3, screen_width)
            self.enemies.add(easy_enemy_sprite)
            self.spawn_time = pygame.time.get_ticks()
            self.spawn = False
            self.enemy_count += 1
        # The second level of difficulty: spawns in easy and medium enemies at a slightly faster pace
        elif 45 >= counter > 15 and self.spawn is True and self.enemy_count < self.enemy_max:
            easy_enemy_sprite = EasyEnemy(random.randint(10, screen_width - 10),
                                          random.choice([self.toprow, self.midrow, self.botrow]), 3, screen_width)
            medium_enemy_sprite = MediumEnemy(random.randint(10, screen_width - 10),
                                              random.choice([self.toprow, self.midrow, self.botrow]), 4, screen_width)
            self.enemies.add(random.choice([medium_enemy_sprite, easy_enemy_sprite]))
            self.spawn_time = pygame.time.get_ticks()
            self.spawn = False
            self.enemy_count += 1
            self.spawn_delay = 1400
        # The final lever of difficulty: spawns in easy, medium, and hard enemies at a rapid pace
        elif counter > 45 and self.spawn is True and self.enemy_count < self.enemy_max:
            easy_enemy_sprite = EasyEnemy(random.randint(10, screen_width - 10),
                                          random.choice([self.toprow, self.midrow, self.botrow]), 3, screen_width)
            medium_enemy_sprite = MediumEnemy(random.randint(10, screen_width - 10),
                                              random.choice([self.toprow, self.midrow, self.botrow]), 4, screen_width)
            hard_enemy_sprite = HardEnemy(random.randint(10, screen_width - 10),
                                          random.choice([self.toprow, self.midrow, self.botrow]), 5, screen_width)
            self.enemies.add(random.choices([hard_enemy_sprite, medium_enemy_sprite, easy_enemy_sprite],
                                            weights=(15, 35, 50), k=1))
            self.spawn_time = pygame.time.get_ticks()
            self.spawn = False
            self.enemy_count += 1
            self.spawn_delay = 1200

    def respawn_timer(self):
        if not self.spawn:
            current_time = pygame.time.get_ticks()
            if current_time - self.spawn_time >= self.spawn_delay:
                self.spawn = True
        if not self.a_spawn:
            a_current_time = pygame.time.get_ticks()
            if a_current_time - self.a_spawn_time >= self.a_spawn_delay:
                self.a_spawn = True

    def iframes(self):
        if self.iframe:
            i_current_time = pygame.time.get_ticks()
            if i_current_time - self.iframe_time >= self.iframe_duration:
                self.iframe = False
                self.player_sprite.image.set_alpha(255)

    # Checks if the bullet collides with an enemy or player
    def collision_checks(self):
        # Check if enemy is hit
        if self.enemies:
            for enemy in self.enemies:
                # After a collision with player bullet, delete enemy and increase score
                if pygame.sprite.spritecollide(enemy, self.player_sprite.bullets, True):
                    enemy.kill()
                    self.score_value += 10
                    self.enemy_count -= 1
                    pygame.mixer.Sound.play(explode_sound)
                    die_sprite = Boom(enemy.rect.center, "assets/explosion.png")
                    self.boom.add(die_sprite)

        # Check if player is hit
        if self.enemy_bullets and not self.iframe:
            for bullet in self.enemy_bullets:
                # After a collision with the player, delete the bullet and register hit
                if pygame.sprite.spritecollide(bullet, self.player, False):
                    bullet.kill()
                    self.health -= 1
                    self.iframe = True
                    self.iframe_time = pygame.time.get_ticks()
                    if self.health != 0:
                        pygame.mixer.Sound.play(hit_sound)

        # Check if asteroid is hit or hits player
        if self.asteroids and not self.iframe:
            for asteroid in self.asteroids:
                # After a collision with the player, delete asteroid and register hit
                if pygame.sprite.spritecollide(asteroid, self.player, False):
                    asteroid.kill()
                    die_sprite = Boom(asteroid.rect.center, "assets/asteroid_broken.png", asteroid.angle)
                    self.boom.add(die_sprite)
                    self.health -= 1
                    self.iframe = True
                    self.iframe_time = pygame.time.get_ticks()
                    pygame.mixer.Sound.play(hit_sound)
        if self.asteroids:
            for asteroid in self.asteroids:
                if pygame.sprite.spritecollide(asteroid, self.player_sprite.bullets, True):
                    asteroid.health -= 1
                    asteroid.orig_image = asteroid.cracked_image
                    if asteroid.health != 0:
                        pygame.mixer.Sound.play(crack_sound)
                    if asteroid.health == 0:
                        self.score_value += 20
                        pygame.mixer.Sound.play(break_sound)
                        asteroid.kill()
                        die_sprite = Boom(asteroid.rect.center, "assets/asteroid_broken.png", asteroid.angle)
                        self.boom.add(die_sprite)

    # Enemy shoot
    def enemy_shoot(self):
        if self.enemies.sprites():
            random_enemy = choice(self.enemies.sprites())
            enemy_bullet_sprite = EnemyBullet("assets/enemyBullet.png", random_enemy.rect.center, 6, screen_height)
            self.enemy_bullets.add(enemy_bullet_sprite)

    # Display the score
    def show_score(self):
        score = font.render("Score: " + str(self.score_value), True, WHITE)
        screen.blit(score, (0, 0))

    # Display player health
    def show_health(self):
        for heart in range(self.health):
            x = self.health_x_start_pos + (heart * (self.health_surface.get_size()[0] + 10))
            screen.blit(self.health_surface, (x, screen_height - 65))

    # Method that runs the game
    def run(self):
        self.player.sprite.bullets.draw(screen)
        self.player.update()
        self.player.draw(screen)
        self.iframes()
        self.enemies.draw(screen)
        self.enemy_bullets.update()
        self.enemy_bullets.draw(screen)
        self.asteroids.draw(screen)
        self.asteroids.update()
        self.boom.draw(screen)
        self.boom.update()
        self.collision_checks()
        self.enemies.update()
        self.show_score()
        self.show_health()
        if not self.start_delay:
            self.enemy_spawn()
            self.asteroid_spawn()
        self.respawn_timer()


# Class that handles multiplayer gameplay
class Multi:
    def __init__(self):

        # Set up player1
        self.player_1_sprite = Player("assets/yellowPlayer.png", (screen_width / 4, screen_height / 2),
                                      screen_width / 2 - 10,
                                      screen_height, 5, 1)
        self.player1 = pygame.sprite.GroupSingle(self.player_1_sprite)
        self.health_p1 = 10

        # Set up player2
        self.player_2_sprite = Player("assets/redPlayer.png", (3 * screen_width / 4, screen_height / 2), screen_width,
                                      screen_height, 5, 2)
        self.player2 = pygame.sprite.GroupSingle(self.player_2_sprite)
        self.health_p2 = 10

        # Set up health

        # Set up the asteroids
        self.asteroids = pygame.sprite.Group()
        self.a_spawn = True
        self.a_spawn_delay = 3000
        self.a_spawn_time = 0

        # Kill animations
        self.boom = pygame.sprite.Group()

        self.start_delay = True

    # Checks if the bullet collides with a player
    def collision_checks(self):
        # Check for player 1 bullets
        if self.player1.sprite.yellow_bullets:
            for bullet in self.player1.sprite.yellow_bullets:
                # After a collision with a player, delete the bullet
                if pygame.sprite.spritecollide(bullet, self.player2, False):
                    bullet.kill()
                    self.health_p2 -= 1
                    pygame.mixer.Sound.play(hit_sound)

        # Check for player 2 bullets
        if self.player2.sprite.red_bullets:
            for bullet in self.player2.sprite.red_bullets:
                # After a collision with a player, delete the bullet
                if pygame.sprite.spritecollide(bullet, self.player1, False):
                    bullet.kill()
                    self.health_p1 -= 1
                    pygame.mixer.Sound.play(hit_sound)

        # Check if asteroid hits player
        if self.asteroids:
            for asteroid in self.asteroids:
                # After a collision with the player, delete asteroid and register hit
                if pygame.sprite.spritecollide(asteroid, self.player1, False):
                    asteroid.kill()
                    die_sprite = Boom(asteroid.rect.center, "assets/asteroid_broken.png", asteroid.angle)
                    self.boom.add(die_sprite)
                    self.health_p1 -= 1
                    pygame.mixer.Sound.play(hit_sound)
                if pygame.sprite.spritecollide(asteroid, self.player2, False):
                    asteroid.kill()
                    die_sprite = Boom(asteroid.rect.center, "assets/asteroid_broken.png", asteroid.angle)
                    self.boom.add(die_sprite)
                    self.health_p2 -= 1
                    pygame.mixer.Sound.play(hit_sound)

    # Asteroid spawns
    def asteroid_spawn(self):
        if self.a_spawn is True:
            asteroid_sprite = Asteroid(random.randint(75, screen_width / 2 - 75), -50, 3, random.choice([-1, 1]),
                                       random.choice([-1, 1]))
            self.asteroids.add(asteroid_sprite)
            asteroid_sprite = Asteroid(random.randint(screen_width / 2 + 75, screen_width - 75), -50, 3,
                                       random.choice([-1, 1]), random.choice([-1, 1]))
            self.asteroids.add(asteroid_sprite)
            self.a_spawn_time = pygame.time.get_ticks()
            self.a_spawn = False

    # Timer for asteroid spawns
    def respawn_timer(self):
        if not self.a_spawn:
            a_current_time = pygame.time.get_ticks()
            if a_current_time - self.a_spawn_time >= self.a_spawn_delay:
                self.a_spawn = True

    # Display health
    def show_health(self):
        if self.health_p1 > 0:
            p1health = pygame.image.load(
                "assets/yellowHeart/yellowHeart" + str(self.health_p1) + ".png").convert_alpha()
            p1health_rect = p1health.get_rect(topleft=screen.get_rect().topleft)
            screen.blit(p1health, p1health_rect)
        if self.health_p2 > 0:
            p2health = pygame.image.load("assets/redHeart/redHeart" + str(self.health_p2) + ".png").convert_alpha()
            p2health_rect = p2health.get_rect(topright=screen.get_rect().topright)
            screen.blit(p2health, p2health_rect)

    def run(self):
        self.player1.sprite.yellow_bullets.draw(screen)
        self.player1.update()
        self.player1.draw(screen)
        self.player2.draw(screen)
        self.player2.sprite.red_bullets.draw(screen)
        self.player2.update()
        self.asteroids.draw(screen)
        self.asteroids.update()
        self.boom.draw(screen)
        self.boom.update()
        if not self.start_delay:
            self.asteroid_spawn()
        self.respawn_timer()
        self.collision_checks()
        self.show_health()


# Sets up the scrolling background
class Background:
    def __init__(self):
        self.bgimage = pygame.image.load('assets/bg.png')
        self.rectBGimg = self.bgimage.get_rect()

        self.bgY1 = -self.rectBGimg.height
        self.bgX1 = 0

        self.bgY2 = 0
        self.bgX2 = 0

        self.moving_speed = -2

    def update(self):
        self.bgY1 -= self.moving_speed
        self.bgY2 -= self.moving_speed
        if self.bgY1 >= self.rectBGimg.height:
            self.bgY1 = -self.rectBGimg.height
        if self.bgY2 >= self.rectBGimg.height:
            self.bgY2 = -self.rectBGimg.height

    def render(self):
        screen.blit(self.bgimage, (self.bgX1, self.bgY1))
        screen.blit(self.bgimage, (self.bgX2, self.bgY2))


class Menu:
    def __init__(self):
        self.mid_h = screen_height / 2
        self.mid_w = screen_width / 2
        self.cursor_rect = pygame.Rect(0, 0, 0, 0)
        self.cursor_x = 320

    def draw_cursor(self):
        draw_text('>', 15, self.cursor_rect.x, WHITE, self.cursor_rect.y)


class MainMenu(Menu):
    def __init__(self):
        Menu.__init__(self)
        self.state = "Singleplayer"
        self.singleplayery = self.mid_h + 30
        self.multiplayery = self.mid_h + 55
        self.leaderboardy = self.mid_h + 80
        self.optionsy = self.mid_h + 105
        self.creditsy = self.mid_h + 130
        self.quity = self.mid_h + 155

        self.cursor_rect.midtop = (self.singleplayery, self.cursor_x)

    def display_menu(self):
        screen.fill(BLACK)
        bg.update()
        bg.render()
        draw_text('Gravity Blasters', 50, screen_height / 2 - 40)
        draw_text("Singleplayer", 20, self.singleplayery)
        draw_text("Multiplayer", 20, self.multiplayery)
        draw_text("Leaderboards", 20, self.leaderboardy)
        draw_text("Options", 20, self.optionsy)
        draw_text("Credits", 20, self.creditsy)
        draw_text("Quit", 20, self.quity)

        self.draw_cursor()
        blit_screen()


class Leaderboard(Menu):
    def __init__(self):
        Menu.__init__(self)

    def display_menu(self):
        screen.fill(BLACK)
        bg.update()
        bg.render()
        f = open('highscores.txt', 'r')  # opens the file in read mode
        data = f.readlines()  # reads all the lines in as a list
        currentTop = int(data[0])  # gets the first line of the file
        second = int(data[1])
        third = int(data[2])
        fourth = int(data[3])
        fifth = int(data[4])
        f.close()

        draw_text('Leaderboard', 30, screen_height / 2 - 20)
        draw_text('Top Scores:', 20, screen_height / 2 + 10)
        draw_text("#1" + "........" + str(currentTop), 30,
                  screen_height / 2 + 45)
        draw_text("#2" + "........." + str(second), 28,
                  screen_height / 2 + 65)
        draw_text("#3" + "........." + str(third), 26,
                  screen_height / 2 + 85)
        draw_text("#4" + "........." + str(fourth), 24,
                  screen_height / 2 + 105)
        draw_text("#5" + "........." + str(fifth), 22,
                  screen_height / 2 + 125)

        blit_screen()


class OptionsMenu(Menu):
    def __init__(self):
        Menu.__init__(self)

    def display_menu(self):
        screen.fill(BLACK)
        bg.update()
        bg.render()
        draw_text('Options', 25, self.mid_h - 30, WHITE, self.mid_w - 10)
        draw_text("Controls", 20, self.mid_h + 20, WHITE, self.mid_w - 10)
        draw_text('>', 15, self.mid_h + 20, WHITE, self.mid_w - 60)
        self.draw_cursor()
        blit_screen()


class ControlsMenu(Menu):
    def __init__(self):
        Menu.__init__(self)

    def display_menu(self):
        screen.fill(BLACK)
        bg.update()
        bg.render()
        p1ctrls = pygame.image.load('assets/p1controls.png')
        p2ctrls = pygame.image.load('assets/p2controls.png')
        DEFAULT_IMAGE_SIZE = (110, 140)
        DEFAULT_IMAGE_SIZE2 = (170, 170)
        p1ctrlfinal = pygame.transform.scale(p1ctrls, DEFAULT_IMAGE_SIZE)
        p2ctrlfinal = pygame.transform.scale(p2ctrls, DEFAULT_IMAGE_SIZE2)
        draw_text("Controls", 30, screen_height / 2 - 25)
        draw_text('Player 1 ', 25, self.mid_h + 10, WHITE, self.mid_w - 150)
        draw_text("Player 2", 25, self.mid_h + 10, WHITE, self.mid_w + 150)
        screen.blit(p2ctrlfinal, (self.mid_w - 230, self.mid_h + 10))
        screen.blit(p1ctrlfinal, (self.mid_w + 90, self.mid_h + 24))
        blit_screen()


class CreditsMenu(Menu):
    def __init__(self):
        Menu.__init__(self)

    def display_menu(self):
        screen.fill(BLACK)
        bg.update()
        bg.render()
        draw_text('Credits', 40, screen_height / 2 - 20)
        draw_text('Made by Phil,  Luis,  Rutva,  and Yessenia', 30,
                  screen_height / 2 + 10)
        blit_screen()


def readTopScore():
    f = open('highscores.txt', 'r')  # opens the file in read mode
    data = f.readlines()  # reads all the lines in as a list
    currentTop = int(data[0])  # gets the first line of the file
    f.close()
    return currentTop


def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()


def updateFile():
    f = open('highscores.txt', 'r')  # opens the file in read mode
    data = f.readlines()  # reads all the lines in as a list
    currentTop = int(data[0])  # gets the first line of the file
    second = int(data[1])
    third = int(data[2])
    fourth = int(data[3])
    fifth = int(data[4])
    f.close()

    if currentTop < game.score_value:
        # sees if the current score is greater than the previous best
        replace_line('highscores.txt', 0, str(game.score_value) + '\n')
        replace_line('highscores.txt', 1, str(currentTop) + '\n')
        replace_line('highscores.txt', 2, str(second) + '\n')
        replace_line('highscores.txt', 3, str(third) + '\n')
        replace_line('highscores.txt', 4, str(fourth) + '\n')

    elif second < game.score_value < currentTop:
        # sees if the current score is greater than the previous best
        replace_line('highscores.txt', 1, str(game.score_value) + '\n')
        replace_line('highscores.txt', 2, str(second) + '\n')
        replace_line('highscores.txt', 3, str(third) + '\n')
        replace_line('highscores.txt', 4, str(fourth) + '\n')

    elif third < game.score_value < second:
        # sees if the current score is greater than the previous best
        replace_line('highscores.txt', 2, str(game.score_value) + '\n')
        replace_line('highscores.txt', 3, str(third) + '\n')
        replace_line('highscores.txt', 4, str(fourth) + '\n')

    elif fourth < game.score_value < third:
        # sees if the current score is greater than the previous best
        replace_line('highscores.txt', 3, str(game.score_value) + '\n')
        replace_line('highscores.txt', 4, str(fourth) + '\n')

    elif fifth < game.score_value < fourth:
        # sees if the current score is greater than the previous best
        replace_line('highscores.txt', 4, str(game.score_value) + '\n')

    return currentTop


# Draw text on the screen
# If there are no variables to pass and you want the text centered, pass the height only
# Y POSITION GOES FIRST!!
def draw_text(content, size, posy, color=(255, 255, 255), posx=0.0):
    font = pygame.font.Font('assets/Eight-Bit Madness.ttf', size)
    text = font.render(content, True, color)
    # If there is no x value given
    if posx != 0.0:
        text_rect = text.get_rect(center=(posx, posy))
    # If there is an x value given
    else:
        text_rect = text.get_rect(center=(screen_width / 2, posy))
    screen.blit(text, text_rect)


def blit_screen():
    screen.blit(screen, (0, 0))
    pygame.display.flip()


if __name__ == '__main__':
    # Initialize pygame
    pygame.init()

    # create the screen
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Create colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    RED = (255, 20, 20)

    # Create the variables for the game clock/timer
    clock = pygame.time.Clock()
    counter = 0
    time_delay = 1000
    TIMER_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMER_EVENT, time_delay)
    FPS = 60

    FLASH_EVENT = pygame.USEREVENT + 3
    pygame.time.set_timer(FLASH_EVENT, 175)

    # Create key input variable
    keys = pygame.key.get_pressed()
    input_rect = pygame.Rect(200, 200, 140, 64)
    user_text = ''

    # Make sure the game will run
    running = True

    p1_ready = False
    p2_ready = False

    # Create game objects
    game = Game()
    multi = Multi()
    bg = Background()
    main_menu = MainMenu()
    leaderboard = Leaderboard()
    credits_menu = CreditsMenu()
    options_menu = OptionsMenu()
    control_menu = ControlsMenu()

    # Set up the music
    play_music = True

    # Font for timer
    font = pygame.font.Font('assets/Eight-Bit Madness.ttf', 64)
    timer_text = font.render(str(counter), True, WHITE)

    # Event for enemy shooting
    ENEMY_BULLET = pygame.USEREVENT + 2
    pygame.time.set_timer(ENEMY_BULLET, 750)

    # set HighScore
    topscore = int(readTopScore())
    # Images
    pygame.display.set_caption("Gravity Blasters")
    icon = pygame.image.load('assets/planet.png')
    pygame.display.set_icon(icon)
    explosion = pygame.image.load("assets/explosion.png").convert_alpha()

    # Initial state for the game
    state = 'menu'
    mode = ''
    reset = True

    # Game Loop
    while running:

        # Menu state
        if state == 'menu':
            # Show main menu options
            main_menu.display_menu()
            volume_sfx()
            mode = 'singlePlayer'
            if play_music:
                pygame.mixer.music.load("assets/Idle Theme.wav")
                pygame.mixer.music.set_volume(volume_music)
                pygame.mixer.music.play(-1)
            play_music = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Check for player input at the main menu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        pygame.mixer.Sound.play(menu_move_down)
                        if main_menu.state == 'Singleplayer':
                            main_menu.cursor_rect.midtop = (
                                main_menu.multiplayery, main_menu.cursor_x)
                            main_menu.state = 'Multiplayer'
                        elif main_menu.state == 'Multiplayer':
                            main_menu.cursor_rect.midtop = (
                                main_menu.leaderboardy, main_menu.cursor_x)
                            main_menu.state = 'Leaderboards'
                        elif main_menu.state == 'Leaderboards':
                            main_menu.cursor_rect.midtop = (main_menu.optionsy, main_menu.cursor_x)
                            main_menu.state = 'Options'
                        elif main_menu.state == 'Options':
                            main_menu.cursor_rect.midtop = (main_menu.creditsy, main_menu.cursor_x)
                            main_menu.state = 'Credits'
                        elif main_menu.state == 'Credits':
                            main_menu.cursor_rect.midtop = (
                                main_menu.quity, main_menu.cursor_x)
                            main_menu.state = 'Quit'
                        elif main_menu.state == 'Quit':
                            main_menu.cursor_rect.midtop = (
                                main_menu.singleplayery, main_menu.cursor_x)
                            main_menu.state = 'Singleplayer'
                    elif event.key == pygame.K_UP:
                        pygame.mixer.Sound.play(menu_move_up)
                        if main_menu.state == 'Singleplayer':
                            main_menu.cursor_rect.midtop = (main_menu.quity, main_menu.cursor_x)
                            main_menu.state = 'Quit'
                        elif main_menu.state == 'Multiplayer':
                            main_menu.cursor_rect.midtop = (
                                main_menu.singleplayery, main_menu.cursor_x)
                            main_menu.state = 'Singleplayer'
                        elif main_menu.state == 'Leaderboards':
                            main_menu.cursor_rect.midtop = (
                                main_menu.multiplayery, main_menu.cursor_x)
                            main_menu.state = 'Multiplayer'
                        elif main_menu.state == 'Options':
                            main_menu.cursor_rect.midtop = (
                                main_menu.leaderboardy, main_menu.cursor_x)
                            main_menu.state = 'Leaderboards'
                        elif main_menu.state == 'Credits':
                            main_menu.cursor_rect.midtop = (main_menu.optionsy, main_menu.cursor_x)
                            main_menu.state = 'Options'
                        elif main_menu.state == 'Quit':
                            main_menu.cursor_rect.midtop = (main_menu.creditsy, main_menu.cursor_x)
                            main_menu.state = 'Credits'
                    elif event.key == pygame.K_SPACE:
                        pygame.mixer.Sound.play(menu_select)
                        if main_menu.state == 'Singleplayer':
                            state = 'countdown'
                            reset = True
                            play_music = True
                        elif main_menu.state == 'Multiplayer':
                            state = 'multiReady'
                            reset = True
                            play_music = True
                        elif main_menu.state == 'Leaderboards':
                            state = 'leaderboard'
                        elif main_menu.state == 'Options':
                            state = 'options'
                        elif main_menu.state == 'Credits':
                            state = 'credits'
                        elif main_menu.state == 'Quit':
                            pygame.quit()
                            sys.exit()

        if state == 'leaderboard':
            leaderboard.display_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Check for player input at the leaderboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = 'menu'
                    if event.key == pygame.K_SPACE:
                        state = 'menu'

        if state == 'options':
            options_menu.display_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = 'menu'
                    if event.key == pygame.K_SPACE:
                        state = 'controls'
                    if event.key == pygame.K_KP_ENTER:
                        state = 'controls'

        if state == 'controls':
            control_menu.display_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = 'options'
                    if event.key == pygame.K_SPACE:
                        state = 'options'

        if state == 'credits':
            credits_menu.display_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Check for player input at the leaderboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = 'menu'
                    if event.key == pygame.K_SPACE:
                        state = 'menu'

        if state == 'countdown':
            screen.fill(BLACK)
            for event in pygame.event.get():
                if event.type == TIMER_EVENT:
                    counter += 1
                    if counter == 1:
                        draw_text("3", 80, screen_height / 2)
                        pygame.mixer.Sound.play(count_sound)
                    if counter == 2:
                        draw_text("2", 80, screen_height / 2)
                        pygame.mixer.Sound.play(count_sound)
                    if counter == 3:
                        draw_text("1", 80, screen_height / 2)
                        pygame.mixer.Sound.play(count_sound)
                    if counter == 4:
                        draw_text("Go!", 80, screen_height / 2)
                        pygame.mixer.Sound.play(go_sound)
                    if counter == 5:
                        pygame.mixer.music.stop()
                        counter = 0
                        state = mode

                    pygame.display.flip()

        if state == 'singlePlayer':
            # Re-initialize all variables on game start
            if reset:
                screen.fill(BLACK)
                counter = 0
                game.score_value = 0
                game.health = 3
                timer_text = font.render('0', True, WHITE)
                game.enemies.empty()
                game.enemy_bullets.empty()
                game.asteroids.empty()
                game.boom.empty()
                game.player_sprite.bullets.empty()
                game.player_sprite.rect.x = screen_width / 2
                game.start_delay = True
                pygame.time.set_timer(ENEMY_BULLET, 750)
                play_music = True
            reset = False
            if counter == 30:
                pygame.time.set_timer(ENEMY_BULLET, 600)
            if counter == 50:
                pygame.time.set_timer(ENEMY_BULLET, 400)
            if counter == 90:
                pygame.time.set_timer(ENEMY_BULLET, 250)
            if counter >= 1:
                game.start_delay = False
            if play_music:
                pygame.mixer.music.load("assets/Battle Theme.wav")
                pygame.mixer.music.set_volume(volume_music + 0.3)
                pygame.mixer.music.play(-1)
            play_music = False
            bg.update()
            bg.render()
            timer_text_rect = timer_text.get_rect(midtop=screen.get_rect().midtop)
            screen.blit(timer_text, timer_text_rect)
            game.run()
            if game.health <= 0:
                state = 'gameOver'
                user_text = ''
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(death_sound)
            pygame.display.flip()
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = 'pause'
                        pygame.mixer.music.pause()
                        pygame.mixer.Sound.play(pause_sound)
                if event.type == ENEMY_BULLET:
                    game.enemy_shoot()
                if event.type == TIMER_EVENT:
                    counter += 1
                    timer_text = font.render(str(counter), True, WHITE)
                if event.type == FLASH_EVENT and game.iframe:
                    if game.flash:
                        game.player_sprite.image.set_alpha(0)
                        game.flash = False
                    else:
                        game.player_sprite.image.set_alpha(255)
                        game.flash = True

        if state == 'multiReady':
            screen.fill(BLACK)
            bg.update()
            bg.render()
            draw_text('Ready?', 60, screen_height / 2 - 200)
            draw_text("Player 1", 40, screen_height / 2 - 50, WHITE, screen_width / 2 - 200)
            draw_text("press Left Shift", 40, screen_height / 2 - 20, WHITE, screen_width / 2 - 200)
            draw_text("Player 2", 40, screen_height / 2 - 50, WHITE, screen_width / 2 + 200)
            draw_text("press Right Shift", 40, screen_height / 2 - 20, WHITE, screen_width / 2 + 200)
            mode = 'multiPlayer'
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT:
                        p1_ready = True
                        pygame.mixer.Sound.play(ready_sound)
                    if event.key == pygame.K_RSHIFT:
                        p2_ready = True
                        pygame.mixer.Sound.play(ready_sound)
                    if event.key == pygame.K_ESCAPE:
                        state = 'menu'
                        p1_ready = False
                        p2_ready = False

            if p1_ready is True:
                draw_text('Ready!', 40, screen_height / 2 + 10, YELLOW, screen_width / 2 - 200)

            if p2_ready is True:
                draw_text('Ready!', 40, screen_height / 2 + 10, RED, screen_width / 2 + 200)

            if p1_ready is True and p2_ready is True:
                state = 'countdown'
                p1_ready = False
                p2_ready = False
            pygame.display.flip()

        if state == 'multiPlayer':
            if reset:
                screen.fill(BLACK)
                counter = 0
                multi.start_delay = True
                multi.health_p1 = 10
                multi.health_p2 = 10
                timer_text = font.render('0', True, WHITE)
                multi.asteroids.empty()
                multi.boom.empty()
                multi.player_1_sprite.yellow_bullets.empty()
                multi.player_2_sprite.red_bullets.empty()
                multi.player_1_sprite.rect.x = screen_width / 4
                multi.player_1_sprite.rect.y = screen_height / 2
                multi.player_2_sprite.rect.x = 3 * screen_width / 4
                multi.player_2_sprite.rect.y = screen_height / 2
                play_music = True
            reset = False
            if play_music:
                pygame.mixer.music.load("assets/Battle Theme.wav")
                pygame.mixer.music.set_volume(volume_music + 0.3)
                pygame.mixer.music.play(-1)
            play_music = False
            bg.update()
            bg.render()
            timer_text_rect = timer_text.get_rect(midtop=screen.get_rect().midtop)
            screen.blit(timer_text, timer_text_rect)
            multi.run()
            if counter >= 1:
                multi.start_delay = False
            if multi.health_p2 == 0 or multi.health_p1 == 0:
                state = 'winner'
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(death_sound)
            pygame.display.flip()
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = 'pause'
                        pygame.mixer.music.pause()
                        pygame.mixer.Sound.play(pause_sound)
                if event.type == TIMER_EVENT:
                    counter += 1
                    timer_text = font.render(str(counter), True, WHITE)

        if state == 'pause':
            # Show paused message
            draw_text("Paused", 64, (screen_height / 2) - 40)
            draw_text("Press space to resume", 40, (screen_height / 2))
            draw_text("Press escape to return to main menu", 40, (screen_height / 2) + 35)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        state = mode
                        pygame.mixer.music.unpause()
                        pygame.mixer.Sound.play(unpause_sound)
                    if event.key == pygame.K_ESCAPE:
                        state = 'menu'
                        counter = 0
                        play_music = True

        # Show game over message
        if state == 'gameOver':
            if game.score_value > topscore:
                draw_text("Game Over!", 60, (screen_height / 2) - 40, WHITE, screen_width / 2)
                draw_text("New HighScore: " + str(game.score_value), 64, (screen_height / 2) + 25, WHITE,
                          screen_width / 2)
                draw_text("Press esc to return to menu", 40, (screen_height / 2) + 60)
                updateFile()
                topscore = game.score_value
            if game.score_value < topscore:
                draw_text("Game Over!", 64, (screen_height / 2) - 40, WHITE, screen_width / 2)
                draw_text("Your Score: " + str(game.score_value), 60, (screen_height / 2) + 25, WHITE, screen_width / 2)
                draw_text("Press esc to return to menu", 40, (screen_height / 2) + 60)
                updateFile()
            pygame.display.flip()
            screen.blit(explosion, game.player_sprite.rect.topleft)
            play_music = True
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = 'menu'
                        counter = 0
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        if state == 'winner':
            if multi.health_p2 == 0:
                draw_text("Yellow wins!", 64, (screen_height / 2) - 40, YELLOW,
                          screen_width / 2)
                screen.blit(explosion, multi.player_2_sprite.rect.topleft)
            else:
                draw_text("Red wins!", 64, (screen_height / 2) - 40, RED, screen_width / 2)
                screen.blit(explosion, multi.player_1_sprite.rect.topleft)
            draw_text("Press space to play again", 40, (screen_height / 2))
            draw_text("Press esc to return to menu", 40, (screen_height / 2) + 35)
            play_music = True
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        reset = True
                        state = 'countdown'
                        counter = 0
                    if event.key == pygame.K_ESCAPE:
                        state = 'menu'
                        counter = 0
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
