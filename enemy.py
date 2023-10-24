import pygame
import setting
import animaition
import random
import os
import protocol
import ather
import time

class GeneralRock(pygame.sprite.Sprite):
    def __init__(self, image, position, speed, middle_line, life, dem, points, image_name, color_key=setting.WHITE):
        # speed is list contain 4 thing
        # 1 x speed
        # 2 y speed
        # 3 rotation speed
        # 4 frame delay between rotate
        self.image_name = image_name
        self.image_path = setting.rocket_image_folder + '\\' + image_name
        self.dem = dem
        self.life = life
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image.set_colorkey(color_key)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = position
        self.speed = speed
        self.rotate = animaition.Rotate(self, speed[2], speed[3])
        self.middle_line = middle_line
        self.point_get = points
        self.is_finish = False

    def update(self):
        if self.life <= 0:
            self.kill()
        if self.rect.bottom > setting.end_windows_height or self.rect.right < 0 or self.rect.left > \
                setting.WIDTH or pygame.sprite.spritecollideany(self, self.middle_line):
            self.kill()
        else:
            self.rect.right += self.speed[0]
            self.rect.top += self.speed[1]
            self.rotate.rotate()

    def dump_with_frame(self, frame_time):
        speed = self.speed
        return f'{self.image_name}~{self.rect.center[0]}~{self.rect.center[1]}~{speed[0]}~' \
               f'{speed[1]}~{speed[2]}~{speed[3]}~{self.life}~{self.dem}~%.2f~{frame_time}' % self.point_get

    @ staticmethod
    def load(data):
        params = data.split('~')
        return params[:-1], params[len(params) - 1]


class EnemyGroup(pygame.sprite.Group):
    def __init__(self, middle_line=None):
        pygame.sprite.Group.__init__(self)
        self.middle_line = middle_line
        rock_images = {}
        self.directory = setting.rocket_image_folder
        names = os.listdir(self.directory)
        files_name = list(map(lambda x: self.directory + '\\' + x, names))
        for item in range(len(names)):
            rock_images[names[item]] = pygame.image.load(files_name[item])
        self.rock_images = rock_images
        self.last_deplay = 0
        self.frame = animaition.FrameTime(0)
        self.current_level = []
        self.running = False
        self.is_finish = False

    def add_rock(self, image_name, position, speed, life, dem, frame_to_wait, color_key=setting.WHITE):
        # the image name start with number always
        image = self.rock_images[image_name]
        rock = GeneralRock(image, position, speed, self.middle_line, life, dem, 35 / int(image_name[0]),
                           image_name, color_key)
        self.current_level.append([rock, frame_to_wait])
        self.is_finish = False

    def update(self):
        pygame.sprite.Group.update(self)
        if self.running:
            if not self.last_deplay == len(self.current_level):
                if self.frame.check():
                    self.add(self.current_level[self.last_deplay][0])
                    self.frame = animaition.FrameTime(self.current_level[self.last_deplay][1])
                    self.last_deplay += 1
            else:
                self.is_finish = True

    def run(self):
        self.running = True

    def stop(self):
        self.running = False

    def add_random_rocks(self, number_of_rocks, frame_to_wait, life, dem):
        for item in range(number_of_rocks):
            image = str(random.randint(1, 9)) + '.png'
            position = [random.randint(0, 500), -40]
            speed = [random.randint(-6, 6), random.randint(1, 8), random.randint(1, 8), 60]
            self.add_rock(image, position, speed, life, dem, frame_to_wait)

    def dump(self):
        data_list = []
        for item in self.current_level:
            data_list.append(item[0].dump_with_frame(item[1]))
        return '|'.join(data_list)


    @ classmethod
    def load(cls, data, middle_line):
        enemy_group = cls(middle_line)
        enemies = data.split('|')
        for rock in enemies:
            enemy_data, frame_time = GeneralRock.load(rock)
            image_name = enemy_data[0]
            speed = [float(enemy_data[3]), float(enemy_data[4]), float(enemy_data[5]), float(enemy_data[6])]
            position = [float(enemy_data[1]), float(enemy_data[2])]
            life = float(enemy_data[7])
            dem = float(enemy_data[8])
            enemy_group.add_rock(image_name, position, speed, life, dem, int(frame_time))
        return enemy_group


