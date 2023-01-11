import math
import pygame

screen = pygame.display.set_mode((1000, 380))
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define the enemy sizes
tiny_enemy_size = 20
small_enemy_size = 40
medium_enemy_size = 60
large_enemy_size = 80
huge_enemy_size = 100

# Set the sinking speed of the enemy boats
sinking_speed = 2
collided = False

# Initialize the enemies list
enemies = []
projectiles = []

# Set the default enemy speed
enemy_speed = 3.5

score = 0


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, size, speed):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = pos
        self.image = pygame.Surface((size, size))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed

        # check for collisions with projectiles
        for projectile in projectiles:
            if self.collide(projectile):
                projectiles.remove(projectile)
                break

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def collide(self, other):
        global score
        if self.rect.colliderect(other):
            if self.size == tiny_enemy_size:
                score += 5
            elif self.size == small_enemy_size:
                score += 4
            elif self.size == medium_enemy_size:
                score += 3
            elif self.size == large_enemy_size:
                score += 2
            elif self.size == huge_enemy_size:
                score += 1
            enemies.remove(self)
            return True
        else:
            return False


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.draw.rect(screen, WHITE, (0, 0, 10, 10))
        self.center = (x, y)
        self.angle = angle
        self.speed = speed
        self.x = x
        self.y = y

    def update(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))
        self.center = (self.x, self.y)

    def draw(self, pos1, pos2):
        # Draw a line
        pygame.draw.line(screen, WHITE, pos1, pos2, 8)


tiny_boat = Enemy((500, 0), tiny_enemy_size, enemy_speed)
small_boat = Enemy((600, 0), small_enemy_size, enemy_speed)
medium_boat = Enemy((700, 0), medium_enemy_size, enemy_speed)
large_boat = Enemy((800, 0), large_enemy_size, enemy_speed)
huge_boat = Enemy((900, 0), huge_enemy_size, enemy_speed)
