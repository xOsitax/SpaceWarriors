import pygame

# Set up screen size
screen_width = 800
screen_height = 600


# Class that handles the player attributes
class Player(pygame.sprite.Sprite):
    # Initializes the player
    def __init__(self, path, pos, xconstraint, yconstraint, speed, player=0):
        super().__init__()
        # Loads the player image file
        self.image = pygame.image.load(path).convert_alpha()
        self.orig_image = self.image

        # Gives the player a rectangle collider
        self.rect = self.image.get_rect(midbottom=pos)

        # How fast the player will move
        self.speed = speed

        # Which player (game mode)
        self.player = player

        # Defines the edge of the screen
        self.max_x_constraint = xconstraint
        self.max_y_constraint = yconstraint

        # To check if bullet is ready to shoot
        self.ready = True

        # Sets the time when a bullet is shot
        self.shoot_time = 0

        # Timer to prevent infinite shooting
        if player == 0:
            self.cooldown = 600
        else:
            self.cooldown = 400

        # Helps to create a new bullet sprite on each key press
        if player == 0:
            self.bullets = pygame.sprite.Group()
        if player == 1:
            self.yellow_bullets = pygame.sprite.Group()
        if player == 2:
            self.red_bullets = pygame.sprite.Group()

        # Declare the shoot sound effect
        self.shoot_sound = pygame.mixer.Sound("assets/shoot.wav")

    # Gets player input
    def get_input(self):
        # Detect if a key is pressed
        keys = pygame.key.get_pressed()
        if self.player == 0:
            # Move the player left/right
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
            # Shoot bullet only when cooldown is 0
            if keys[pygame.K_SPACE] and self.ready:
                self.shoot()
                # Triggers the bullet cooldown
                self.ready = False
                self.shoot_time = pygame.time.get_ticks()
        if self.player == 1:
            # Move player 1 in all directions
            if keys[pygame.K_w]:
                self.rect.y -= self.speed
            if keys [pygame.K_s]:
                self.rect.y += self.speed
            if keys[pygame.K_a]:
                self.rect.x -= self.speed
            if keys[pygame.K_d]:
                self.rect.x += self.speed
            # Shoot bullet only when cooldown is 0
            if keys[pygame.K_LSHIFT] and self.ready:
                self.shoot()
                # Triggers the bullet cooldown
                self.ready = False
                self.shoot_time = pygame.time.get_ticks()
        if self.player == 2:
            # Move player 2 in all directions
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
            if keys[pygame.K_UP]:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN]:
                self.rect.y += self.speed
            # Shoot bullet only when cooldown is 0
            if keys[pygame.K_RSHIFT] and self.ready:
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
        if self.player == 2:
            if self.rect.left <= screen_width / 2 + 10:
                self.rect.left = screen_width / 2 + 10
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint
        if self.rect.bottom >= self.max_y_constraint:
            self.rect.bottom = self.max_y_constraint
        if self.rect.top <= 40:
            self.rect.top = 40

    # Method that handles shooting bullets by the player
    def shoot(self):
        if self.player == 0:
            self.bullets.add(Bullet("assets/bullet.png", self.rect.center, -8, self.rect.bottom, screen_width))
        if self.player == 1:
            self.yellow_bullets.add(Bullet("assets/yellowBullet.png", self.rect.center, 8, self.rect.bottom, screen_width,
                                           1))
        if self.player == 2:
            self.red_bullets.add(Bullet("assets/redBullet.png", self.rect.center, -8, self.rect.bottom, screen_width, 1))
        pygame.mixer.Sound.play(self.shoot_sound)

    # Updates the game as it is running
    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        if self.player == 0:
            self.bullets.update()
        elif self.player == 1:
            self.yellow_bullets.update()
        elif self.player == 2:
            self.red_bullets.update()


# Class that handles aspects of the bullets fired from the players and enemies
class Bullet(pygame.sprite.Sprite):
    def __init__(self, path, pos, speed, screen_height, screen_width, mode=0):
        super().__init__()
        # Loads the bullet image file
        self.image = pygame.image.load(path).convert_alpha()

        # Gives the bullet a rectangle collider
        self.rect = self.image.get_rect(center=pos)

        # Sets the speed of the bullet
        self.speed = speed

        # Which player
        self.mode = mode

        # Sets the constraints
        self.height_y_constraint = screen_height
        self.x_constraint = screen_width

    # Deletes the bullet when it leaves the screen
    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()
        elif self.rect.x <= -50 or self.rect.x >= self.x_constraint + 50:
            self.kill()

    def update(self):
        if self.mode == 0:
            self.rect.y += self.speed
        else:
            self.rect.x += self.speed
        self.destroy()


