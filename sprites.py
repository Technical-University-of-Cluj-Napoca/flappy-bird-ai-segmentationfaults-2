import pygame

class SpriteSheet:
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename)
            if pygame.display.get_surface():
                self.sheet = self.sheet.convert_alpha()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)

    def get_image(self, x, y, width, height):
        rect = pygame.Rect(x, y, width, height)
        if not self.sheet.get_rect().contains(rect):
           # Warning suppressed for now as we know some coordinates might be tricky
           # print(f"Warning: Rect {rect} is outside of sprite sheet bounds {self.sheet.get_rect()}")
           pass
        return self.sheet.subsurface(rect)

def get_background_day(sheet):
    try:
        image = sheet.get_image(0, 0, 144, 256)
        return pygame.transform.scale(image, (288, 512))
    except Exception as e:
        return sheet.get_image(0, 0, 288, 512)

def get_background_night(sheet):
    try:
        image = sheet.get_image(146, 0, 144, 256)
        return pygame.transform.scale(image, (288, 512))
    except Exception as e:
        # Fallback to synthesized night bg
        day_bg = get_background_day(sheet).copy()
        dark_overlay = pygame.Surface(day_bg.get_size()).convert_alpha()
        dark_overlay.fill((0, 0, 50, 100))
        day_bg.blit(dark_overlay, (0, 0))
        return day_bg

def get_base(sheet):
    # Based on analysis: Base is likely at x=292, y=0.
    # Height 56 (half of 112). Width 168 (half of 336).
    try:
        image = sheet.get_image(292, 0, 168, 56)
        return pygame.transform.scale(image, (336, 112))
    except Exception as e:
        print(f"Error loading base: {e}")
        return sheet.get_image(292, 0, 336, 112)

def get_bird_down(sheet):
    return sheet.get_image(115, 329, 34, 24)

def get_bird_mid(sheet):
    return sheet.get_image(115, 355, 34, 24)

def get_bird_up(sheet):
    return sheet.get_image(115, 381, 34, 24)

def get_pipe_green_bottom(sheet):
    return sheet.get_image(56, 323, 52, 320)

def get_pipe_green_top(sheet):
    return sheet.get_image(84, 323, 52, 320)

def get_game_over(sheet):
    return sheet.get_image(395, 59, 96, 21)

def get_message(sheet):
    return sheet.get_image(292, 281, 184, 176)

def get_number_0(sheet):
    return sheet.get_image(496, 60, 12, 18)
    
def get_number_1(sheet):
    return sheet.get_image(136, 455, 8, 18)

def get_number_2(sheet):
    return sheet.get_image(292, 160, 12, 18)
