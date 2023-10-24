import socket
import protocol
import enemy
import os
import threading
import pygame

udp_addr = ('10.0.0.9', protocol.udp_port)
is_running = True

def send_play(sock):
    protocol.send(sock, b'PLAY')


def get_id(sock):
    is_ret = True
    a = protocol.get_part(sock, 4)
    while not a == b'YOID':
        a = protocol.get_part(sock, 4)
    if is_ret:
        return protocol.get_part(sock, 4),  protocol.get_part(sock, 1)


class ClientMsg:
    def __init__(self, enemy_group, client_tcp_sock, opponent_group, level):
        global is_running
        is_running = True
        self.level = level
        self.opponent_group = opponent_group
        self.is_quit = False
        self.enemy_group = enemy_group
        self.middle_line = self.enemy_group.middle_line
        self.is_win = False
        self.level_number = 1
        self.tcp_sock = client_tcp_sock
        self.udp_sock = socket.socket(type=socket.SOCK_DGRAM)
        send_play(self.tcp_sock)
        data = get_id(self.tcp_sock)
        if data is None:
            self.is_quit = True
        if not self.is_quit:
            self.identify, self.num = data
            self.can_ask = True
            self.ask_level()

    def ask_level(self, level_number = None):
        if self.can_ask:
            if level_number is None:
                level_number = self.level_number
            protocol.send(self.tcp_sock, b'LEVL' + self.identify + str(level_number).encode().zfill(3))
            self.level_number += 1
            self.enemy_group.is_finish = False
            self.can_ask = False

    def get_and_treat_msg_tcp(self):
        global is_running
        # in this part on tcp thare are 2 message 1 you win second level
        # if player get message of winning the get_win become True
        while is_running:
            kind = protocol.get_kind(self.tcp_sock)
            if kind == b'LEVL':
                data = protocol.get_obj(self.tcp_sock)
                a = enemy.EnemyGroup.load(data, self.middle_line)
                self.enemy_group.current_level = a.current_level
                self.enemy_group.run()
                self.can_ask = True
                self.level.level_got()

            elif kind == b'WINS':
                self.is_win = True
                is_running = False

    def lose(self):
        global is_running
        is_running = False
        protocol.send(self.tcp_sock, b'LOSE' + self.identify + self.num)
        protocol.send(self.tcp_sock, b'STOP')

    def stop(self):
        global is_running
        is_running = False
        protocol.send(self.tcp_sock, b'STOP')

    def win(self):
        global is_running
        is_running = False

    def send_get_state_udp(self, obj_list):
        kind = 'INFO'
        identify = self.identify
        player_byte = self.num
        data = protocol.dumps(obj_list)
        data = identify + player_byte + data
        protocol.send_udp(data, udp_addr, self.udp_sock, kind)
        # here the client get data from server about opponent info

        kind, data, addr = protocol.recv_udp(self.udp_sock)
        if kind == b'INFO':
            if not data == b'stop':
                print(data)
                self.opponent_group.loads(data)

