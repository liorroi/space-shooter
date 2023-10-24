import pygame
import copy
import animaition
import bullet
import setting
import os
bullet_img = os.path.join('img', 'bullets')


class GeneralGun(pygame.sprite.Group):
    def __init__(self, x, speed, image_number, user, delay_time, dem, color_key=setting.WHITE, y=0):
        pygame.sprite.Group.__init__(self)
        self.shoot_sound = pygame.mixer.Sound('music\\shoot.mp3')

        # the bullet position x most have to contain the point for shoot to get out
        # the top point of object +it position to change the y and + position x
        image_path = os.path.join(bullet_img, str(image_number))+ '.png'
        image = pygame.image.load(image_path)
        self.bull = bullet.GeneralBullet(x, speed, image, image_path, dem, color_key = color_key, y=y)
        self.user = user
        self.game = pygame.sprite.Group()
        self.delay_time = animaition.FrameTime(delay_time)

    def shoot(self):
        # also play shoot sound
        if self.delay_time.check():
            bullet1 = bullet.GeneralBullet(self.bull.x, self.bull.speed, self.bull.image, self.bull.image_path, self.bull.dem)
            bullet1.rect.x = self.user.rect.center[0] + self.bull.x
            bullet1.rect.y = self.user.rect.center[1] + self.bull.y
            self.add(bullet1)
            self.shoot_sound.play()


class GunGroup(pygame.sprite.Group):
    def __init__(self, gun_list):
        pygame.sprite.Group.__init__(self)
        for item in gun_list:
            self.add(item)
        self.gun_list = gun_list

    def __getitem__(self, item):
        return self.gun_list[item]

    def update(self):
        for item in self.gun_list:
            item.update()

    def draw(self, screen):
        for item in self.gun_list:
            item.draw(screen)


