import pyxel
import random as rand


class Block:
    def __init__(self):
        self.n = False  # /\
        self.e = False  # >
        self.s = False  # \/
        self.w = False  # <

    def reset(self):
        self.n = False
        self.e = False
        self.s = False
        self.w = False

    def draw(self, x, y):
        pyxel.pset(x, y, 7)
        if self.n:
            pyxel.pset(x, y - 1, 6)
        if self.e:
            pyxel.pset(x + 1, y, 6)
        if self.s:
            pyxel.pset(x, y + 1, 6)
        if self.w:
            pyxel.pset(x - 1, y, 6)


class App:
    def __init__(self):
        pyxel.init(55, 55, fps=30)
        rand.seed(10)
        self.maze = []
        for y in range(pyxel.height // 2 + 1):
            for x in range(pyxel.width // 2 + 1):
                self.maze.append(Block())
        self.SIZE = (pyxel.width // 2, pyxel.height // 2)

        self.start = self.SIZE[0] // 2, self.SIZE[1] // 2
        self.current = list(self.start)
        self.last = list(self.current)

        self.posibble_moves = set()

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        def add(x, y):
            if pyxel.pget(x * 2, y * 2) == 0:
                next_moves.add((x, y))

        def update_maze():
            b1, b2 = self.last, self.current
            x, y = b1[0] - b2[0], b1[1] - b2[1]
            i1 = b1[1] * self.SIZE[0] + b1[0]
            i2 = b2[1] * self.SIZE[0] + b2[0]
            if x == 0:
                if y < 0:
                    self.maze[i1].s = True
                    self.maze[i2].n = True
                else:
                    self.maze[i1].n = True
                    self.maze[i2].s = True
            elif y == 0:
                if x < 0:
                    self.maze[i1].e = True
                    self.maze[i2].w = True
                else:
                    self.maze[i1].w = True
                    self.maze[i2].e = True

        cx, cy = self.current
        next_moves = set()

        x = cx - 1
        if x >= 0:
            add(x, cy)
        y = cy - 1
        if y >= 0:
            add(cx, y)
        x = cx + 1
        if x <= self.SIZE[0]:
            add(x, cy)
        y = cy + 1
        if y <= self.SIZE[1]:
            add(cx, y)

        if next_moves:
            next_move = rand.choice(tuple(next_moves))
            if len(next_moves) > 1:
                # self.posibble_moves.add(next_move)
                self.posibble_moves.add(tuple(self.current))
            self.last = list(self.current)
            self.current = list(next_move)

            update_maze()
            # print(len(self.posibble_moves))
        else:
            if self.posibble_moves:
                print(len(self.posibble_moves))
                self.current = list(self.posibble_moves.pop())

    def draw(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            for block in self.maze:
                block.reset()
            self.posibble_moves.clear()
            pyxel.cls(0)

        b1, b2 = self.last, self.current
        # pyxel.pset(b1[0] * 2, b1[1] * 2, 7)
        # pyxel.pset(b2[0] * 2, b2[1] * 2, 12)

        i1 = b1[1] * self.SIZE[0] + b1[0]
        i2 = b2[1] * self.SIZE[0] + b2[0]
        self.maze[i1].draw(b1[0] * 2, b1[1] * 2)
        self.maze[i2].draw(b2[0] * 2, b2[1] * 2)
        # pyxel.text(2, 2, str(self.current), 7)


if __name__ == '__main__':
    a = App()
    a.run()
