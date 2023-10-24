import pygame
import setting
import bullet


class GeneralPlayer(pygame.sprite.Sprite):
    # the against player draws on right of screen
    def __init__(self, against, speed, img_name, life, lines, is_player = True):
        pygame.sprite.Sprite.__init__(self)
        self.is_player = is_player
        self.image_path = img_name
        self.is_game_over = False
        self.kills = 0
        self.point = 0
        self.life = life
        self.speed = speed
        self.lines = pygame.sprite.Group(lines)
        self.against = against
        self.image = pygame.image.load(img_name).convert()
        self.image.set_colorkey(setting.WHITE)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        if not against:
            self.rect.center = setting.start_point

    def update(self):
        if not self.against:
            if self.life <= 0:
                self.is_game_over = True
            else:
                self.key_input()

    def key_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and not pygame.sprite.spritecollide(self, self.lines, False):
            self.rect.left += self.speed
        if keys[pygame.K_LEFT] and not self.rect.left < 0:
            self.rect.left -= self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.top -= self.speed
        if keys[pygame.K_DOWN] and not self.rect.bottom > setting.end_windows_height:
            self.rect.top += self.speed




