class Blueprinter:
    def __init__(self):
        self.command_list = ['сместись_в_точку', 'сместись_на_вектор', 'подними_перо', 'опусти_перо']
        self.pos = [0, 0]
        self.f = True

    def moveto(self, x, y):
        self.pos = [x * 20, y * 20]

    def vector_move(self, x, y):
        self.pos[0] += x * 20
        self.pos[1] += y * 20

    def up(self):
        self.f = False

    def down(self):
        self.f = True

    def f(self):
        return self.f

    def pos(self):
        return self.pos
