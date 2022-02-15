import pygame

import sys

from models import Player, Enemy

class Game:
   # Initialize the game
   def __init__(self):
       # Set up the player
       player_sprite = Player((screen_width / 2, screen_height - 50), screen_width, 5)
       self.player = pygame.sprite.GroupSingle(player_sprite)

       # Set up the enemies
       self.enemies = pygame.sprite.Group()
       self.enemy_setup(rows=1, cols=1)

   # Sets up the enemies in case we are doing a grid like format
   # WIP
   def enemy_setup(self, rows, cols):
       for row_index, row in enumerate(range(rows)):
           for col_index, col in enumerate(range(cols)):
               x = col_index
               y = row_index
               enemy_sprite = Enemy('red', screen_width / 2, screen_height - 500)
               self.enemies.add(enemy_sprite)

   def collision_checks(self):
       # Check for player bullets
       if self.player.sprite.bullets:
           for bullet in self.player.sprite.bullets:
               # After a collision with an enemy, delete the bullet
               if pygame.sprite.spritecollide(bullet, self.enemies, True):
                   bullet.kill()

   # Method that runs the game
   def run(self):
       self.player.sprite.bullets.draw(screen)
       self.player.update()
       self.player.draw(screen)
       self.enemies.draw(screen)
       self.collision_checks()


if __name__ == '__main__':
   # Initialize the pygame
   pygame.init()

   # create the screen
   screen_width = 800
   screen_height = 600
   screen = pygame.display.set_mode((screen_width, screen_height))

   # Create the game clock
   clock = pygame.time.Clock()

   game = Game()

   # Caption and Icon
   pygame.display.set_caption("Space Warriors")
   icon = pygame.image.load('logo.png')
   pygame.display.set_icon(icon)

   # Game Loop

   while True:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()


       # RGB = Red, Green, Blue
       screen.fill((0, 0, 0))
       game.run()

       pygame.display.flip()
       clock.tick(60)