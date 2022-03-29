import pygame
import sys
from random import choice
import random

from models import Player, EasyEnemy, MediumEnemy, HardEnemy, EnemyBullet


class Game:
    # Initialize the game
    def __init__(self):

        # Set up the player
        self.player_sprite = Player((screen_width / 2, screen_height - 50), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(self.player_sprite)
        self.initial = ''
        self.hs = 0

        # Set up the enemies
        self.enemies = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.score_value = 0
        self.spawn = True
        self.spawn_delay = 1800
        self.spawn_time = 0
        self.enemy_max = 0
        self.start_delay = True

        # Set up the player health
        self.health = 3
        self.health_surface = pygame.image.load("assets/heart.png").convert_alpha()
        self.health_x_start_pos = screen_width - (self.health_surface.get_size()[0] * 3 + 620)

        # Set up the three rows
        self.toprow = screen_height - 560
        self.midrow = screen_height - 500
        self.botrow = screen_height - 440

        # Declare the sound effects
        self.explode_sound = pygame.mixer.Sound("assets/explosion.wav")
        self.hit_sound = pygame.mixer.Sound("assets/hit.mp3")

    # Sets the volume for the sounds effects
    def volume_sfx(self, level=0.3):
        self.explode_sound.set_volume(level)
        self.hit_sound.set_volume(level)
        self.player_sprite.shoot_sound.set_volume(level)

    # Sets the volume for the music
    def volume_music(self, level=0.3):
        pass

    # Sets up the enemies
    def enemy_spawn(self):
        # The first level of difficulty: spawns in only easy enemies
        if counter <= 15 and self.spawn is True and self.enemy_max < 20:
            easy_enemy_sprite = EasyEnemy(random.randint(10, screen_width - 10),
                                          random.choice([self.toprow, self.midrow, self.botrow]), 3, screen_width)
            self.enemies.add(easy_enemy_sprite)
            self.spawn_time = pygame.time.get_ticks()
            self.spawn = False
            self.enemy_max += 1
        # The second level of difficulty: spawns in easy and medium enemies at a slightly faster pace
        elif 45 >= counter > 15 and self.spawn is True and self.enemy_max < 20:
            easy_enemy_sprite = EasyEnemy(random.randint(10, screen_width - 10),
                                          random.choice([self.toprow, self.midrow, self.botrow]), 3, screen_width)
            medium_enemy_sprite = MediumEnemy(random.randint(10, screen_width - 10),
                                              random.choice([self.toprow, self.midrow, self.botrow]), 4, screen_width)
            self.enemies.add(random.choice([medium_enemy_sprite, easy_enemy_sprite]))
            self.spawn_time = pygame.time.get_ticks()
            self.spawn = False
            self.enemy_max += 1
            self.spawn_delay = 1400
        # The final lever of difficulty: spawns in easy, medium, and hard enemies at a rapid pace
        elif counter > 45 and self.spawn is True and self.enemy_max < 20:
            easy_enemy_sprite = EasyEnemy(random.randint(10, screen_width - 10),
                                          random.choice([self.toprow, self.midrow, self.botrow]), 3, screen_width)
            medium_enemy_sprite = MediumEnemy(random.randint(10, screen_width - 10),
                                              random.choice([self.toprow, self.midrow, self.botrow]), 4, screen_width)
            hard_enemy_sprite = HardEnemy(random.randint(10, screen_width - 10),
                                          random.choice([self.toprow, self.midrow, self.botrow]), 5, screen_width)
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
                    pygame.mixer.Sound.play(self.hit_sound)

    # Enemy shoot
    def enemy_shoot(self):
        if self.enemies.sprites():
            random_enemy = choice(self.enemies.sprites())
            enemy_bullet_sprite = EnemyBullet(random_enemy.rect.center, 6, screen_height)
            self.enemy_bullets.add(enemy_bullet_sprite)

    # Display the score
    def show_score(self):
        score = font.render("Score: " + str(self.score_value), True, WHITE)
        screen.blit(score, (0, 0))

    # Display player health
    def show_health(self):
        for heart in range(self.health):
            x = self.health_x_start_pos + (heart * self.health_surface.get_size()[0] + 10)
            screen.blit(self.health_surface, (x, screen_height - 60))

    # Method that runs the game
    def run(self):
        self.player.sprite.bullets.draw(screen)
        self.player.update()
        self.player.draw(screen)
        self.enemies.draw(screen)
        self.enemy_bullets.update()
        self.enemy_bullets.draw(screen)
        self.collision_checks()
        self.enemies.update()
        self.show_score()
        self.show_health()
        if not self.start_delay:
            self.enemy_spawn()
        self.respawn_timer()


# Sets up the scrolling background
class Background:
    def __init__(self):
        self.bgimage = pygame.image.load('assets/bg.png')
        self.rectBGimg = self.bgimage.get_rect()

        self.bgY1 = -self.rectBGimg.height
        self.bgX1 = 0

        self.bgY2 = 0
        self.bgX2 = 0

        self.moving_speed = -3

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
        self.cursor_rect = pygame.Rect(0, 0, 0, 0)
        self.cursor_x = 320

    def draw_cursor(self):
        draw_text('>', 15, self.cursor_rect.x, self.cursor_rect.y)


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
        draw_text('Leaderboard', 20, screen_height / 2 - 20)
        draw_text('Top Scores:', 15, screen_height / 2 + 10)
        draw_text(str(game.initial) + "........." + str(game.hs), 22,
                  screen_height / 2 + 45)
        blit_screen()


class CreditsMenu(Menu):
    def __init__(self):
        Menu.__init__(self)

    def display_menu(self):
        screen.fill(BLACK)
        draw_text('Credits', 20, screen_height / 2 - 20)
        draw_text('Made by Phil,  Luis,  Rutva,  and Yessenia', 15,
                  screen_height / 2 + 10)
        blit_screen()


# Draw text on the screen
# If there are no variables to pass and you want the text centered, pass the height only
def draw_text(content, size, posy, posx=0.0, value=''):
    font = pygame.font.Font('assets/Eight-Bit Madness.ttf', size)
    text = font.render(content, True, WHITE)
    # If there is no x value given
    if posx != 0.0 and value == '':
        text_rect = text.get_rect(center=(posx, posy))
    # If there is a value passed
    elif value != '':
        text = font.render(content + value, True, WHITE)
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
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Create colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Create the variables for the game clock/timer
    clock = pygame.time.Clock()
    counter = 0
    time_delay = 1000
    TIMER_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMER_EVENT, time_delay)

    # Create key input variable
    keys = pygame.key.get_pressed()

    # Make sure the game will run
    running = True

    # Create game objects
    game = Game()
    bg = Background()
    main_menu = MainMenu()
    leaderboard = Leaderboard()
    credits_menu = CreditsMenu()

    # Font for timer
    font = pygame.font.Font('assets/Eight-Bit Madness.ttf', 64)
    timer_text = font.render(str(counter), True, WHITE)

    # Event for enemy shooting
    ENEMY_BULLET = pygame.USEREVENT + 1
    pygame.time.set_timer(ENEMY_BULLET, 750)

    # Play the music
    # pygame.mixer.music.load("Battle Theme.wav")
    # pygame.mixer.music.play(-1)

    # Caption and Icon
    pygame.display.set_caption("Gravity Blasters")
    icon = pygame.image.load('assets/logo.png')
    pygame.display.set_icon(icon)

    # Initial state for the game
    state = 'menu'
    reset = True

    # Game Loop
    while running:

        # Menu state
        if state == 'menu':
            # Show main menu options
            main_menu.display_menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Check for player input at the main menu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
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
                        if main_menu.state == 'Singleplayer':
                            state = 'readySingle'
                            reset = True
                        elif main_menu.state == 'Multiplayer':
                            state = 'multiPlayer'
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

        if state == 'readySingle':
            screen.fill(BLACK)
            game.volume_sfx()
            for event in pygame.event.get():
                if event.type == TIMER_EVENT:
                    counter += 1
                    if counter == 1:
                        draw_text("3", 80, screen_height / 2)
                    if counter == 2:
                        draw_text("2", 80, screen_height / 2)
                    if counter == 3:
                        draw_text("1", 80, screen_height / 2)
                    if counter == 4:
                        draw_text("Go!", 80, screen_height / 2)
                    if counter == 5:
                        counter = 0
                        state = 'singlePlayer'
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
                game.player_sprite.bullets.empty()
                game.player_sprite.rect.x = screen_width / 2
                game.start_delay = True
            reset = False
            if counter >= 1:
                game.start_delay = False
            if game.player_sprite.pause:
                state = 'pause'
            bg.update()
            bg.render()
            timer_text_rect = timer_text.get_rect(midtop=screen.get_rect().midtop)
            screen.blit(timer_text, timer_text_rect)
            game.run()
            if game.health <= 0:
                state = 'gameOver'
            pygame.display.flip()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == ENEMY_BULLET:
                    game.enemy_shoot()
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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        state = 'singlePlayer'
                        game.player_sprite.pause = False
                    if event.key == pygame.K_ESCAPE:
                        state = 'menu'
                        game.player_sprite.pause = False
                        counter = 0

        # Show game over message
        if state == 'gameOver':
            # If score is not 0 print the value of the score
            if game.score_value != 0:
                draw_text("Game Over! Score: ", 64, (screen_height / 2) - 40, screen_width / 2, str(game.score_value))
            else:
                draw_text("Game Over! Score: 0", 64, (screen_height / 2) - 40)
            draw_text("Press space to play again", 40, (screen_height / 2))
            draw_text("Press esc to return to menu", 40, (screen_height / 2) + 35)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        reset = True
                        state = 'readySingle'
                        counter = 0
                    if event.key == pygame.K_ESCAPE:
                        state = 'menu'
                        counter = 0
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
