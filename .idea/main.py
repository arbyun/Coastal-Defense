import random
from sprite_classes import *
from calculations import *
from pause_and_gameover_screens import *

pygame.init()

fpsClock = pygame.time.Clock()
FPS = 60
screen = pygame.display.set_mode((1000, 380))
gravity = (0, 980)  # 9.8 m/s^2

# Set the colors for the shapes
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Set the delay between the creation of new enemies (in seconds)
enemy_creation_delay = 2
collision_delay = 2

# Set the timer for the enemy creation delay to the initial delay value
enemy_creation_timer = enemy_creation_delay
collision_delay_timer = collision_delay

# Set the flag for creating a new enemy
new_enemy = False
mouse_time = 0
font = pygame.font.SysFont("Arial", 20)
level = 1
lives = 3
heart_image = pygame.image.load("sprites/pixel_heart_idle.png")
heart_image = pygame.transform.scale(heart_image, (20, 20))

heart1_pos = (900, 40)
heart2_pos = (920, 40)
heart3_pos = (940, 40)

heart_image1 = {heart_image: heart1_pos}
heart_image2 = {heart_image: heart2_pos}
heart_image3 = {heart_image: heart3_pos}

blt = False

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()

        if event.type == pygame.K_ESCAPE:
            pause()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_time = pygame.time.get_ticks()

        if event.type == pygame.MOUSEBUTTONUP:
            elapsed_time = pygame.time.get_ticks() - mouse_time
            # Get mouse position in a tuple of (x, y)
            mouse_pos = pygame.mouse.get_pos()
            # Calculate the shooting force
            shooting_force = elapsed_time / 1000
            # Calculate the initial velocity of the bullet
            bullet_vel = (shooting_force * 50, -shooting_force * 50)
            # Set the initial position of the bullet in the center of the cannon
            cannon_pos = (100, 300)
            # Create a new bullet
            angle = calculate_angle(mouse_pos, cannon_pos)
            bullet = Projectile(cannon_pos, bullet_vel, angle, 5)
            blt = True

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

    for enemy in enemies:
        if level == 2:
            enemy.speed += 0.5
        elif level == 3:
            enemy.speed += 1
        elif level == 4:
            enemy.speed += 1.5
        elif level == 5:
            enemy.speed += 2
        elif level == 6:
            enemy.speed += 2.5
        elif level == 7:
            enemy.speed += 3

    screen.fill(BLACK)

    # Add a tiny enemy to the enemies list
    enemies.append(tiny_boat)

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

    # Draw the enemies
    for enemy in enemies:
        enemy.draw(screen)
        enemy.update()
        if enemy.collide(danger_zone_rect):
            new_enemy = True
            lives -= 1
            # Sink the ship
            enemy.y += sinking_speed
            break
        # Remove the sunk enemy from the list after it has sunk
        if enemy.y > screen.get_height():
            enemies.remove(enemy)
        if len(enemies) > 1:
            for i in range(len(enemies) - 1):
                if enemies[i].colliderect(enemies[i + 1]):
                    enemies[i + 1].y += random.randint(1, 10)

    # Create a new enemy if the timer has reached 0
    if new_enemy and enemy_creation_timer <= 0:
        # Create a new enemy with a random size
        nwenemy = random.choice((tiny_boat, small_boat, medium_boat, large_boat, huge_boat))
        enemies.append(nwenemy)
        # Reset the enemy creation timer
        enemy_creation_timer = enemy_creation_delay
        new_enemy = False

    # Draw the bullet
    if blt:
        bull_time = pygame.time.get_ticks() / 1000
        bullet_vel = (bullet_vel[0], bullet_vel[1] + gravity[1] * bull_time)
        bullet_pos = (cannon_pos[0] + bullet_vel[0] * bull_time, cannon_pos[1] + bullet_vel[1] * bull_time)
        bullet.draw(cannon_pos, bullet_pos)
        # bullet.update()

    pygame.display.update()

pygame.quit()
