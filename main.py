import math
import random
import time
import pygame
import sys
from pygame import gfxdraw

# Initialize Pygame and set the window size
pygame.init()
screen = pygame.display.set_mode((1000, 380))

# Set the colors for the shapes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Define the enemy sizes
tiny_enemy_size = 20
small_enemy_size = 40
medium_enemy_size = 60
large_enemy_size = 80
huge_enemy_size = 100

# Set the sinking speed of the enemy boats
sinking_speed = 2
collided = False

# Set the delay between the creation of new enemies (in seconds)
enemy_creation_delay = 2
collision_delay = 2

# Set the timer for the enemy creation delay to the initial delay value
enemy_creation_timer = enemy_creation_delay
collision_delay_timer = collision_delay

# Initialize the enemies list
enemies = []

# Set the enemy speed
enemy_speed = 3.5


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.draw.rect(screen, WHITE, (0, 0, 10, 10))
        self.center = (x, y)
        self.angle = angle
        self.speed = 3
        self.x = x
        self.y = y

    def update(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))
        self.center = (self.x, self.y)
        self.draw()

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, 10, 10))


# Draw the player area at the bottom of the screen
player_rect = pygame.Rect(0, 280, 100, 100)
pygame.draw.rect(screen, WHITE, player_rect)

# Draw the cannon on top of the player area (collides with the player area)
cannon_base_rect = pygame.Rect(player_rect.centerx - 10, player_rect.top - 20, 10, 20)
pygame.draw.rect(screen, BLUE, cannon_base_rect)
# Draw the cannon barrel in the middle front of the cannon base
cannon_barrel_rect = pygame.Rect(cannon_base_rect.centerx - 5, cannon_base_rect.centery - 20, 30, 10)
pygame.draw.rect(screen, BLUE, cannon_barrel_rect)

