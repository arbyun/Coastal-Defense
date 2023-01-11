import sys
from sprite_classes import screen, pygame

pause_image = pygame.image.load("sprites/pause.png")


def pause():
    global pause
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    global pause_surface
                    # make pause surface not visible
                    pause_surface.set_alpha(0)
                    # remove the image
                    screen.blit(pause_surface, (0, 0))
                    pause = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Create a new surface and make it 50% transparent
        pause_surface = pygame.Surface((1000, 380))
        pause_surface.set_alpha(128)
        pause_surface.fill((0, 0, 0))
        # Spawn an image in the middle of the pause surface
        screen.blit(pause_surface, (0, 0))
        pause_surface.blit(pause_image, (450, 150))
        pygame.display.update()
