import pygame
import setting
import os


class FrameTime:
    # this function make function happen every number of frame
    def __init__(self, frame_delay):
        self.frame_delay = frame_delay
        self.last_time = pygame.time.get_ticks()

    def check(self):
        now_frame = pygame.time.get_ticks()
        if now_frame - self.last_time >= self.frame_delay:
            self.last_time = now_frame
            return True
        return False

    def reset(self):
        self.last_time = pygame.time.get_ticks()

    def reset_all(self, frame_delay):
        self.last_time = pygame.time.get_ticks()
        self.frame_delay = frame_delay


class Rotate:
    def __init__(self, obj, speed, delay_time):
        self.delay = FrameTime(delay_time)
        self.obj = obj
        self.speed = speed
        self.image = obj.image.copy()
        self.degrees = 0

    def rotate(self):
        if self.delay.check():
            self.degrees += self.speed
            self.obj.image = pygame.transform.rotate(self.image, self.degrees)


class GeneralAnimation(pygame.sprite.Sprite):
    def __init__(self, image_list, path_list_image, frame_between_picture, position, color_key=setting.BLACK):
        pygame.sprite.Sprite.__init__(self)
        self.path_list_image = path_list_image
        self.image_list = image_list
        self.frame = FrameTime(frame_between_picture)
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        self.image.set_colorkey(color_key)
        self.position = position
        self.rect.center = position
        self.current_index = 0
        self.image_path = path_list_image[self.current_index]

    def update(self):
        if self.frame.check():
            if self.current_index + 1 < len(self.image_list) - 1:
                self.current_index += 1
                self.image = self.image_list[self.current_index]
                self.image_path = self.path_list_image[self.current_index]
                self.rect = self.image.get_rect()
                self.rect.center = self.position
            else:
                self.kill()


class GroupAnimation(pygame.sprite.Group):

    def __init__(self):
        self.explosion_sound = pygame.mixer.Sound('music\\explosion.wav')
        pygame.sprite.Group.__init__(self)
        self.bomb_image_list = []
        directory = setting.explusion_images
        names = os.listdir(directory)
        files_name = list(map(lambda x: directory + '\\' + x, names))
        self.files_path = files_name
        for item in files_name:
            self.bomb_image_list.append(pygame.image.load(item))
        for item in range(len(self.bomb_image_list)):
            self.bomb_image_list[item] = pygame.transform.scale(self.bomb_image_list[item] , setting.bomb_images_size)

    # this also play a sound
    def add_bomb(self, position):
        self.add(GeneralAnimation(self.bomb_image_list, self.files_path, setting.bomb_frame, position))
        self.explosion_sound.play()