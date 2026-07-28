import random, sys, pygame
from dataclasses import dataclass, field

pygame.init()

SHAPES = {
    "I": [[1, 1, 1, 1]], "O": [[1, 1], [1, 1]], "T": [[0, 1, 0], [1, 1, 1]],
    "L": [[1, 0, 0], [1, 1, 1]], "J": [[0, 0, 1], [1, 1, 1]],
    "S": [[0, 1, 1], [1, 1, 0]], "Z": [[1, 1, 0], [0, 1, 1]],
}
COLORS = {
    "I": (0, 220, 220), "O": (240, 220, 70), "T": (170, 90, 220),
    "L": (255, 150, 40), "J": (70, 120, 240), "S": (80, 200, 120), "Z": (230, 80, 80),
}

@dataclass(frozen=True)
class Cfg:
    cell: int = 30; cols: int = 10; rows: int = 20; side: int = 240; fps: int = 60
    bg: tuple = (18, 18, 24); panel: tuple = (24, 24, 32); grid: tuple = (40, 40, 52)
    border: tuple = (80, 80, 110); text: tuple = (235, 235, 240); muted: tuple = (180, 180, 195)
    accent: tuple = (255, 215, 90); fail: tuple = (200, 70, 70); ok: tuple = (90, 210, 120)
    targets: dict = field(default_factory=lambda: {1: 18, 2: 26, 3: 36})
    speeds: dict = field(default_factory=lambda: {1: 550, 2: 350, 3: 180})
    @property
    def width(self): return self.cols * self.cell + self.side
    @property
    def height(self): return self.rows * self.cell

@dataclass
class Piece:
    name: str; matrix: list; color: tuple; x: int; y: int = 0
    def rotated(self): return [list(r) for r in zip(*self.matrix[::-1])]
    def cells(self, dx=0, dy=0, matrix=None):
        for y, row in enumerate(matrix or self.matrix):
            for x, v in enumerate(row):
                if v: yield self.x + x + dx, self.y + y + dy

class Board:
    def __init__(self, c): self.c = c; self.reset()
    def reset(self): self.grid = [[None] * self.c.cols for _ in range(self.c.rows)]
    def valid(self, p, dx=0, dy=0, matrix=None):
        for x, y in p.cells(dx, dy, matrix):
            if x < 0 or x >= self.c.cols or y >= self.c.rows or (y >= 0 and self.grid[y][x] is not None): return False
        return True
    def lock(self, p):
        for x, y in p.cells():
            if 0 <= y < self.c.rows: self.grid[y][x] = p.color
    def clear(self):
        keep = [r for r in self.grid if not all(r)]
        n = self.c.rows - len(keep)
        self.grid = [[None] * self.c.cols for _ in range(n)] + keep
        return n

