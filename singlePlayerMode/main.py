import pygame
import sys
from random import choice
import random

from models import Player, EasyEnemy, MediumEnemy, HardEnemy, EnemyBullet


class Game:
    # Initialize the game
    def __init__(self):
        # Set up the player
        player_sprite = Player((screen_width / 2, screen_height - 50), screen_width, 5)
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
        self.health_x_start_pos = screen_width - (self.health_surface.get_size()[0] * 3 + 620)

        # Set up the three rows
        self.toprow = screen_height - 560
        self.midrow = screen_height - 500
        self.botrow = screen_height - 440

        # Declare the explosion sound effect
        self.explode_sound = pygame.mixer.Sound("explosion.wav")
        self.explode_sound.set_volume(0.3)

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

    # Enemy shoot
    def enemy_shoot(self):
        if self.enemies.sprites():
            random_enemy = choice(self.enemies.sprites())
            enemy_bullet_sprite = EnemyBullet(random_enemy.rect.center, 6, screen_height)
            self.enemy_bullets.add(enemy_bullet_sprite)

    # Display the score
    def show_score(self):
        score = font.render("Score: " + str(self.score_value), True, (255, 255, 255))
        screen.blit(score, (0, 0))

    # Display player health
    def show_health(self):
        for heart in range(self.health):
            x = self.health_x_start_pos + (heart * self.health_surface.get_size()[0] + 10)
            screen.blit(self.health_surface, (x, screen_height - 60))

    # Show game over screen
    def show_game_over(self):
        game_over_message = font.render("GAME OVER score: " + str(self.score_value), True, (255, 255, 255))
        screen.blit(game_over_message, (screen_width / 2, screen_height / 4))

        waiting = True
        while waiting:
            clock.tick(60)
            for game.event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.K_SPACE:
                    waiting = False

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
        self.enemy_spawn()
        self.respawn_timer()


if __name__ == '__main__':
    # Initialize pygame
    pygame.init()

    # create the screen
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))

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

    # Create game object
    game = Game()

    # Font for timer
    font = pygame.font.Font('Eight-Bit Madness.ttf', 64)
    timer_text = font.render(str(counter), True, (255, 255, 255))
    menu_text = font.render("Press space to start", True, (255, 255, 255))



    # Event for enemy shooting
    ENEMY_BULLET = pygame.USEREVENT + 1
    pygame.time.set_timer(ENEMY_BULLET, 750)

    # Play the music
    #pygame.mixer.music.load("Battle Theme.wav")
    #pygame.mixer.music.play(-1)

    # Caption and Icon
    pygame.display.set_caption("Space Warriors")
    icon = pygame.image.load('logo.png')
    pygame.display.set_icon(icon)

    # Initial state for the game
    state = 'menu'

    # Game Loop
    while running:

        # Menu state
        if state == 'menu':
            # Show some text
            menu_text_rect = menu_text.get_rect(center=screen.get_rect().center)
            screen.blit(menu_text, menu_text_rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Check for player input to start the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        state = 'singlePlayer'

        if state == 'gameOver':
            # Show game over
            game_over_text = font.render("Game Over! Score: " + str(game.score_value), True, (255, 255, 255))
            game_over_text_rect = game_over_text.get_rect(center=screen.get_rect().center)
            screen.blit(game_over_text, game_over_text_rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        if state == 'singlePlayer':
            # RGB = Red, Green, Blue
            screen.fill((0, 0, 0))
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
                    timer_text = font.render(str(counter), True, (255, 255, 255))


