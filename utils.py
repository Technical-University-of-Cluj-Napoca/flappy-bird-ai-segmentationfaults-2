import pygame

win_height = 720
win_width = 551
scroll_speed = 1

# Universal scale factor to match original 288x512 proportions
ORIGINAL_WIDTH = 288
ORIGINAL_HEIGHT = 512
SCALE = win_width / ORIGINAL_WIDTH  # ~1.91

# Ground height (original is ~112px, scaled properly)
GROUND_HEIGHT = int(112 * SCALE * 0.6)  # ~128px - slightly smaller for more play area

# Bird start position
bird_start_position = (100, 300)

def scale_image(image, scale_factor):
    """Scale an image by a given factor"""
    width = int(image.get_width() * scale_factor)
    height = int(image.get_height() * scale_factor)
    return pygame.transform.scale(image, (width, height))

# Load and scale bird images (original bird is ~34x24px)
bird_scale = SCALE * 0.7  # Makes bird appropriately sized
bird_images = [scale_image(pygame.image.load("sprites/redbird-downflap.png"), bird_scale),
               scale_image(pygame.image.load("sprites/redbird-midflap.png"), bird_scale),
               scale_image(pygame.image.load("sprites/redbird-upflap.png"), bird_scale)]

# Load and scale ground image (wide enough for seamless scrolling)
_ground_raw = pygame.image.load("sprites/base.png")
ground_image = pygame.transform.scale(_ground_raw, (win_width + 100, GROUND_HEIGHT))

# Calculate playable area (from top to ground)
PLAYABLE_HEIGHT = win_height - GROUND_HEIGHT  # Area where bird can fly

# Load and scale pipe images - pipes should be TALL (extend off-screen)
# Original pipe is ~320px tall, we make them much taller to extend off screen
_top_pipe_raw = pygame.image.load("sprites/pipe-green-down.png")
_bottom_pipe_raw = pygame.image.load("sprites/pipe-green.png")
pipe_width = int(_top_pipe_raw.get_width() * SCALE * 0.7)  # Same width scale as bird
pipe_height = 500  # Tall enough to extend off-screen and reach ground
top_pipe_image = pygame.transform.scale(_top_pipe_raw, (pipe_width, pipe_height))
bottom_pipe_image = pygame.transform.scale(_bottom_pipe_raw, (pipe_width, pipe_height))

# Load and scale UI images
game_over_image = scale_image(pygame.image.load("sprites/gameover.png"), SCALE * 0.8)
start_image = scale_image(pygame.image.load("sprites/start.png"), SCALE * 0.8)

# Scale background to fit window exactly
skyline_image = pygame.transform.scale(pygame.image.load("sprites/background-night.png"), (win_width, win_height))