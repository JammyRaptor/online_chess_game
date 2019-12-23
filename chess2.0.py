import pygame as pg
from pygame.locals import *
from pieces import *
from network import Network
import Colours as c
from Meta import *


class Main:
    def __init__(self):
        self.width = 800
        self.height = 800

        self.images = [[pg.image.load('assets/pawn1.png'), pg.image.load('assets/knight1.png'),
                        pg.image.load('assets/bishop1.png'), pg.image.load('assets/rook1.png'),
                        pg.image.load('assets/queen1.png'), pg.image.load('assets/king1.png')],
                       [pg.image.load('assets/pawn2.png'), pg.image.load('assets/knight2.png'),
                        pg.image.load('assets/bishop2.png'), pg.image.load('assets/rook2.png'),
                        pg.image.load('assets/queen2.png'), pg.image.load('assets/king2.png')]]

        self.clock = pg.time.Clock()

        self.background = pg.image.load('assets/board.png')
        self.background = pg.transform.scale(self.background, (self.width, self.height))

        pg.init()
        self.meta = Meta()
        self.win = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption('Chess')

    def mainloop(self):
        global peices1, peices2

        self.font = pg.font.Font('freesansbold.ttf', 50)

        text = self.font.render('Waiting for opponent . . .', True, c.BLACK, c.WHITE)

        textRect = text.get_rect()

        textRect.center = (self.width // 2, self.height // 2)

        start = n.send('ready')

        while not start:
            self.clock.tick(30)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()

            self.win.fill(c.WHITE)

            self.win.blit(text, textRect)

            start = n.send('ready')
            pg.display.update()
        run = True

        while run:

            self.meta = n.send(('turn', self.meta))

            self.clock.tick(60)

            if player == 0:
                peices = (n.send([peices1, peices2]))
                peices1 = peices[0]
                peices2 = peices[1]
            else:
                peices = (n.send([self.swap_ploc(peices1), self.swap_ploc(peices2)]))
                peices1 = self.swap_ploc(peices[0])
                peices2 = self.swap_ploc(peices[1])
            # print(peices)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    pg.quit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    self.click(pg.mouse.get_pos())
            root.redraw([], peices1, peices2)

    def redraw(self, extras, me, notme):
        self.win.blit(self.background, (0, 0))

        for extras in extras:
            extras.draw(self.win)

        for peice in notme + me:
            if peice.draw():
                # print(peice.image)
                self.win.blit(self.images[peice.type - 1][peice.image], (peice.x, peice.y))

        pg.display.update()

    def convert_loc(self, loc):
        x, y = loc
        x = x // (self.height // 8)
        y = y // (self.height // 8)
        loc = (x, y)
        return loc

    def revert_loc(self, loc):
        x, y = loc
        x = x * (self.height // 8)
        y = y * (self.height // 8)
        loc = (x, y)
        return loc

    def swap_ploc(self, pieces):
        for piece in pieces:
            piece.x = 700 - piece.x
            piece.y = 700 - piece.y
        return pieces

    def click(self, loc):
        print(self.convert_loc(loc))
        if player == 0:
            me = peices1
            notme = peices2
        else:
            me = peices2
            notme = peices1

        for i, peice in enumerate(me):
            if self.convert_loc(peice.get_location()) == self.convert_loc(loc):
                squares = peice.generate_squares(me, notme, self.convert_loc(loc))

                pg.event.get()
                c, *_ = pg.mouse.get_pressed()
                x, y = pg.mouse.get_pos()
                x = x - (x // 100) * 100
                y = y - (y // 100) * 100

                while c:
                    pg.event.get()

                    peice.x, peice.y = pg.mouse.get_pos()
                    peice.x -= x
                    peice.y -= y
                    c, *_ = pg.mouse.get_pressed()
                    self.redraw(squares, me, notme)
                peice.x, peice.y = self.revert_loc(self.convert_loc(pg.mouse.get_pos()))

                valid = False

                for square in squares:
                    if (square.x, square.y) == (peice.x, peice.y):
                        valid = True

                if not valid:
                    peice.x, peice.y = self.revert_loc(self.convert_loc(loc))
                else:
                    if peice.moved():
                        selection = self.reached_end(me)

                        if player == 1:
                            if selection == 1:
                                peices1[i] = Rook(peice.x // (self.width // 8), peice.y // (self.width // 8),
                                                  peice.type, self.width)
                            elif selection == 2:
                                peices1[i] = Bishop(peice.x // (self.width // 8), peice.y // (self.width // 8),
                                                    peice.type, self.width)
                            elif selection == 3:
                                peices1[i] = Knight(peice.x // (self.width // 8), peice.y // (self.width // 8),
                                                    peice.type, self.width)
                            elif selection == 4:
                                peices1[i] = Queen(peice.x // (self.width // 8), peice.y // (self.width // 8),
                                                   peice.type, self.width)
                        else:
                            if selection == 1:
                                peices2[i] = Rook(peice.x // (self.width // 8), peice.y // (self.width // 8),
                                                  peice.type, self.width)
                            elif selection == 2:
                                peices2[i] = Bishop(peice.x // (self.width // 8), peice.y // (self.width // 8),
                                                    peice.type, self.width)
                            elif selection == 3:
                                peices2[i] = Knight(peice.x // (self.width // 8), peice.y // (self.width // 8),
                                                    peice.type, self.width)
                            elif selection == 4:
                                peices2[i] = Queen(peice.x // (self.width // 8), peice.y // (self.width // 8),
                                                   peice.type, self.width)

                    for p in notme:
                        if p.x == peice.x and p.y == peice.y:
                            p.take()

    def reached_end(self, me):

        r = pg.image.load(f'assets/rook{me[0].type}.png')
        r = pg.transform.scale(r, (self.width // 8, self.width // 8))
        b = pg.image.load(f'assets/bishop{me[0].type}.png')
        b = pg.transform.scale(b, (self.width // 8, self.width // 8))
        k = pg.image.load(f'assets/knight{me[0].type}.png')
        k = pg.transform.scale(k, (self.width // 8, self.width // 8))
        q = pg.image.load(f'assets/queen{me[0].type}.png')
        q = pg.transform.scale(q, (self.width // 8, self.width // 8))

        text = self.font.render('Select Promotion', True, c.BLACK)
        textRect = text.get_rect()
        textRect.center = (self.width // 2, self.height // 5)

        while True:
            self.clock.tick(30)

            self.win.blit(self.background, (0, 0))

            self.win.blit(text, textRect)

            self.win.blit(r, self.revert_loc((2, 3)))
            self.win.blit(b, self.revert_loc((5, 3)))
            self.win.blit(k, self.revert_loc((2, 6)))
            self.win.blit(q, self.revert_loc((5, 6)))

            pg.display.update()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    loc = pg.mouse.get_pos()
                    loc = self.convert_loc(loc)

                    if loc == (2, 3):
                        return 1
                    elif loc == (5, 3):
                        return 2
                    elif loc == (2, 6):
                        return 3
                    elif loc == (5, 6):
                        return 4


if __name__ == '__main__':
    root = Main()
    n = Network()
    width = 800

    peices, player = n.getP()
    print(player)
    peices1 = peices[0]
    peices2 = peices[1]
    print(peices)
    print(peices1)
    print(peices2)
    root.mainloop()
