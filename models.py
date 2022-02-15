import pygame


# Class that handles the player attributes
class Player(pygame.sprite.Sprite):
    # Initializes the player
    def __init__(self, pos, constraint, speed):
        super().__init__()
        # Loads the player image file
        self.image = pygame.image.load("player.png").convert_alpha()

        # Gives the player a rectangle collider
        self.rect = self.image.get_rect(midbottom=pos)

        # How fast the player will move
        self.speed = speed

        # Defines the edge of the screen
        self.max_x_constraint = constraint

        # To check if bullet is ready to shoot
        self.ready = True

        # Sets the time when a bullet is shot
        self.shoot_time = 0

        # Timer to prevent infinite shooting
        self.cooldown = 600

        # Helps to create a new bullet sprite on each key press
        self.bullets = pygame.sprite.Group()

    # Gets player input
    def get_input(self):
        # Detect if a key is pressed
        keys = pygame.key.get_pressed()

        # Move the player left/right
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        # Shoot bullet only when cooldown is 0
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot()
            # Triggers the bullet cooldown
            self.ready = False
            self.shoot_time = pygame.time.get_ticks()

    # Handles the bullet recharge time
    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.cooldown:
                self.ready = True

    # Stops the player from leaving the screen
    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    # Method that handles shooting bullets by the player
    def shoot(self):
        self.bullets.add(Bullet(self.rect.center, -8, self.rect.bottom))

    # Updates the game as it is running
    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.bullets.update()


# Class that handles aspects of the bullets fired from the players and enemies
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height):
        super().__init__()
        # Loads the bullet image file
        self.image = pygame.image.load("bullet.png").convert_alpha()

        # Gives the bullet a rectangle collider
        self.rect = self.image.get_rect(center=pos)

        # Sets the speed of the bullet
        self.speed = speed

        # Sets the height of the screen
        self.height_y_constraint = screen_height

    # Deletes the bullet when it leaves the screen
    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()


# Class that handles the enemies
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, constraint):
        super().__init__()

        # Defines the edge of the screen
        self.max_x_constraint = constraint

        # How fast the enemy will move
        self.speed = speed

        #self.rect = self.image.get_rect(midtop=(x, y))

    # Stops the enemy from leaving the screen
    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    # Moves the enemies
    '''def move(self):
        turn_around = False
        if self.rect.right != self.max_x_constraint & turn_around == False:
            self.rect.x += self.speed
            if self.rect.right == self.max_x_constraint:
                turn_around = True

        elif self.rect.left != 0 & turn_around == True:
            self.rect.x -= self.speed '''

    # Updates the enemy as the game is running
    def update(self, direction):
        self.constraint()
        self.rect.x += direction


# Subclass that handles the easy enemies (green)
class EasyEnemy(Enemy):
    def __init__(self, x, y, speed, constraint):
        super().__init__(x, y, speed, constraint)
        file_path = 'enemy_green.png'
        self.speed = speed
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(midtop=(x, y))


# Subclass that handles the medium enemies (red)
class MediumEnemy(Enemy):
    def __init__(self, x, y, speed, constraint):
        super().__init__(x, y, speed, constraint)
        file_path = 'enemy_red.png'
        self.speed = speed
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(midtop=(x, y))


# Subclass that handles the hard enemies (purple)
class HardEnemy(Enemy):
    def __init__(self, x, y, speed, constraint):
        super().__init__(x, y, speed, constraint)
        file_path = 'enemy_purple.png'
        self.speed = speed
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(midtop=(x, y))