# Draw the enemy area
enemy_area_rect = pygame.Rect(140, 300, 860, 360 // 4)
pygame.draw.rect(screen, BLUE, enemy_area_rect)

# Draw the danger zone
danger_zone_rect = pygame.Rect(100, 280, 50, 100)
pygame.draw.rect(screen, GREEN, danger_zone_rect)

# Add the initial enemy boat to the list
tiny_enemy_rect = pygame.Rect(enemy_area_rect.centerx - 10, enemy_area_rect.top - 5, 20, 10)
enemies.append(tiny_enemy_rect)

# Set the flag for creating a new enemy
new_enemy = False

font = pygame.font.SysFont("Arial", 20)
score = 0
level = 1
lives = 3
heart_image = pygame.image.load("../../../PycharmProjects/CoastalDefense/sprites/Pixel_heart_idle.png")
heart_image = pygame.transform.scale(heart_image, (20, 20))

heart1_pos = (900, 40)
heart2_pos = (920, 40)
heart3_pos = (940, 40)

heart_image1 = {heart_image: heart1_pos}
heart_image2 = {heart_image: heart2_pos}
heart_image3 = {heart_image: heart3_pos}





''''Bullet'''

p0 = (cannon_barrel_rect.centerx, cannon_barrel_rect.centery)


def draw_arc(surface, x, y, radius, start_angle, stop_angle, color):
    start_angle = int(start_angle % 360)
    stop_angle = int(stop_angle % 360)
    if start_angle == stop_angle:
        gfxdraw.circle(surface, x, y, radius, color)
    else:
        gfxdraw.arc(surface, x, y, radius, start_angle, stop_angle, color)


def calculate_center(p0, p1):
    x0, y0 = p0
    x1, y1 = p1
    return (x0 + x1) / 2, (y0 + y1) / 2


def calculate_angle(p0, p1):
    x0, y0 = p0
    x1, y1 = p1
    return math.degrees(math.atan2(y1 - y0, x1 - x0))


def shoot_bullet(p0, p1):
    global enemies, new_enemy, score
    """Shoot a bullet from the cannon."""
    angle = calculate_angle(p0, p1)
    center = calculate_center(p0, p1)
    end_angle = angle + 180
    center = (math.floor(center[0]), math.floor(center[1]))
    radius = math.floor(math.hypot(center[0] - p0[0], center[1] - p0[1]))
    arc_color = (255, 0, 0, 0)  # Red with 0% transparency
    draw_arc(screen, center[0], center[1], radius, angle, end_angle, arc_color)

    # Set the number of steps to take along the arc
    steps = 100

    # Set the initial position of the bullet along the arc
    x, y = center[0] + radius * math.cos(math.radians(angle)), center[1] + radius * math.sin(math.radians(angle))

    # Loop through the steps to draw the bullet at different positions along the arc
    for i in range(steps):
        # Calculate the angle at the current step
        current_angle = angle + (end_angle - angle) * i / steps

        # Calculate the position of the bullet at the current angle
        x2 = center[0] + radius * math.cos(math.radians(current_angle))
        y2 = center[1] + radius * math.sin(math.radians(current_angle))

        # Draw a line between the previous position and the current position
        line = pygame.draw.line(screen, WHITE, (x, y), (x2, y2), 8)

        # Update the position of the bullet
        x, y = x2, y2

        # Update the display
        pygame.display.flip()

        # Clear the screen
        screen.fill(BLACK)

        # Draw everything again
        draw_everything_again()

        # Collision detection
        for enemy in enemies:
            if enemy.colliderect(line):
                # Depending on the size of the enemy, add a different amount of points to the score
                if enemy.width == tiny_enemy_size:
                    score += 5
                elif enemy.width == small_enemy_size:
                    score += 4
                elif enemy.width == medium_enemy_size:
                    score += 3
                elif enemy.width == large_enemy_size:
                    score += 2
                elif enemy.width == huge_enemy_size:
                    score += 1
                enemies.remove(enemy)
                new_enemy = True
                break


def draw_everything_again():
    # Draw score in the top right corner
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (900, 10))

    # Draw player lives under the score, represented by hearts
    if lives == 3:
        screen.blit(heart_image, heart1_pos)
        screen.blit(heart_image, heart2_pos)
        screen.blit(heart_image, heart3_pos)
    elif lives == 2:
        screen.blit(heart_image, heart1_pos)
        screen.blit(heart_image, heart2_pos)
    elif lives == 1:
        screen.blit(heart_image, heart1_pos)

    # Draw the enemy area
    enemy_area_rect = pygame.Rect(140, 300, 860, 360 // 4)
    pygame.draw.rect(screen, BLUE, enemy_area_rect)

    # Draw the danger zone
    danger_zone_rect = pygame.Rect(100, 280, 50, 100)
    pygame.draw.rect(screen, GREEN, danger_zone_rect)

    # Draw the enemy boats
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    # Draw the player area at the bottom of the screen
    player_rect = pygame.Rect(0, 280, 100, 100)
    pygame.draw.rect(screen, WHITE, player_rect)

    # Draw the cannon on top of the player area (collides with the player area)
    cannon_base_rect = pygame.Rect(player_rect.centerx - 10, player_rect.top - 20, 10, 20)
    pygame.draw.rect(screen, BLUE, cannon_base_rect)
    # Draw the cannon barrel in the middle front of the cannon base
    cannon_barrel_rect = pygame.Rect(cannon_base_rect.centerx - 5, cannon_base_rect.centery - 20, 30, 10)
    pygame.draw.rect(screen, BLUE, cannon_barrel_rect)

    # Update the display
    pygame.display.update()

game_over = False

# Run the game loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get mouse position in a tuple of (x, y)
            mouse_pos = pygame.mouse.get_pos()
            shoot_bullet(mouse_pos, p0)

    # Decrement the enemy creation timer
    enemy_creation_timer -= 0.05
    collision_delay_timer -= 0.05

    if score <= 100:
        level = 1
    elif score >= 100:
        level = 2
    elif score >= 200:
        level = 3
    elif score >= 300:
        level = 4
    elif score >= 400:
        level = 5
    elif score >= 500:
        level = 6
    elif score >= 600:
        level = 7

    if level == 2:
        enemy_speed += 0.5
    elif level == 3:
        enemy_speed += 1
    elif level == 4:
        enemy_speed += 1.5
    elif level == 5:
        enemy_speed += 2
    elif level == 6:
        enemy_speed += 2.5
    elif level == 7:
        enemy_speed += 3

    # Move the enemy boats left
    for enemy in enemies:
        enemy.x -= enemy_speed

        # Check if the enemy has entered the danger zone
        if enemy.colliderect(danger_zone_rect):
            # Update the position of the enemy to appear "sunk" below the danger zone
            enemy.y += sinking_speed
            new_enemy = True
            collided = True

        # Remove the sunk enemy from the list after it has sunk
        if enemy.y > screen.get_height():
            enemies.remove(enemy)

    # Create a new enemy if the timer has reached zero and the new_enemy flag is set
    if new_enemy and enemy_creation_timer <= 0:
        # Create a new enemy
        # Width depends on the size of the enemy, get random size
        width = random.choice(
            [tiny_enemy_size, small_enemy_size, medium_enemy_size, large_enemy_size, huge_enemy_size])
        height = 10
        new_enemy_rect = pygame.Rect(screen.get_width(), enemy_area_rect.top - height, width, height)
        # Add the new enemy boat to the list
        enemies.append(new_enemy_rect)
        # Reset the enemy creation timer
        enemy_creation_timer = enemy_creation_delay
        new_enemy = False

    # If there are more than 1 enemies, make sure they don't overlap

    if len(enemies) > 1:
        for i in range(len(enemies) - 1):
            if enemies[i].colliderect(enemies[i + 1]):
                enemies[i + 1].y += random.randint(1, 10)

    # If enemies collide with the danger zone, take away a life from the player
    if collided and collision_delay_timer <= 0:
        for enemy in enemies:
            if enemy.colliderect(danger_zone_rect):
                lives -= 1
                if lives == 0:
                    game_over = True
                    break
                break
        collision_delay_timer = collision_delay
        collided = False

    # Clear the screen
    screen.fill(BLACK)

    # Draw everything again
    draw_everything_again()

    # Set the frame rate
    clock = pygame.time.Clock()
    clock.tick(60)

    # Delay to slow down the game
    time.sleep(0.01)

    # Update the display
    pygame.display.update()

    if game_over:
        # Draw the game over text in the middle of the black screen
        screen.fill(BLACK)
        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, screen.get_height() // 2 - game_over_text.get_height() // 2))

        # Update the display
        pygame.display.update()

        # Wait for 5 seconds
        pygame.time.wait(5000)

        # Quit the game
        pygame.quit()
        sys.exit()
