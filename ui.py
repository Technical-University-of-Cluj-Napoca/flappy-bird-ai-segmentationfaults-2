import pygame
import sys
from sprites import SpriteSheet, get_background_night, get_base

class FlappyBirdUI:
    def __init__(self, width=None, height=None):
        pygame.init()
        
        # Get screen dimensions
        info = pygame.display.Info()
        screen_height = info.current_h
        
        # Set Window Size (Height 80% of screen, Width 9:16 aspect ratio)
        if height is None:
            self.height = int(screen_height * 0.8)
        else:
            self.height = height
            
        if width is None:
            # Maintain 9:16 aspect ratio (phone screen)
            self.width = int(self.height * (9 / 16))
        else:
            self.width = width
            
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Flappy Bird AI")
        self.clock = pygame.time.Clock()
        
        # Load sprites
        self.sprite_sheet = SpriteSheet('flappy-sprites.png')
        self.background = get_background_night(self.sprite_sheet)
        self.base = get_base(self.sprite_sheet)
        
        # Scale background to fit new window size
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        
        # Game Variables
        self.base_scroll = 0
        self.scroll_speed = 4
        self.base_height = 112
        self.ground_y = self.height - self.base_height

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))
        
        # Draw Base (dynamic number of copies for scrolling)
        base_width = self.base.get_width()
        num_tiles = (self.width // base_width) + 2
        
        for i in range(num_tiles):
            self.screen.blit(self.base, (self.base_scroll + base_width * i, self.ground_y))

    def update(self):
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update Base Scroll
        self.base_scroll -= self.scroll_speed
        if abs(self.base_scroll) > self.base.get_width():
            self.base_scroll = 0

        # Drawing
        self.draw_background()
        
        # Update display
        pygame.display.update()
        self.clock.tick(30)
