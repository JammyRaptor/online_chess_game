import socket
from _thread import *
from pieces import *
import pickle
import copy

server = "192.168.0.28"

port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen(2)
print('waiting for a connection, server started')

width = 100


class ppos:
    def __init__(self):
        self.peicespos = [
            [(1 * width, 6 * width), (2 * width, 6 * width), (3 * width, 6 * width), (4 * width, 6 * width),
             (5 * width, 6 * width), (6 * width, 6 * width), (7 * width, 6 * width), (0 * width, 6 * width),
             (0 * width, 7 * width), (1 * width, 7 * width), (2 * width, 7 * width), (3 * width, 7 * width),
             (4 * width, 7 * width), (5 * width, 7 * width), (6 * width, 7 * width), (7 * width, 7 * width)],

            [(0 * width, 0 * width), (1 * width, 0 * width), (2 * width, 0 * width), (3 * width, 0 * width),
             (4 * width, 0 * width), (5 * width, 0 * width), (6 * width, 0 * width), (7 * width, 0 * width),
             (0 * width, 1 * width), (1 * width, 1 * width), (2 * width, 1 * width), (3 * width, 1 * width),
             (4 * width, 1 * width), (5 * width, 1 * width), (6 * width, 1 * width), (7 * width, 1 * width)]]

        self.oldpos = copy.deepcopy(self.peicespos)
        self.turn = 0

    def updatepos(self, pos, player):

        if pos != self.peicespos and pos != self.oldpos:

            self.oldpos = copy.deepcopy(self.peicespos)
            self.peicespos = pos

            if self.turn == 0:
                self.turn = 1
            else:
                self.turn = 0


def swap_pos(pos):
    pos1 = pos[0]
    pos2 = pos[1]
    p1 = []
    p2 = []

    for p in pos1:
        x = 700 - p[0]
        y = 700 - p[1]
        p1.append((x, y))
    for p in pos2:
        x = 700 - p[0]
        y = 700 - p[1]
        p2.append((x, y))
    pos = [p1, p2]
    return pos


def threaded_client(conn, player):
    conn.send(pickle.dumps((swap_pos(p.peicespos), player)))

    reply = ''

    while True:
        try:
            data = pickle.loads(conn.recv(2048 * 2))

            if data == 'turn':
                conn.sendall(pickle.dumps(p.turn))
            elif data == 'ready':

                if currentPlayer > 1:
                    conn.sendall(pickle.dumps(True))
                else:
                    conn.sendall(pickle.dumps(False))
            else:
                if player == 1:
                    data = swap_pos(data)
                if p.turn == player:
                    p.updatepos(data, player)

                if not data:
                    print('Dissconected')
                    break
                else:
                    if player == 1:
                        reply = swap_pos(p.peicespos)
                    else:
                        reply = p.peicespos
                    # print(f'recieved: {data}')
                    # print(f'sending: {reply}')

                conn.sendall(pickle.dumps(reply))
        except:
            break
    print('lost connection')
    conn.close()


currentPlayer = 0
p = ppos()
while True:
    conn, addr = s.accept()
    print(f'connected to: {addr}')

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
