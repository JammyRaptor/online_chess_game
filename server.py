import socket
from _thread import *
from pieces import *
import pickle
import copy
from Meta import *

server = "192.168.0.87"

port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen(2)
print('waiting for a connection, server started')

key = {1: 'pawn', 2: 'knight', 3: 'bishop', 4: 'rook', 5: 'queen', 6: 'king'}


class ppos:
    def __init__(self):
        width = 800
        self.pieces = [

            [Pawn(1, 6, 1, width), Pawn(2, 6, 1, width),
             Pawn(3, 6, 1, width),
             Pawn(4, 6, 1, width), Pawn(5, 6, 1, width),
             Pawn(6, 6, 1, width),
             Pawn(7, 6, 1, width), Pawn(0, 6, 1, width),
             Rook(0, 7, 1, width),
             Knight(1, 7, 1, width), Bishop(2, 7, 1, width),
             Queen(3, 7, 1, width),
             King(4, 7, 1, width), Bishop(5, 7, 1, width),
             Knight(6, 7, 1, width),
             Rook(7, 7, 1, width)],

            [Rook(0, 0, 2, width), Knight(1, 0, 2, width),
             Bishop(2, 0, 2, width),
             Queen(3, 0, 2, width), King(4, 0, 2, width),
             Bishop(5, 0, 2, width),
             Knight(6, 0, 2, width), Rook(7, 0, 2, width),
             Pawn(0, 1, 2, width),
             Pawn(1, 1, 2, width), Pawn(2, 1, 2, width),
             Pawn(3, 1, 2, width),
             Pawn(4, 1, 2, width), Pawn(5, 1, 2, width),
             Pawn(6, 1, 2, width),
             Pawn(7, 1, 2, width)]]
        self.oldpos = copy.deepcopy(self.pieces)

    def promote(self, promotiondata):
        player, position, promotion = promotiondata
        self.pieces[player][position] = promotion


    def updatepos(self, pieces, player):
        self.pieces = pieces

        # if pieces != self.pieces and pieces != self.oldpos:
        #   print(f'swapped {player}')
        #  self.oldpos = copy.deepcopy(self.pieces)
        # self.pieces = pieces

        # if self.turn == 0:
        #     self.turn = 1
        # else:
        #     self.turn = 0


def threaded_client(conn, player):
    global meta
    meta.connectedplayers[player] = True
    conn.send(pickle.dumps((meta, p.pieces, player)))

    # reply = ''

    while True:
        try:
            data = pickle.loads(conn.recv(2048 * 3))

            if data == 'ready':

                if meta.connectedplayers[0] and  meta.connectedplayers[1]:
                    conn.sendall(pickle.dumps(True))
                else:
                    conn.sendall(pickle.dumps(False))
            else:
                newmeta, positions = data

                if newmeta.peicemoved:

                    meta = newmeta
                    meta.peicemoved = False
                    meta.swapturn()
                    p.updatepos(positions, player)
                    if meta.premote:
                        p.promote(meta.premotedata)
                        meta.premote = False

                if not data:
                    print('Dissconected')
                    break
                else:
                    conn.sendall(pickle.dumps((meta, p.pieces)))

                    # print(f'recieved: {data}')
                    # print(f'sending: {reply}')


        except:
            break
    print('lost connection')
    conn.close()
    meta.connectedplayers[player] = False
    if not meta.connectedplayers[0] and not meta.connectedplayers[1]:
        p.__init__()
        meta.__init__()
        print('game reset')
currentPlayer = 0
meta = Meta()
p = ppos()
while True:
    conn, addr = s.accept()
    print(f'connected to: {addr}')
    if not meta.connectedplayers[0]:
        start_new_thread(threaded_client, (conn, 0))
    elif not meta.connectedplayers[1]:
        start_new_thread(threaded_client, (conn, 1))
    currentPlayer += 1
