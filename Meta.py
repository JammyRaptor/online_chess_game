class Meta():
    def __init__(self):
        self.turn = 0
        self.moved = False
        self.peicemoved = True

    def swapturn(self):
        if self.turn == 0:
            self.turn = 1
        else:
            self.turn = 0
