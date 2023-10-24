import pygame
import setting
import button


class MiddleLine(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((setting.middle_line_width, setting.end_windows_height + 100))
        self.image.fill(setting.middle_line_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = ((setting.WIDTH - setting.middle_line_width) / 2 , -100)


class LevelNumber:
    def __init__(self):
        self.level = 0
        self.can_add = True

    def next_level(self):
        if self.can_add:
            self.level += 1
            self.can_add = False

    def level_got(self):
        self.can_add = True


class PrintTextSprite(pygame.sprite.Sprite):
    def __init__(self, size, text, letter_color, font='arial'):
        pygame.sprite.Sprite.__init__(self)
        self.image = button.text_surface(size, text, letter_color, font=font)
        self.rect = self.image.get_rect()
