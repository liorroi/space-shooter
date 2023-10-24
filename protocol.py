import pickle
import struct
import socket
import pygame
import setting
import enemy
import ather
tcp_port = 1234
udp_port = 12345
server_ip = '10.0.0.9'
client_ip = socket.gethostbyname(socket.gethostname())
is_debug = True


def send(sock, data):
    sock.send(data)
    if is_debug:
        print(b'the data sent>>>' + data)


def get(sock, size):
    data = sock.recv(size)
    if is_debug:
        print(b'data is get>>>' + data)
    return data


def send_object(sock, kind, data):
    byte_size = number_to_send(len(data))
    data = kind.encode() + byte_size + data.encode()
    send(sock, data)


def get_part(sock, size):
    siz = size
    data = b''
    while len(data) < siz:
        data += get(sock, siz - len(data))
        if data == b'':
            break
    return data


def get_kind(sock):
    return get_part(sock, 4)


def get_obj(sock):
    # this function call when we know that its game object
    size = get_number(get_part(sock, 4))
    data = get_part(sock, size)
    return data.decode()


def number_to_send(num):
    num_big_india = socket.htonl(num)
    num_bytes = struct.pack('I', num_big_india)
    return num_bytes


def get_number(byte):
    num_big_india = struct.unpack('I', byte)[0]
    num = socket.ntohl(num_big_india)
    return num


class Opponent(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
        self.images = {}

    def add_load(self, params):
        if params[0] in self.images:
            imag = self.images[params[0]]
        else:
            imag = pygame.image.load(params[0])
            self.images[params[0]] = imag
        center_point = (float(params[1]), float(params[2]))
        if 'explosion' in params[0]:
            imag = pygame.transform.scale(imag, setting.bomb_images_size)
        self.add(SimpleSprite(imag, center_point))

    def loads(self, data):
        self.empty()
        sprites = loads(data)
        sprites = Opponent.convert(sprites)
        for item in sprites:
            self.add_load(item)

    @ staticmethod
    def convert(data_list):
        """
        this function convert the sprute position from left to right
        """
        add = (setting.WIDTH - setting.middle_line_width) / 2 + setting.middle_line_width
        for item in data_list:
            item[1] = int(item[1])
            item[1] += add
            item[1] = str(item[1])
        return data_list


class SimpleSprite(pygame.sprite.Sprite):
    def __init__(self, imag, center_point, color_key=setting.WHITE):
        pygame.sprite.Sprite.__init__(self)
        self.image = imag
        self.image.set_colorkey(color_key)
        self.rect = self.image.get_rect()
        self.rect.center = center_point


def dump(obj):
    image_path = obj.image_path
    position = obj.rect.center
    position_x = obj.rect.center[0]
    position_y = obj.rect.center[1]
    return f'{image_path}~{position_x}~{position_y}'.encode()


def load(data):
    params = data.split('~')
    return params


def dumps(obj_list):
    # it used to send player state
    return b'|'.join(map(dump, obj_list))


def loads(data):
    # retuen list contain list that contain 3 stuff (image_path, position_x , position_y)
    # it used to load the player state after sending
    data = data.decode()
    sprites_list = []
    sprites = data.split('|')
    for item in sprites:
        sprites_list.append(load(item))
    return sprites_list


def send_udp(data, addr, sock, kind):
    message = kind.encode() + data
    if is_debug:
        print('udp sent >>>' + message.decode())
    sock.sendto(message, addr)


def recv_udp(sock):
    message, addr = sock.recvfrom(1024)
    kind = message[:4]
    message = message[4:]
    if is_debug:
        print('udp get >>>' + kind.decode(), message.decode(), addr)
    return kind, message, addr