# Class that handles enemy bullets
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, path, pos, speed, screen_height):
        super().__init__()
        # Loads the bullet image file
        self.image = pygame.image.load(path).convert_alpha()

        # Gives the bullet a rectangle collider
        self.rect = self.image.get_rect(center=pos)

        # Sets the speed of the bullet
        self.speed = speed

        # Sets the constraints
        self.height_y_constraint = screen_height

    # Deletes the bullet when it leaves the screen
    def destroy(self):
        pass
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

        # Helps to create a new bullet sprite on each key press
        self.bullets = pygame.sprite.Group()

        # Sets the time when a bullet is shot
        self.shoot_time = 0

        # To check if bullet is ready to shoot
        self.ready = True

        # Timer to prevent infinite shooting
        self.cooldown = 600

    # Stops the enemy from leaving the screen
    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    # Method that handles shooting bullets by the enemy
    '''def shoot(self):
        # Shoot bullet only when cooldown is 0
        if self.ready:
            self.bullets.add(EnemyBullet(self.rect.center, 8, self.rect.bottom))
            # Triggers the bullet cooldown
            self.ready = False
            self.shoot_time = pygame.time.get_ticks()

    # Handles the bullet recharge time
    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.cooldown:
                self.ready = True'''

    # Moves the enemies
    def move(self):
        if self.rect.right >= screen_width:
            self.speed = -self.speed
        elif self.rect.left <= 0:
            self.speed = -self.speed

    # Updates the enemy as the game is running
    def update(self):
        self.constraint()
        self.move()
        self.rect.x += self.speed
        #self.shoot()
        #self.recharge()
        self.bullets.update()


# Subclass that handles the easy enemies (green)
class EasyEnemy(Enemy):
    def __init__(self, x, y, speed, constraint):
        super().__init__(x, y, speed, constraint)
        file_path = 'assets/enemy_green.png'
        self.speed = speed
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(midtop=(x, y))


# Subclass that handles the medium enemies (red)
class MediumEnemy(Enemy):
    def __init__(self, x, y, speed, constraint):
        super().__init__(x, y, speed, constraint)
        file_path = 'assets/enemy_red.png'
        self.speed = speed
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(midtop=(x, y))


# Subclass that handles the hard enemies (purple)
class HardEnemy(Enemy):
    def __init__(self, x, y, speed, constraint):
        super().__init__(x, y, speed, constraint)
        file_path = 'assets/enemy_purple.png'
        self.speed = speed
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(midtop=(x, y))


# Class that handles the asteroids
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, angle_change, direction=1):
        super().__init__()
        # Loads the asteroid image file
        self.image = pygame.image.load("assets/asteroid.png").convert_alpha()
        self.orig_image = self.image
        self.broken_image = pygame.image.load("assets/asteroid_broken.png").convert_alpha()

        if direction == -1:
            y = screen_height + 50

        # Gives the asteroid a rectangle collider
        self.rect = self.image.get_rect(center=(x, y))

        # How fast the asteroid will move
        self.speed = speed * direction
        if direction == 1:
            self.direction = 'down'
        elif direction == -1:
            self.direction = 'up'

        # How many hits it takes to kill the asteroid
        self.health = 2

        self.angle = 0
        self.angle_change = angle_change

        # Sets the constraint
        self.height_y_constraint = screen_height

    # Deletes the asteroid when it leaves the screen
    def destroy(self):
        if self.direction == 'down':
            if self.rect.y >= self.height_y_constraint + 50:
                self.kill()
        if self.direction == 'up':
            if self.rect.y <= 0 - 100:
                self.kill()

    # Rotates the asteroid
    def rotate(self):
        if self.angle_change != 0:
            self.angle += self.angle_change
            self.image = pygame.transform.rotozoom(self.orig_image, self.angle, 1)
            self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.rect.y += self.speed
        self.destroy()
        self.rotate()


# Class that handles death animations
class Boom(pygame.sprite.Sprite):
    def __init__(self, pos, path):
        super().__init__()
        # Loads the asteroid image file
        self.image = pygame.image.load(path).convert_alpha()

        # Gives the asteroid a rectangle collider
        self.rect = self.image.get_rect(center=pos)

        # Sets the alpha for fadeout
        self.alpha = 255

    def update(self):
        self.alpha = max(0, self.alpha - 5)  # alpha should never be < 0.
        self.image = self.image.copy()
        self.image.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)
        if self.alpha <= 0:  # Kill the sprite when the alpha is <= 0.
            self.kill()