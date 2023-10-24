import button
import pygame
import setting
import ather
import animaition


class StartGame(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        self.start_text = ather.PrintTextSprite(60, 'press play to start the game ', setting.WHITE)
        self.start_text.rect.center = (setting.play_button_position[0], setting.play_button_position[0] - 400)
        self.start_button = button.Button(button.text_surface(setting.play_button_letter_size, 'play', setting.start_game_letter_color))
        self.start_button.rect.center = setting.play_button_position
        self.add(self.start_button)
        self.add(self.start_text)

    def check_click(self, mouse_position):
        # 1 is the play button
        if self.start_button.check_mouse_position_in_button_rect(mouse_position):
            return 1


class GameOver(pygame.sprite.Group):
    def __init__(self, player, is_win):
        pygame.sprite.Group.__init__(self)
        self.is_win = is_win
        self.player = player
        self.text = ather.PrintTextSprite(60, 'you win, your score is %.2f' % self.player.point, setting.WHITE)
        self.start_button = button.Button(button.text_surface(setting.play_button_letter_size, 'play again', setting.start_game_letter_color))
        self.start_button.rect.center = setting.play_button_position
        self.add(self.start_button)

    def check_click(self, mouse_position):
        # 1 is the play button
        if self.start_button.check_mouse_position_in_button_rect(mouse_position):
            print('cliced')
            return 1

    def draw(self, screen):
        self.text.kill()
        if self.is_win:
            self.text = ather.PrintTextSprite(60, 'you win, your score is %.2f' % self.player.point, setting.WHITE)
        else:
            self.text = ather.PrintTextSprite(60, 'you lose, your score is %.2f' % self.player.point, setting.WHITE)
        self.text.rect.center = (setting.play_button_position[0], setting.play_button_position[0] - 400)
        self.add(self.text)
        pygame.sprite.Group.draw(self, screen)


class WaitingForAnotherPlayer(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        self.text = ather.PrintTextSprite(100, 'waiting for another player.', setting.WHITE, 'arial')
        self.text.rect.center = (500, 200)
        self.add(self.text)



