import pygame as pg



class Piece:
    def __init__(self, x, y, type, screemWidth):

        self.type = type
        self.image = self.get_image()
        self.width = screemWidth // 8
        self.height = screemWidth // 8

        self.x = x * self.width
        self.y = y * self.width



        self.moves = []
        self.extrainit()
        self.piece = ''
        self.inplay = True

    def take(self):
        self.inplay = False
        self.x = 10 * self.width
        self.y = 10 * self.width

    def generate_squares(self, peices1, peices2, loc):
        squares = []
        for move in self.moves:
            looking = True
            mm = (0, 0)
            while looking:
                mm = (mm[0] + move[0], mm[1] + move[1])
                x, y = loc
                x += mm[0]
                y += mm[1]

                collide = False
                for peice in peices1:
                    if (x, y) == (peice.x // self.width, peice.y // self.width):
                        collide = True
                if x > 7 or x < 0 or y > 7 or y < 0:
                    collide = True
                if not collide:
                    squares.append(Square(loc, mm, self.width))

                    for peice in peices2:
                        if (x, y) == (peice.x // self.width, peice.y // self.width):
                            collide = True
                    if collide:
                        looking = False
                else:
                    looking = False
        return squares

    def checkmove(self, move, peices, loc, ):
        xl, yl = loc
        xm, ym = move
        xl += xm
        yl += ym

        if xl > 7 or xl < 0 or yl > 7 or yl < 0:
            return False

        for p in peices:
            if p.x // self.width == xl and p.y // self.width == yl:
                return False
        return True

    def extrainit(self):
        pass

    def moved(self):
        pass

    def draw(self):
        if self.inplay:
            return True

    def get_image(self):
        pass

    def get_location(self):
        loc = (self.x, self.y)
        return loc


class Bishop(Piece):
    def get_image(self):
        return 2

    def extrainit(self):
        self.moves = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.piece = 'bishop'


class Pawn(Piece):
    def moved(self):
        if self.first:
            self.moves.pop(1)

        self.first = False

        if self.y == 0:
            return True

    def extrainit(self):
        self.first = True
        self.moves = [(0, -1), (0, -2)]
        self.takemoves = [(-1, -1,), (1, -1)]
        self.piece = 'pawn'

    def get_image(self):
        return 0

    def generate_squares(self, peices1, peices2, loc):
        squares = []

        for move in self.moves:
            if self.checkmove(move, peices1 + peices2, loc):
                squares.append(Square(loc, move, self.width))

        for move in self.takemoves:
            if not (self.checkmove(move, peices2, loc)):
                squares.append(Square(loc, move, self.width))
        return squares


class King(Piece):
    def extrainit(self):
        self.moves = [(0, -1), (0, 1), (-1, 0), (1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        self.piece = 'king'

    def get_image(self):
        return 5

    def generate_squares(self, peices1, peices2, loc):
        squares = []

        for move in self.moves:
            if self.checkmove(move, peices1, loc):
                squares.append(Square(loc, move, self.width))

        return squares


class Knight(Piece):
    def extrainit(self):
        self.moves = [(-1, 2), (1, 2), (-2, 1), (2, 1), (-1, -2), (1, -2), (-2, -1), (2, -1)]
        self.piece = 'knight'

    def get_image(self):
        return 1

    def generate_squares(self, peices1, peices2, loc):
        squares = []

        for move in self.moves:
            if self.checkmove(move, peices1, loc):
                squares.append(Square(loc, move, self.width))

        return squares


class Rook(Piece):
    def get_image(self):
        return 3

    def extrainit(self):
        self.moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.piece = 'rook'


class Queen(Piece):
    def get_image(self):
        return 4

    def extrainit(self):
        self.moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.piece = 'queen'


class Square:

    def __init__(self, loc, move, width):
        self.image = pg.image.load(f'assets/rectangle.png')
        self.image = pg.transform.scale(self.image, (width, width))

        x, y = loc
        xm, ym = move

        x += xm
        y += ym

        self.x = x * width
        self.y = y * width

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
