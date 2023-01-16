import math
import random
import numpy as np
import sys
import pygame
from pygame.locals import *
from pygame import gfxdraw

# Initialize pygame
pygame.init()

# Set the window size
window_size = (1000, 380)

# Create the window
screen = pygame.display.set_mode(window_size)

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
enemy_speed = 1.5

mouse=False
gravity = 9.8

danger_zone_rect = pygame.Rect(100, 280, 50, 100)
player_rect = pygame.Rect(0, 280, 100, 100)
cannon_base_rect = pygame.Rect(player_rect.centerx - 10, player_rect.top - 20, 10, 20)
cannon_barrel_rect = pygame.Rect(cannon_base_rect.centerx - 5, cannon_base_rect.centery - 20, 30, 10)
enemy_area_rect = pygame.Rect(140, 300, 860, 360 // 4)

# Add the initial enemy boat to the list
tiny_enemy_rect = pygame.Rect(enemy_area_rect.centerx - 10, enemy_area_rect.top - 5, 20, 10)
enemies.append(tiny_enemy_rect)

# Set the flag for creating a new enemy
new_enemy = False

font = pygame.font.SysFont("Arial", 20)
score = 0
level = 1
lives = 3
heart_image = pygame.image.load("sprites/Pixel_heart_idle.png")
heart_image = pygame.transform.scale(heart_image, (20, 20))

heart1_pos = (900, 40)
heart2_pos = (920, 40)
heart3_pos = (940, 40)

heart_image1 = {heart_image: heart1_pos}
heart_image2 = {heart_image: heart2_pos}
heart_image3 = {heart_image: heart3_pos}


def calculate_center(p0, p1):
    x0, y0 = p0
    x1, y1 = p1
    return (x0 + x1) / 2, (y0 + y1) / 2




bullets = []


class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, color, x, y, radius):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.draw.circle(screen, color, (x, y), radius, 5)
        self.x = x
        self.y = y
        self.rect = self.image
        self.rect.center = (x, y)
        self.gravity = 9.8
        bullets.append(self)

    def kill_bullet(self):
        self.kill()
        bullets.remove(self)


def shoot_bullet(v0):
    global enemies, new_enemy, score
   
    x0=80
    y0=300
    x3=80
    y3=300
# Clacular o seno e o cosseno
    mouse=pygame.mouse.get_pos()
    hipotenosa=np.sqrt(np.square(mouse[0])+np.square(mouse[1]))
    seno=np.divide(380-mouse[1],hipotenosa)
    cosseno=np.divide(mouse[0],hipotenosa)

    g=int(9.8)
   
    t=1
    
    
    while x3<1000 and y3>0 and x3>0 and y3<800:
        t=t+1
       

        #formula para o movimento 
        x3=x0+v0*cosseno*t
        y3=y0-v0*t*seno+1/2*g*np.square(t)
        

   
        bullet=Bullet(screen, RED,x3, y3, 5)
    
        for enemy in enemies:
            
            if enemy.colliderect(bullet):
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
                # Remove the enemy and bullet from their respective lists
                enemies.remove(enemy)
                    
                new_enemy = True
                break

    pygame.display.update()
    clock.tick((5))


# Set the charging rate (how quickly the end angle increases)
charging_rate = 5

# Set the charging limit (maximum end angle)
charging_limit = 180

# Set the charging flag to False
is_charging = False

game_over = False

# Run the game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            game_over = True
        elif event.type == MOUSEBUTTONDOWN:
            mouse=True
            # Set the charging flag to True when the mouse button is pressed
            is_charging = True
            arc_angle = 180
            arc_end_angle = arc_angle
        elif event.type == MOUSEBUTTONUP:
            mouse=False
            # Set the charging flag to False when the mouse button is released
            is_charging = False
            shoot_bullet(v0)
            arc_end_angle = 0
            arc_angle = 0
    
# aumenta a velocidade ao pressionar o botão do rato
    if mouse==True and v0<90:
        v0=v0+5
      
    elif mouse==True and v0==90:
        pass
    else:
        v0=0

    # Update the arc end angle if the mouse button is being held down
    if is_charging:
        arc_end_angle += 5
        if arc_end_angle < 0:
            arc_end_angle = 0

    # Clear the screen
    screen.fill(BLACK)

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

    # Draw the player area at the bottom of the screen
    pygame.draw.rect(screen, WHITE, player_rect)

    # Draw the cannon on top of the player area (collides with the player area)
    pygame.draw.rect(screen, BLUE, cannon_base_rect)
    # Draw the cannon barrel in the middle front of the cannon base
    pygame.draw.rect(screen, BLUE, cannon_barrel_rect)

    # Draw the enemy area
    pygame.draw.rect(screen, BLUE, enemy_area_rect)

    # Draw the danger zone
    pygame.draw.rect(screen, GREEN, danger_zone_rect)

   

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
        # Draw the enemy boats
        pygame.draw.rect(screen, RED, enemy)

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

    # Check if the bullet has collided with an enemy
    

    # Update the display
    pygame.display.flip()

    clock = pygame.time.Clock()
    clock.tick(60)

    if game_over:
        # Draw the game over text in the middle of the black screen
        screen.fill(BLACK)
        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2,
                                     screen.get_height() // 2 - game_over_text.get_height() // 2))

        # Update the display
        pygame.display.update()

        # Wait for 5 seconds
        pygame.time.wait(5000)
        running = False

        # Quit the game
        pygame.quit()
        sys.exit()

# Quit pygame
pygame.quit()