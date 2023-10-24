import socket
import protocol
import threading
import enemy

udp_addr = (protocol.server_ip, protocol.udp_port)
tcp_socket = socket.socket()
tcp_socket.bind((protocol.server_ip, protocol.tcp_port))
udp_socket = socket.socket(type=socket.SOCK_DGRAM)
udp_socket.bind(('0.0.0.0', 12345))
enemy_life = 100
enemy_dem = 25
waiting_list = []
# waiting list locked
waiting_list_lock = threading.Lock()
players_data = {}
players_data_lock = threading.Lock()
players_level = {}
player_level_lock = threading.Lock()
players_sock = {}
player_sock_lock = threading.Lock()
running = True


def send_win(sock):
    sock.send(b'WINS')


def send_level(enemy_group_dump, sock):
    protocol.send_object(sock, 'LEVL', enemy_group_dump)


def create_enemies(level):
    frame_time = 100 - level
    number_of_enemies = level * 100
    enem = enemy.EnemyGroup()
    enem.add_random_rocks(number_of_enemies, frame_time, enemy_life, enemy_dem)
    return enem.dump()


def create_game_id():
    num = 0
    while True:
        yield str(num).zfill(4)
        if num >= 9999:
            num = 0
        else:
            num += 1


id_generator = create_game_id()


def one_client(sock):
    try:
        while True:
            kind = protocol.get_kind(sock)
            if kind == b'PLAY':
                waiting_list_lock.acquire()
                waiting_list.append(sock)
                print(waiting_list)
                waiting_list_lock.release()

            elif kind == b'LOSE':
                identify = protocol.get_part(sock, 4).decode()
                player_num = int(protocol.get_part(sock, 1).decode())
                player_sock_lock.acquire()

                if player_num == 0:
                    player_num = 1
                elif player_num == 1:
                    player_num = 0
                else:
                    print('the player num is not valid ')
                sock_1 = players_sock[identify][player_num]
                protocol.send(sock_1, b'WINS')
                player_sock_lock.release()

            elif kind == b'LEVL':
                game_id = protocol.get_part(sock, 4).decode()
                level_number_byte = protocol.get_part(sock, 3)
                level_number = int(level_number_byte)
                if game_id in players_level:
                    player_level_lock.acquire()
                    dic = players_level[game_id]
                    if level_number in dic:
                        send_level(dic[level_number], sock)

                    else:
                        enemies = create_enemies(level_number)
                        dic[level_number] = enemies
                        send_level(enemies, sock)
                    player_level_lock.release()
                else:
                    # send error that ask the player to send again the level
                    print('error')

            elif kind == b'STOP':
                protocol.send(sock, b'STOP')

            elif kind == b'':
                break

    except:
        print('error')

def send_id(sock, identify, num):
    protocol.send(sock, b'YOID' + identify.encode() + num.encode())


def start_game(sock1, sock2):
    identify = next(id_generator)

    send_id(sock1, identify, '0')
    send_id(sock2, identify, '1')

    players_data_lock.acquire()
    players_data[identify] = [b'', b'']
    players_data_lock.release()

    player_level_lock.acquire()
    players_level[identify] = {}
    player_level_lock.release()

    player_sock_lock.acquire()
    players_sock[identify] = (sock1, sock2)
    player_sock_lock.release()


def start_games():
    while running:
        waiting_list_lock.acquire()
        if len(waiting_list) >= 2:
            start_game(waiting_list[0], waiting_list[1])
            del(waiting_list[0])
            del(waiting_list[0])
        waiting_list_lock.release()


def udp(sock=udp_socket):
    while True:
        try:
            kind, message, addr = protocol.recv_udp(sock)
            if kind == b'INFO':
                identify = message[:4].decode()
                message = message[4:]
                player_id = int(message[:1])
                message = message[1:]
                players_data_lock.acquire()
                dic = players_data[identify]
                dic[player_id] = message
                players_data_lock.release()
                # sent back the opponent state
                if player_id == 0:
                    player_id = 1

                elif player_id == 1:
                    player_id = 0
                players_data_lock.acquire()
                data = dic[player_id]
                if data == b'':
                    data = b'stop'
                protocol.send_udp(data, addr, sock, 'INFO')
                players_data_lock.release()

        except:
            print('error')

def main():
    tcp_socket.listen()
    # this function start games
    threading.Thread(target=start_games, args=()).start()
    # this function treat udp message
    threading.Thread(target=udp, args=()).start()
    while True:
        client_sock, ip = tcp_socket.accept()
        threading.Thread(target=one_client, args=(client_sock,)).start()


if __name__ == '__main__':
    main()
