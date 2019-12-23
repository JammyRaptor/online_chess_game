class Meta:
    def __init__(self):
        self.turn = 0
        self.moved = False
        self.peicemoved = False
        self.premote = False
        # premotedata key = (player, position, promotion)
        self.premotedata = (0, 0, 0)
    def swapturn(self):
        if self.turn == 0:
            self.turn = 1
        else:
            self.turn = 0
