import pygame
from utils import *

def create_button(text, width, height, color=(223, 113, 38), text_color=(255, 255, 255)):
   
    button = pygame.Surface((width, height))
    button.fill(color)
    
    pygame.draw.rect(button, (255, 255, 255), (0, 0, width, height), 3)
    pygame.draw.rect(button, (180, 80, 20), (3, 3, width-6, height-6), 2)
    
    font = pygame.font.SysFont('Arial', int(height * 0.5), bold=True)
    text_surface = font.render(text, True, text_color)
    text_x = (width - text_surface.get_width()) // 2
    text_y = (height - text_surface.get_height()) // 2
    button.blit(text_surface, (text_x, text_y))
    
    return button


start_button = create_button("START", BUTTON_WIDTH, BUTTON_HEIGHT)
rate_button = create_button("RATE", BUTTON_WIDTH, BUTTON_HEIGHT)
score_button = create_button("SCORE", BUTTON_WIDTH, BUTTON_HEIGHT)


def create_title_image():
    title_font = pygame.font.SysFont('Arial', int(50 * SCALE * 0.5), bold=True)
    
    flappy_text = title_font.render("Flappy", True, (83, 175, 30))  # Green
    bird_text = title_font.render("Bird", True, (83, 175, 30))
    
    total_width = flappy_text.get_width() + bird_text.get_width() + 20
    title_surface = pygame.Surface((total_width + 60, flappy_text.get_height() + 10), pygame.SRCALPHA)
    
    shadow_font = pygame.font.SysFont('Arial', int(50 * SCALE * 0.5), bold=True)
    shadow_flappy = shadow_font.render("Flappy", True, (50, 100, 20))
    shadow_bird = shadow_font.render("Bird", True, (50, 100, 20))
    
    title_surface.blit(shadow_flappy, (3, 3))
    title_surface.blit(shadow_bird, (flappy_text.get_width() + 23, 3))
    title_surface.blit(flappy_text, (0, 0))
    title_surface.blit(bird_text, (flappy_text.get_width() + 20, 0))
    
    return title_surface

title_image = create_title_image()


def draw_score(window, score, x, y, centered=True, size='normal'):
    if size == 'tiny':
        images = tiny_number_images
    elif size == 'small':
        images = small_number_images
    else:
        images = number_images
    
    score_str = str(score)
    
 
    total_width = sum(images[int(digit)].get_width() for digit in score_str)
    
    if centered:
        start_x = x - total_width // 2
    else:
        start_x = x
    

    current_x = start_x
    for digit in score_str:
        digit_img = images[int(digit)]
        window.blit(digit_img, (current_x, y))
        current_x += digit_img.get_width()

skyline_image = pygame.transform.scale(pygame.image.load("sprites/background-night.png"), (win_width, win_height))


def create_copyright_text():
    font = pygame.font.SysFont('Arial', int(14 * SCALE * 0.6))
    return font.render("(c) .GEARS Studios 2013", True, (255, 255, 255))



