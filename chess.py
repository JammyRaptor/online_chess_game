import pygame as pg
from pygame.locals import *
from pieces import *
from network import Network
import Colours as c
from Meta import *


class Main:
    def __init__(self):
        scale = 600
        self.width = scale
        self.height = scale

        self.clock = pg.time.Clock()

        self.resize_assets()

        pg.init()
        self.meta = Meta()
        self.win = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption('Chess')

    def resize_assets(self):
        self.images = [[pg.image.load('assets/pawn1.png'), pg.image.load('assets/knight1.png'),
                        pg.image.load('assets/bishop1.png'), pg.image.load('assets/rook1.png'),
                        pg.image.load('assets/queen1.png'), pg.image.load('assets/king1.png')],
                       [pg.image.load('assets/pawn2.png'), pg.image.load('assets/knight2.png'),
                        pg.image.load('assets/bishop2.png'), pg.image.load('assets/rook2.png'),
                        pg.image.load('assets/queen2.png'), pg.image.load('assets/king2.png')]]
        self.background = pg.image.load('assets/board.png')
        self.menu_background = pg.image.load('assets/menu.png')
        self.settings_background = pg.image.load('assets/setings_background.png')
        self.small_button = pg.image.load('assets/small_button.png')
        self.medium_button = pg.image.load('assets/medium_button.png')
        self.large_button = pg.image.load('assets/large_button.png')
        self.back_button = pg.image.load('assets/back_button.png')
        self.play_button = pg.image.load('assets/play_button.png')
        self.settings_button = pg.image.load('assets/settings_button.png')
        self.exit_button = pg.image.load('assets/exit_button.png')
        self.connecting_screen = pg.image.load('assets/connecting_screen.png')
        self.waiting_screen = pg.image.load('assets/waiting.png')
        for i, image in enumerate(self.images[0]):
            self.images[0][i] = pg.transform.scale(image, (self.width // 8, self.height // 8))
        for i, image in enumerate(self.images[1]):
            self.images[1][i] = pg.transform.scale(image, (self.width // 8, self.height // 8))
        self.background = pg.transform.scale(self.background, (self.width, self.height))
        self.menu_background = pg.transform.scale(self.menu_background, (self.width, self.height))
        self.settings_background = pg.transform.scale(self.settings_background, (self.width, self.height))
        self.small_button = pg.transform.scale(self.small_button, (self.width, self.height))
        self.medium_button = pg.transform.scale(self.medium_button, (self.width, self.height))
        self.large_button = pg.transform.scale(self.large_button, (self.width, self.height))
        self.back_button = pg.transform.scale(self.back_button, (self.width, self.height))
        self.play_button = pg.transform.scale(self.play_button, (self.width, self.height))
        self.settings_button = pg.transform.scale(self.settings_button, (self.width, self.height))
        self.exit_button = pg.transform.scale(self.exit_button, (self.width, self.height))
        self.waiting_screen = pg.transform.scale(self.waiting_screen, (self.width, self.height))
        self.connecting_screen = pg.transform.scale(self.connecting_screen, (self.width, self.height))
        self.win = pg.display.set_mode((self.width, self.height))

    def settings_menu(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    x, y = pos
                    x, y = (x / self.width, y / self.width)
                    if 0.026 < x < 0.274 and 0.427 < y < 0.726:
                        self.width = 300
                        self.height = 300
                        self.resize_assets()
                    if 0.326 < x < 0.675 and 0.427 < y < 0.726:
                        self.width = 600
                        self.height = 600
                        self.resize_assets()
                    if 0.726 < x < 0.975 and 0.377 < y < 0.726:
                        self.width = 900
                        self.height = 900
                        self.resize_assets()
                    if 0.375 < x < 0.625 and 0.777 < y < 0.926:
                        running = False

            self.win.blit(self.settings_background, (0, 0))

            pos = pg.mouse.get_pos()
            x, y = pos
            x, y = (x / self.width, y / self.width)

            if 0.026 < x < 0.274 and 0.427 < y < 0.726:
                self.win.blit(self.small_button, (0, 0))
            if 0.326 < x < 0.675 and 0.427 < y < 0.726:
                self.win.blit(self.medium_button, (0, 0))
            if 0.726 < x < 0.975 and 0.377 < y < 0.726:
                self.win.blit(self.large_button, (0, 0))
            if 0.375 < x < 0.625 and 0.777 < y < 0.926:
                self.win.blit(self.back_button, (0, 0))

            pg.display.update()

    def menu(self):
        running = True

        while running:

            self.clock.tick(30)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    x, y = pos
                    x, y = (x / self.width, y / self.width)
                    if 0.377 < x < 0.626 and 0.477 < y < 0.627:
                        running = False

                    if 0.276 < x < 0.726 and 0.626 < y < 0.776:
                        self.settings_menu()

                    if 0.376 < x < 0.626 and 0.777 < y < 0.926:
                        pg.quit()

            self.win.blit(self.menu_background, (0, 0))

            pos = pg.mouse.get_pos()
            x, y = pos
            x, y = (x / self.width, y / self.width)

            if 0.377 < x < 0.626 and 0.477 < y < 0.627:
                self.win.blit(self.play_button, (0, 0))

            if 0.276 < x < 0.726 and 0.626 < y < 0.776:
                self.win.blit(self.settings_button, (0, 0))

            if 0.376 < x < 0.626 and 0.777 < y < 0.926:
                self.win.blit(self.exit_button, (0, 0))
            pg.display.update()

    def mainloop(self, meta):
        global peices1, peices2
        self.meta = meta
        self.font = pg.font.Font('freesansbold.ttf', 50)




        start = n.send('ready')

        while not start:
            self.clock.tick(30)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()

            self.win.fill(c.WHITE)

            self.win.blit(self.waiting_screen, (0, 0))

            start = n.send('ready')
            pg.display.update()
        run = True

        while run:

            self.clock.tick(60)

            if player == 0:
                self.meta, peices = (n.send((self.meta, [self.shrink_coords(peices1), self.shrink_coords(peices2)])))
                peices1 = self.enlarge_coords(peices[0])
                peices2 = self.enlarge_coords(peices[1])
            else:
                self.meta, peices = (n.send((self.meta, [self.swap_ploc(self.shrink_coords(peices1)),
                                                         self.swap_ploc(self.shrink_coords(peices2))])))
                peices1 = self.enlarge_coords(self.swap_ploc(peices[0]))
                peices2 = self.enlarge_coords(self.swap_ploc(peices[1]))

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

    def enlarge_coords(self, peices):
        for peice in peices:
            peice.x *= (self.width // 8)
            peice.y *= (self.width // 8)
        return peices

    def shrink_coords(self, peices):
        for peice in peices:
            peice.x //= (self.width // 8)
            peice.y //= (self.width // 8)
        return peices

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
            piece.x = 7 - piece.x
            piece.y = 7 - piece.y
        return pieces

    def click(self, loc):

        if player == 0:
            me = peices1
            notme = peices2
        else:
            me = peices2
            notme = peices1

        for i, peice in enumerate(me):
            if self.convert_loc(peice.get_location()) == self.convert_loc(loc):
                if player == self.meta.turn:
                    squares = peice.generate_squares(me, notme, self.convert_loc(loc), self.width // 8)
                else:
                    squares = []

                pg.event.get()
                c, *_ = pg.mouse.get_pressed()
                x, y = pg.mouse.get_pos()
                x = x - (x // (self.width // 8)) * (self.width // 8)
                y = y - (y // (self.width // 8)) * (self.width // 8)

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
                    if self.meta.turn == player:
                        self.meta.peicemoved = True
                    if peice.moved():
                        selection = self.reached_end(me)
                        self.meta.premote = True

                        if selection == 1:
                            self.meta.premotedata = (player, i,
                                                     Rook(peice.x // (self.width // 8), peice.y // (self.width // 8),
                                                          peice.type, self.width))


                        elif selection == 2:
                            self.meta.premotedata = (
                                player, i, Bishop(peice.x // (self.width // 8), peice.y // (self.width // 8),
                                                  peice.type, self.width))

                        elif selection == 3:

                            self.meta.premotedata = (
                                player, i, Knight(peice.x // (self.width // 8), peice.y // (self.width // 8),
                                                  peice.type, self.width))
                        elif selection == 4:
                            self.meta.premotedata = (
                                player, i, Queen(peice.x // (self.width // 8), peice.y // (self.width // 8),
                                                 peice.type, self.width))
                        if player == 1:
                            self.meta.premotedata[2].x = 7 - self.meta.premotedata[2].x
                            self.meta.premotedata[2].y = 7 - self.meta.premotedata[2].y
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

    root.menu()


    while True:
        n = Network()
        root.clock.tick(30)
        try:
            meta, peices, player = n.getP()
            break
        except:
            root.win.blit(root.connecting_screen, (0, 0))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    x, y = pos
                    x, y = (x / root.width, y / root.width)

                    if 0.375 < x < 0.625 and 0.777 < y < 0.926:
                        root.menu()
            pos = pg.mouse.get_pos()
            x, y = pos
            x, y = (x / root.width, y / root.width)
            if 0.375 < x < 0.625 and 0.777 < y < 0.926:
                root.win.blit(root.back_button, (0, 0))
            pg.display.update()
    peices1 = peices[0]
    peices2 = peices[1]

    root.mainloop(meta)
