# Pygame template - skeleton for a new pygame project
# art from kenny.nl
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>
import pygame
import ather
import setting
import player
import enemy
import gun
import animaition
import button
import game_windows
import protocol
import client_intertnet
import threading
import socket
import sys
import os

running_main_loop = True


class Game:
    def __init__(self, gun_group=None, back_ground_image=None, middle_line=None, screen=None, pla=None, is_game=True, tcp_sock=None):
        # load sounds
        self.is_game_over = False
        self.sending_thread = threading.Thread()
        if is_game:
            self.level = ather.LevelNumber()
            self.pla = pla
            all_sprites = pygame.sprite.Group()
            all_sprites.add(pla)
            limited_line = pygame.sprite.Group(middle_line)
            self.clock = pygame.time.Clock()
            self.group_list = []
            self.current_level = []

            for item in range(8):
                self.group_list.append(pygame.sprite.Group())

            self.running = True
            self.screen = screen
            self[0] = all_sprites
            self[1] = limited_line
            self[3] = protocol.Opponent()
            self[2] = gun_group
            self[4] = enemy.EnemyGroup(self[1])
            self[5] = animaition.GroupAnimation()
            self[6] = button.create_buttons(self.pla, self.level)
            # place 0 contain the player
            # place 1 middle_line
            # place 2 gun group of player
            # place 3 all shape of opponent
            # place 4 enemy_shape
            # place 5 animations group
            # place 6 button_group
            self.msg = client_intertnet.ClientMsg(self[4], tcp_sock, self[3], self.level)
            # image list image and thar here rect
            background_image = pygame.image.load(back_ground_image).convert()
            self.back_ground = [background_image, background_image.get_rect()]
            # place 0 background image
            # place 1 rock image
            self.current_gun = gun_group[0]
            # place 0 background image
            # gun list
            self.gun_list = gun_group


    def __getitem__(self, item):
        return self.group_list[item]

    def __setitem__(self, key, value):
        self.group_list[key] = value

    def events(self):
        global running_main_loop
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                running_main_loop = False
                self.msg.lose()

    def draw(self):
        if self.running:
            self.keys()
            for item in self:
                item.update()
            self.screen.blit(self.back_ground[0], self.back_ground[1])
            for item in self:
                item.draw(self.screen)
            pygame.display.flip()
        # *after* drawing everything, flip the display

    def keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.current_gun.shoot()

    def check_colision(self):
        enem = self[4]
        # check if bullet get touch with enemy
        for bullets in self[2].gun_list:
            for bull in bullets:
                mob_hits = pygame.sprite.spritecollide(bull, enem, False, pygame.sprite.collide_mask)
                if mob_hits:
                    bull.kill()
                for item in mob_hits:
                    if type(item) == enemy.GeneralRock:
                        item.life -= bull.dem
                        # add player th score and kills
                        if item.life <= 0:
                            self.pla.point += item.point_get
                            self.pla.kills += 1
                            self[5].add_bomb(item.rect.center)
        # check if enemy get touch with player
        mob_hits = pygame.sprite.spritecollide(self.pla, enem, True, pygame.sprite.collide_mask)
        for item in mob_hits:
            self.pla.life -= item.dem
            self[5].add_bomb(self.pla.rect.center)

    def level_end(self):
        if self[4].is_finish:
            self.level.next_level()
            # send that the level end
            self.msg.ask_level()

    def check_if_game_over(self):
        if self.pla.is_game_over or self.msg.is_quit:
            self.is_game_over = True
            self.running = False
            self.msg.lose()

        elif self.msg.is_win:
            self.is_game_over = True
            self.running = False
            self.msg.win()

    def run(self):
        # Game loop
        threading.Thread(target=self.msg.get_and_treat_msg_tcp, args=()).start()
        while self.running:
            # keep loop running at the right speed
            self.clock.tick(setting.FPS)
            # Process input (events)
            self.events()
            # Draw / render
            self.draw()
            # check colision
            self.check_colision()
            # check if level end
            self.level_end()
            # check if game over
            self.check_if_game_over()
            # send state
            if not self.sending_thread.is_alive():
                self.sending_thread = threading.Thread(target=self.send_state, args=())
                self.sending_thread.start()

    def send_state(self):
        obj = [self.pla]
        for gunn in self[2].gun_list:
            for bullet in gunn:
                obj.append(bullet)
        for group_number in range(4, 6):
            for item in self[group_number]:
                obj.append(item)
        self.msg.send_get_state_udp(obj)


def create_game(screen, limit_line, pla, tcp_sock):
    gun_list = gun.GunGroup([gun.GeneralGun(-5, [0, 10], 1, pla, setting.shoot_delay, 50, y=-20)])
    client_intertnet.is_run = True
    game = Game(gun_list, 'img\\backgrounds\\1.png', limit_line, screen, pla, tcp_sock=tcp_sock)
    game.run()
    return game


def main():
    global running_main_loop
    pygame.init()
    pygame.mixer.init()
    # load an play background sound
    pygame.mixer.music.load('music\\tgfcoder-FrozenJam-SeamlessLoop.ogg')
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.4)
    screen = pygame.display.set_mode((setting.WIDTH, setting.HEIGHT))
    # create player and middle_line
    limt_line = ather.MiddleLine()
    pla = player.GeneralPlayer(False, 5, 'img\\players\\1.png', 100, lines=limt_line)
    pygame.display.set_caption("My Game")
    start_windows = game_windows.StartGame()
    game_over = game_windows.GameOver(pla, False)
    windows_show = start_windows
    back_ground_image = pygame.image.load('img\\backgrounds\\2.png')
    client_tcp_socket = socket.socket()
    client_tcp_socket.connect((protocol.server_ip, 1234))
    while running_main_loop:
        game = Game(is_game=False)
        screen.blit(back_ground_image, back_ground_image.get_rect())
        windows_show.update()
        windows_show.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_main_loop = False
                client_intertnet.is_run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if windows_show.check_click(pygame.mouse.get_pos()) == 1:
                    # send ask to start game
                    pla = player.GeneralPlayer(False, 5, 'img\\players\\1.png', 100, lines=limt_line)
                    client_tcp_socket = socket.socket()
                    client_tcp_socket.connect((protocol.server_ip, protocol.tcp_port))
                    wait_windows = game_windows.WaitingForAnotherPlayer()
                    screen.blit(back_ground_image, back_ground_image.get_rect())
                    wait_windows.draw(screen)
                    pygame.display.flip()
                    windows_show = wait_windows
                    game = create_game(screen, limt_line, pla, client_tcp_socket)
                    game_over.player = pla
                if game.is_game_over:
                    game_over.is_win = game.msg.is_win
                    windows_show.draw(screen)
                    windows_show = game_over
        if running_main_loop:
            pygame.display.flip()
        # check if game over


if __name__ == '__main__':
    main()
