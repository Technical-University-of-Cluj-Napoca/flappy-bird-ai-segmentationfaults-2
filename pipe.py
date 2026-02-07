import pygame
from utils import win_width, scroll_speed

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, image, pipe_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.passed = False
        self.pipe_type = pipe_type

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.x <= -win_width:
            self.kill()