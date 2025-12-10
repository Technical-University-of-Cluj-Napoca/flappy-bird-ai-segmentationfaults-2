import pygame
import sys
from sprites import SpriteSheet, get_background_night, get_base

class FlappyBirdUI:
    def __init__(self, width=576, height=1024):
        pygame.init()
        self.width = width
        self.height = height
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
        
        # Draw Base (2 copies for scrolling)
        self.screen.blit(self.base, (self.base_scroll, self.ground_y))
        self.screen.blit(self.base, (self.base_scroll + self.base.get_width(), self.ground_y))
        # Add a 3rd one just in case 576 > 672? No, 576 < 672. But if scroll moves left...
        # If scroll is -4, second copy is at 332. Ends at 668. Covers 576. 
        # But when scroll is -336, it snaps to 0. 
        # So we need enough copies to cover 'width + one sprite width'.
        # 576 + 336 = 912. 3 sprites (336*3=1008) is safer.
        self.screen.blit(self.base, (self.base_scroll + self.base.get_width() * 2, self.ground_y))

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
