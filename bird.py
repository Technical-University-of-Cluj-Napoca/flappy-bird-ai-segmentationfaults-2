import pygame
from ai import brain
from utils import bird_images, bird_start_position, win_height, GROUND_HEIGHT, window, win_width

class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bird_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = bird_start_position
        self.image_index = 0
        self.vel = 0
        self.flap = False
        self.alive = True
        self.max_y = win_height - GROUND_HEIGHT 

        # ai attributes
        self.lifespan = 0
        self.decision = None
        self.vision = [0.5, 1, 0.5]
        self.fitness = 0
        self.score = 0
        self.passed_pipes = set()
        self.inputs = 3
        self.brain = brain.Brain(self.inputs)
        self.brain.generate_net()
    def update(self, user_input, pipes=None):
        # Advance animation
        if self.alive:
            self.image_index += 1
        if self.image_index >= 30:
            self.image_index = 0
        self.image = bird_images[self.image_index // 10]

        # Gravity
        self.vel += 0.5
        if self.vel > 7:
            self.vel = 7

        # Move vertically (cap at ground)
        if self.rect.y < self.max_y:
            self.rect.y += int(self.vel)
        if self.vel == 0:
            self.flap = False

        # Rotation for drawing
        self.image = pygame.transform.rotate(self.image, self.vel * -7)

        # Safely check for space key (user_input can be a tuple from pygame or an empty dict from AI)
        is_space = False
        try:
            is_space = bool(user_input[pygame.K_SPACE])
        except Exception:
            is_space = False

        if is_space and not self.flap and self.rect.y > 0 and self.alive:
            self.flap = True
            self.vel = -7

        # If AI mode passes pipes in, check collisions with them
        if pipes is not None:
            # count per-bird passed bottom pipes as score
            try:
                for p in pipes:
                    if getattr(p, 'pipe_type', None) == 'bottom':
                        # Check if bird has passed this pipe (bird x is to the right of pipe right edge)
                        if p.rect.right < self.rect.left and id(p) not in self.passed_pipes:
                            self.passed_pipes.add(id(p))
                            self.score += 1
                            print(f'Bird passed pipe! Score now: {self.score}')
            except Exception as e:
                print(f'Error checking pipe pass: {e}')
                pass

            if self.pipe_collision(pipes) or self.rect.y >= self.max_y:
                self.alive = False
                self.flap = False
                self.vel = 0

        # Lifespan increments while alive
        if self.alive:
            self.lifespan += 1

    # --- AI / compatibility methods adapted from original Player class ---
    def draw(self, window):
        # Population code calls this on individual birds
        window.blit(self.image, self.rect)

    def ground_collision(self, ground):
        # ground can be a sprite Group or a single sprite/rect
        try:
            for g in ground:
                if pygame.Rect.colliderect(self.rect, g.rect):
                    return True
            return False
        except Exception:
            try:
                return pygame.Rect.colliderect(self.rect, ground)
            except Exception:
                return False

    def sky_collision(self):
        return bool(self.rect.y < 0)

    def pipe_collision(self, pipes):
        # pipes is expected to be an iterable of Pipe sprites
        if not pipes:
            return False
        for p in pipes:
            if pygame.Rect.colliderect(self.rect, p.rect):
                return True
        return False

    def bird_flap(self):
        if not self.flap and not self.sky_collision():
            self.flap = True
            self.vel = -7
        if self.vel >= 3:
            self.flap = False

    @staticmethod
    def closest_pipe(pipes, bird_rect):
        # Find the nearest top pipe whose right edge is ahead of the bird
        candidates = [p for p in pipes if getattr(p, 'pipe_type', None) == 'top']
        if not candidates:
            return None
        candidates.sort(key=lambda p: p.rect.x)
        for p in candidates:
            if p.rect.right > bird_rect.left:
                return p
        return candidates[0]

    def look(self, pipes):
        # Compute vision relative to the closest pipe pair
        if not pipes:
            return

        top = self.closest_pipe(pipes, self.rect)
        if top is None:
            return

        # find matching bottom pipe (same x, pipe_type == 'bottom')
        bottom = None
        for p in pipes:
            if getattr(p, 'pipe_type', None) == 'bottom' and abs(p.rect.x - top.rect.x) < 5:
                bottom = p
                break

        # Line to top pipe
        top_dist = max(0, self.rect.center[1] - top.rect.bottom)
        self.vision[0] = top_dist / 500
        try:
            pygame.draw.line(window, (255, 255, 255), self.rect.center,
                             (self.rect.center[0], top.rect.bottom))
        except Exception:
            pass

        # Line to mid pipe (horizontal distance)
        mid_dist = max(0, top.rect.x - self.rect.center[0])
        self.vision[1] = mid_dist / 500
        try:
            pygame.draw.line(window, (255, 255, 255), self.rect.center,
                             (top.rect.x, self.rect.center[1]))
        except Exception:
            pass

        # Line to bottom pipe
        if bottom is not None:
            bottom_dist = max(0, bottom.rect.top - self.rect.center[1])
        else:
            bottom_dist = max(0, (self.max_y) - self.rect.center[1])
        self.vision[2] = bottom_dist / 500
        try:
            if bottom is not None:
                pygame.draw.line(window, (255, 255, 255), self.rect.center,
                                 (self.rect.center[0], bottom.rect.top))
        except Exception:
            pass

    def think(self):
        self.decision = self.brain.feed_forward(self.vision)
        # lower threshold slightly to encourage more exploratory flaps
        if self.decision > 0.7:
            self.bird_flap()

    def calculate_fitness(self):
        # Reward both lifespan and pipes passed so evolution prioritizes pipe-passing
        # Score multiplier (50) is tunable; increase to prioritize passing pipes more strongly
        self.fitness = self.lifespan + (self.score * 50)

    def clone(self):
        clone = Bird()
        clone.fitness = self.fitness
        clone.brain = self.brain.clone()
        clone.brain.generate_net()
        return clone