import pygame
from sys import exit
import random
from bird import Bird
from pipe import Pipe
from ground import Ground
from utils import *

pygame.init()
clock = pygame.time.Clock()


window = pygame.display.set_mode((win_width, win_height))



score = 0
font = pygame.font.SysFont('Segoe', 26)
game_stopped = True



def quit_game():
    # Exit Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


# Game Main Method
def main():
    global score

    # Instantiate Bird
    bird = pygame.sprite.GroupSingle()
    bird.add(Bird())

    # Setup Pipes
    pipe_timer = 0
    pipes = pygame.sprite.Group()

    # Instantiate Initial Ground (position at bottom of screen)
    x_pos_ground = 0
    y_pos_ground = win_height - ground_image.get_height()
    ground = pygame.sprite.Group()
    ground.add(Ground(x_pos_ground, y_pos_ground))

    run = True
    while run:
        # Quit
        quit_game()

        # Reset Frame
        window.fill((0, 0, 0))

        # User Input
        user_input = pygame.key.get_pressed()

        # Draw Background
        window.blit(skyline_image, (0, 0))

        # Spawn Ground
        if len(ground) <= 2:
            ground.add(Ground(win_width, y_pos_ground))

        # Draw - Pipes, Ground and Bird
        pipes.draw(window)
        ground.draw(window)
        bird.draw(window)

        # Show Score
        score_text = font.render('Score: ' + str(score), True, pygame.Color(255, 255, 255))
        window.blit(score_text, (20, 20))

        # Update - Pipes, Ground and Bird
        if bird.sprite.alive:
            pipes.update()
            ground.update()
        bird.update(user_input)

        # Collision Detection
        collision_pipes = pygame.sprite.spritecollide(bird.sprites()[0], pipes, False)
        collision_ground = pygame.sprite.spritecollide(bird.sprites()[0], ground, False)
        if collision_pipes or collision_ground:
            bird.sprite.alive = False
            if collision_ground:
                window.blit(game_over_image, (win_width // 2 - game_over_image.get_width() // 2,
                                              win_height // 2 - game_over_image.get_height() // 2))
                if user_input[pygame.K_r]:
                    score = 0
                    break

        # Spawn Pipes
        if pipe_timer <= 0 and bird.sprite.alive:
            x_pos = win_width + 10
            pipe_gap = random.randint(140, 180)  # Gap for bird to fly through
            
            # Random position for the gap (where bird flies through)
            # Gap should be in the middle portion of playable area
            min_gap_top = 80  # Minimum distance from top
            max_gap_top = y_pos_ground - pipe_gap - 80  # Leave room at bottom
            gap_top = random.randint(min_gap_top, max_gap_top)
            
            # Top pipe: bottom edge at gap_top, extends upward off-screen
            y_top = gap_top - top_pipe_image.get_height()
            
            # Bottom pipe: top edge at gap_bottom, extends down to ground
            y_bottom = gap_top + pipe_gap
            
            pipes.add(Pipe(x_pos, y_top, top_pipe_image, 'top'))
            pipes.add(Pipe(x_pos, y_bottom, bottom_pipe_image, 'bottom'))
            pipe_timer = random.randint(180, 250)
        pipe_timer -= 1

        clock.tick(60)
        pygame.display.update()


# Menu
def menu():
    global game_stopped

    while game_stopped:
        quit_game()

        # Draw Menu
        window.fill((0, 0, 0))
        window.blit(skyline_image, (0, 0))
        window.blit(ground_image, (0, win_height - ground_image.get_height()))
        window.blit(bird_images[0], bird_start_position)
        window.blit(start_image, (win_width // 2 - start_image.get_width() // 2,
                                  win_height // 2 - start_image.get_height() // 2))

        # User Input
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_SPACE]:
            main()

        pygame.display.update()


menu()
