import pygame
import setting
import os


class GeneralBullet(pygame.sprite.Sprite):
    def __init__(self, x, speed, image_file, image_path, dem, color_key=setting.WHITE, y = 0):
        # speed contain list
        pygame.sprite.Sprite.__init__(self)
        self.image_path = image_path
        self.dem = dem
        self.x = x
        self.y = y
        self.speed = speed
        self.image = image_file
        self.image.set_colorkey(color_key)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = x, y

    def update(self):
            if self.rect.top < 0 or self.rect.bottom > setting.HEIGHT or self.rect.right < 0 or self.rect.left > setting.WIDTH:
                self.kill()
            else:
                self.rect.bottom -= self.speed[1]
                self.rect.right += self.speed[0]