class Tetris:
    MENU, RULES, PLAYING, OVER = "menu", "rules", "playing", "over"

    def __init__(self):
        self.c = Cfg()
        self.screen = pygame.display.set_mode((self.c.width, self.c.height))
        pygame.display.set_caption("Тетрис")
        self.clock = pygame.time.Clock()
        self.f1 = pygame.font.SysFont("arial", 34, bold=True)
        self.f2 = pygame.font.SysFont("arial", 22)
        self.f3 = pygame.font.SysFont("arial", 18)
        self.menu, self.mi = ["Начать игру", "Правила", "Выход"], 0
        self.board, self.state = Board(self.c), self.MENU
        self.reset()

    def new_piece(self):
        n = random.choice(list(SHAPES)); m = [r[:] for r in SHAPES[n]]
        return Piece(n, m, COLORS[n], self.c.cols // 2 - len(m[0]) // 2)

    def reset(self):
        self.board.reset()
        self.level = self.lines = self.score = self.placed = self.on_level = self.drop = 0
        self.level, self.fast = 1, False
        self.msg, self.msg_color = "", self.c.fail
        self.cur, self.next = self.new_piece(), self.new_piece()

    def start(self): self.reset(); self.state = self.PLAYING

    def move(self, dx, dy):
        if self.board.valid(self.cur, dx, dy):
            self.cur.x += dx; self.cur.y += dy
            return True
        return False

    def rotate(self):
        m = self.cur.rotated()
        if self.board.valid(self.cur, matrix=m): self.cur.matrix = m; return
        for s in (-1, 1, -2, 2):
            if self.board.valid(self.cur, dx=s, matrix=m):
                self.cur.x += s; self.cur.matrix = m; return

    def lock(self):
        self.board.lock(self.cur)
        self.placed += 1; self.on_level += 1
        n = self.board.clear()
        self.lines += n; self.score += n * 100 * self.level
        if self.level < 3 and self.on_level >= self.c.targets[self.level]:
            self.level += 1; self.on_level = 0
        elif self.level == 3 and self.on_level >= self.c.targets[3]:
            self.msg, self.msg_color, self.state = "Победа! Три уровня пройдены", self.c.ok, self.OVER
            return
        self.cur, self.next = self.next, self.new_piece()
        if not self.board.valid(self.cur):
            self.msg, self.msg_color, self.state = "Игра окончена: поле заполнено", self.c.fail, self.OVER

    def update(self, dt):
        if self.state != self.PLAYING: return
        self.drop += dt
        if self.drop >= (40 if self.fast else self.c.speeds[self.level]):
            self.drop = 0
            if not self.move(0, 1): self.lock()

    def cell(self, x, y, color, s=None, ox=0):
        s = s or self.c.cell
        r = pygame.Rect(ox + x * s, y * s, s, s)
        pygame.draw.rect(self.screen, color, r.inflate(-2, -2), border_radius=4)
        pygame.draw.rect(self.screen, self.c.border, r, 1)

    def text(self, txt, font, color, pos, center=False):
        img = font.render(txt, True, color)
        self.screen.blit(img, img.get_rect(center=pos) if center else pos)

    def draw_board(self):
        pygame.draw.rect(self.screen, self.c.panel, (0, 0, self.c.cols * self.c.cell, self.c.rows * self.c.cell))
        for y in range(self.c.rows):
            for x in range(self.c.cols):
                pygame.draw.rect(self.screen, self.c.grid, (x * self.c.cell, y * self.c.cell, self.c.cell, self.c.cell), 1)
                if self.board.grid[y][x] is not None: self.cell(x, y, self.board.grid[y][x])
        if self.state in (self.PLAYING, self.OVER):
            for x, y in self.cur.cells():
                if y >= 0: self.cell(x, y, self.cur.color)
        pygame.draw.rect(self.screen, self.c.border, (0, 0, self.c.cols * self.c.cell, self.c.rows * self.c.cell), 2)

    def draw_side(self):
        ox = self.c.cols * self.c.cell + 20
        pygame.draw.rect(self.screen, (22, 22, 30), (self.c.cols * self.c.cell, 0, self.c.side, self.c.height))
        self.text("ТЕТРИС", self.f2, self.c.accent, (ox, 20))
        info = [
            f"Уровень: {self.level}",
            f"Фигур всего: {self.placed}",
            f"Фигур на уровне: {self.on_level}/{self.c.targets[self.level]}",
            f"Линий: {self.lines}",
            f"Очки: {self.score}",
        ]
        for i, t in enumerate(info): self.text(t, self.f3, self.c.text, (ox, 60 + i * 28))
        self.text("Следующая", self.f2, self.c.accent, (ox, 220))
        for y, row in enumerate(self.next.matrix):
            for x, v in enumerate(row):
                if v: self.cell(x, y, self.next.color, 24, ox), pygame.draw.rect(self.screen, self.c.border, (ox + x * 24, 260 + y * 24, 24, 24), 1)
        controls = ["Управление:", "← →  движение", "↑ ↓  поворот", "Пробел  ускорение", "Esc  меню", "R  новая игра"]
        for i, t in enumerate(controls): self.text(t, self.f3, self.c.accent if i == 0 else self.c.muted, (ox, 360 + i * 24))

    def draw_menu(self):
        self.screen.fill(self.c.bg)
        self.text("ТЕТРИС", self.f1, self.c.accent, (self.c.width // 2, 110), True)
        self.text("Русское меню игры", self.f3, self.c.muted, (self.c.width // 2, 145), True)
        for i, item in enumerate(self.menu):
            self.text(("> " if i == self.mi else "  ") + item, self.f2, self.c.accent if i == self.mi else self.c.text, (self.c.width // 2, 240 + i * 55), True)
        self.text("↑/↓ - выбор, Enter - подтвердить", self.f3, self.c.muted, (self.c.width // 2, 470), True)

    def draw_rules(self):
        self.screen.fill(self.c.bg)
        self.text("Правила игры", self.f2, self.c.accent, (40, 40))
        rules = [
            "1. Собирайте горизонтальные линии без пустот.",
            "2. Одинаковые фигуры имеют одинаковый цвет.",
            "3. Поворот выполняется стрелками вверх и вниз.",
            "4. Пробел ускоряет падение фигуры.",
            "5. Для перехода на следующий уровень нужно",
            "   разместить нужное количество фигур.",
            "6. На каждом уровне скорость выше.",
            "7. Если поле заполнено — игра заканчивается.",
            "8. Esc - назад в меню.",
        ]
        for i, t in enumerate(rules): self.text(t, self.f3, self.c.text, (40, 95 + i * 32))

    def draw_over(self):
        ov = pygame.Surface((self.c.width, self.c.height), pygame.SRCALPHA); ov.fill((0, 0, 0, 170)); self.screen.blit(ov, (0, 0))
        self.text(self.msg, self.f2, self.msg_color, (self.c.width // 2, self.c.height // 2 - 20), True)
        self.text("Enter - в главное меню", self.f3, self.c.text, (self.c.width // 2, self.c.height // 2 + 25), True)
        self.text("R - начать заново", self.f3, self.c.text, (self.c.width // 2, self.c.height // 2 + 55), True)

    def draw(self):
        if self.state == self.MENU: self.draw_menu(); return
        if self.state == self.RULES: self.draw_rules(); return
        self.screen.fill(self.c.bg); self.draw_board(); self.draw_side()
        if self.state == self.OVER: self.draw_over()

    def keydown(self, k):
        if self.state == self.MENU:
            if k == pygame.K_UP: self.mi = (self.mi - 1) % len(self.menu)
            elif k == pygame.K_DOWN: self.mi = (self.mi + 1) % len(self.menu)
            elif k in (pygame.K_RETURN, pygame.K_KP_ENTER):
                if self.mi == 0: self.start()
                elif self.mi == 1: self.state = self.RULES
                else: pygame.quit(); sys.exit()
            return
        if self.state == self.RULES:
            if k == pygame.K_ESCAPE: self.state = self.MENU
            return
        if self.state == self.OVER:
            if k in (pygame.K_RETURN, pygame.K_KP_ENTER): self.state = self.MENU
            elif k == pygame.K_r: self.start()
            return
        if k == pygame.K_ESCAPE: self.state, self.fast = self.MENU, False
        elif k == pygame.K_r: self.start()
        elif k == pygame.K_LEFT: self.move(-1, 0)
        elif k == pygame.K_RIGHT: self.move(1, 0)
        elif k in (pygame.K_UP, pygame.K_DOWN): self.rotate()
        elif k == pygame.K_SPACE: self.fast = True

    def run(self):
        while True:
            dt = self.clock.tick(self.c.fps)
            for e in pygame.event.get():
                if e.type == pygame.QUIT: pygame.quit(); sys.exit()
                elif e.type == pygame.KEYDOWN: self.keydown(e.key)
                elif e.type == pygame.KEYUP and self.state == self.PLAYING and e.key == pygame.K_SPACE: self.fast = False
            self.update(dt); self.draw(); pygame.display.flip()

if __name__ == "__main__":
    Tetris().run()
