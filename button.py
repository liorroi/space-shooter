import pygame
import setting


class Button(pygame.sprite.Sprite):
    def __init__(self, image, image_to_change=None,color_key=setting.WHITE):
        pygame.sprite.Sprite.__init__(self)
        self.is_change = True
        if image_to_change is None:
            self.is_change = False
        self.original_image = image
        self.image = image
        self.rect = self.image.get_rect()
        self.image_to_change = image_to_change

    def check_mouse_position_in_button_rect(self, mouse_point):
        if self.rect.collidepoint(mouse_point):
            return True
        return False

    def image_press(self):
        if self.is_change:
            center_point = self.rect.center
            self.image = self.image_to_change
            self.rect = self.image.get_rect()
            self.rect.center = center_point

    def set_original_image(self):
        center_point = self.rect.center
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = center_point


class CreateBackground(pygame.sprite.Sprite):
    def __init__(self, size, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()


class ButtonList(pygame.sprite.Group):
    def __init__(self, buttons, player, level):
        self.information = InformationGroup(player, level)
        self.all_button = []
        self.button_press = 0
        back_ground = CreateBackground((setting.WIDTH, 3 * setting.button_size[1] + 1), setting.back_ground_button_color)
        back_ground.rect.bottomright = (setting.WIDTH, setting.HEIGHT)
        # buttons is list contain all button image
        pygame.sprite.Group.__init__(self)
        self.add(back_ground)
        battom = setting.HEIGHT
        for item in buttons:
            position = (0, 0)
            color_key = setting.WHITE
            item.rect.bottomleft = (0, battom)
            battom -= setting.button_size[1] - 1
            self.all_button.append(item)
            self.add(item)

    def update(self):
        pygame.sprite.Group.update(self)
        if pygame.mouse.get_pressed(3)[0]:
            for item in self.all_button:
                if item.check_mouse_position_in_button_rect(pygame.mouse.get_pos()):
                    self.all_button[self.button_press].set_original_image()
                    self.button_press = self.all_button.index(item)
        self.all_button[self.button_press].image_press()
        self.information.update()

    def draw(self, screen):
        pygame.sprite.Group.draw(self, screen)
        if self.button_press == 0:
            self.information.draw(screen)


def text_surface(size, text, letter_color, background = None, font='arial'):
    font = pygame.font.match_font(font)
    font_obj = pygame.font.Font(font, size)
    text = font_obj.render(text, True, letter_color, background)
    return text


def create_buttons(player, level):
    size = setting.text_size
    font = setting.font
    b1 = Button(text_surface(size, 'tower', setting.letter_color, setting.back_ground_button_color),
                text_surface(size, 'tower', setting.letter_click_color, setting.back_ground_click_color))
    b2 = Button(text_surface(size, 'attack', setting.letter_color, setting.back_ground_button_color),
                text_surface(size, 'attack', setting.letter_click_color, setting.back_ground_click_color))
    b3 = Button(text_surface(size, 'information', setting.letter_color, setting.back_ground_button_color),
                text_surface(size, 'information', setting.letter_click_color, setting.back_ground_click_color))
    button_list = [b3, b2, b1]
    return ButtonList(button_list, player, level)


class InformationPart(pygame.sprite.Sprite):
    def __init__(self, player, position, text):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.player = player
        self.position = position
        self.image = text_surface(setting.letter_size, text, setting.information_color)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.position

    def update(self):
        self.image = text_surface(setting.letter_size, self.text, setting.letter_color)
        self.rect = self.image.get_rect()
        self.rect.center = self.position


class InformationGroup(pygame.sprite.Group):
    def __init__(self, player, level):
        pygame.sprite.Group.__init__(self)
        self.player = player
        self.level = level

    def update(self):
        self.empty()
        y = setting.start_information_position[1]
        score = InformationPart(self.player, (setting.start_information_position[0], y), 'Score %.2f' % self.player.point)
        life = InformationPart(self.player, (score.rect.right + setting.space_between_items, y), f'Life {self.player.life}')
        kills = InformationPart(self.player, (life.rect.right + setting.space_between_items, y), f'kills {self.player.kills}')
        level = InformationPart(self.player, (kills.rect.right + setting.space_between_items, y), f'level {self.level.level}')
        self.add(score)
        self.add(life)
        self.add(kills)
        self.add(level)
