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

    # Sets up the enemies
    def enemy_spawn(self):
        difficulty = 0
        if counter <= 15 and self.spawn is True:
            easy_enemy_sprite = EasyEnemy(random.randint(10, screen_width - 10), screen_height - 440, 3, screen_width)
            self.enemies.add(easy_enemy_sprite)
            self.spawn_time = pygame.time.get_ticks()
            self.spawn = False
        elif 45 >= counter > 15 and self.spawn is True:
            medium_enemy_sprite = MediumEnemy(random.randint(10, screen_width - 10), screen_height - 500, 4, screen_width)
            self.enemies.add(medium_enemy_sprite)
            self.spawn_time = pygame.time.get_ticks()
            self.spawn = False
            self.spawn_delay = 1400
        elif counter > 45 and self.spawn is True:
            hard_enemy_sprite = HardEnemy(random.randint(10, screen_width - 10), screen_height - 560, 5, screen_width)
            self.enemies.add(hard_enemy_sprite)
            self.spawn_time = pygame.time.get_ticks()
            self.spawn = False
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
                    self.score_value += 1

        # Check for enemy bullets
        if self.enemy_bullets:
            for bullet in self.enemy_bullets:
                # After a collision with the player, delete the bullet and register hit
                if pygame.sprite.spritecollide(bullet, self.player, False):
                    bullet.kill()
                    print('hit')

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

    # Method that runs the game
    def run(self):
        self.player.sprite.bullets.draw(screen)
        # self.enemies.sprite.bullets.draw(screen)
        self.player.update()
        self.player.draw(screen)
        self.enemies.draw(screen)
        self.enemy_bullets.update()
        self.enemy_bullets.draw(screen)
        self.collision_checks()
        self.enemies.update()
        self.show_score()
        self.enemy_spawn()
        self.respawn_timer()


if __name__ == '__main__':
    # Initialize the pygame
    pygame.init()

    # create the screen
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    # Create the variables for the game clock/timer
    clock = pygame.time.Clock()
    counter = 0
    time_delay = 1000
    TIMER_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMER_EVENT, time_delay)

    # Create the game class
    game = Game()

    # Font for timer
    font = pygame.font.Font('Eight-Bit Madness.ttf', 64)
    timer_text = font.render(str(counter), True, (255, 255, 255))

    # Event for enemy shooting
    ENEMY_BULLET = pygame.USEREVENT + 1
    pygame.time.set_timer(ENEMY_BULLET, 800)

    # Caption and Icon
    pygame.display.set_caption("Space Warriors")
    icon = pygame.image.load('logo.png')
    pygame.display.set_icon(icon)

    # Game Loop
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ENEMY_BULLET:
                game.enemy_shoot()
            if event.type == TIMER_EVENT:
                counter += 1
                timer_text = font.render(str(counter), True, (255, 255, 255))

        # RGB = Red, Green, Blue
        screen.fill((0, 0, 0))
        timer_text_rect = timer_text.get_rect(midtop=screen.get_rect().midtop)
        screen.blit(timer_text, timer_text_rect)
        game.run()

        pygame.display.flip()
        clock.tick(60)
