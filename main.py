import copy
import pygame


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                  self.cell_size,
                                  self.cell_size), 1)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # cell - кортеж (x, y)
    def on_click_wall(self, cell):
        # заглушка для реальных игровых полей
        pass

    def on_click_move(self, cell):
        # заглушка для реальных игровых полей
        pass

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click_wall(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell and cell < (self.width, self.height):
            self.on_click_wall(cell)

    def get_click_move(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell and cell < (self.width, self.height):
            self.on_click_move(cell)


class Quoridor(Board):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.selected_cell = None
        self.board[0][0] = 2
        self.board[-1][-1] = 3
        self.cur_person = "blue"
        self.blue_pos = (0, 0)
        self.red_pos = (height - 1, width - 1)

    def has_path(self, x1, y1, x2, y2):
        # словарь расстояний
        d = {(x1, y1): 0}
        v = [(x1, y1)]
        while len(v) > 0:
            x, y = v.pop(0)
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dx * dy != 0:
                        continue
                    if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                        continue
                    if self.board[y + dy][x + dx] in [0, 2, 3]:
                        dn = d.get((x + dx, y + dy), -1)
                        if dn == -1:
                            d[(x + dx, y + dy)] = d.get((x, y), -1) + 1
                            v.append((x + dx, y + dy))
        dist = d.get((x2, y2), -1)
        return dist >= 0

    def on_click_wall(self, cell):
        x = cell[0]
        y = cell[1]
        if self.cur_person == "blue" and self.board[y][x] == 0:
            self.board[y][x] = 1
            paths1 = []
            paths2 = []
            for i in range(0, self.width):
                paths1.append(self.has_path(i, self.height - 1, self.blue_pos[0], self.blue_pos[1]))
            for i in range(0, self.width):
                paths2.append(self.has_path(i, 0, self.red_pos[0], self.red_pos[1]))
            if not (any(paths1) and any(paths2)):
                self.board[y][x] = 0
            else:
                self.cur_person = "red"
        elif self.cur_person == "red" and self.board[y][x] == 0:
            self.board[y][x] = 1
            paths1 = []
            paths2 = []
            for i in range(0, self.width):
                paths1.append(self.has_path(i, self.height - 1, self.blue_pos[0], self.blue_pos[1]))
            for i in range(0, self.width):
                paths2.append(self.has_path(i, 0, self.red_pos[0], self.red_pos[1]))
            if not (any(paths1) and any(paths2)):
                self.board[y][x] = 0
            else:
                self.cur_person = "blue"

    def on_click_move(self, cell):
        x = cell[0]
        y = cell[1]
        if self.cur_person == "blue" and (x - 1 == self.blue_pos[0] and y == self.blue_pos[1] or
                                          x + 1 == self.blue_pos[0] and y == self.blue_pos[1] or
                                          x == self.blue_pos[0] and y - 1 == self.blue_pos[1] or
                                          x == self.blue_pos[0] and y + 1 == self.blue_pos[1]):
            self.board[self.blue_pos[1]][self.blue_pos[0]] = 0
            self.blue_pos = cell
            self.board[y][x] = 2
            self.cur_person = "red"
        elif self.cur_person == "red" and (x - 1 == self.red_pos[0] and y == self.red_pos[1] or
                                           x + 1 == self.red_pos[0] and y == self.red_pos[1] or
                                           x == self.red_pos[0] and y - 1 == self.red_pos[1] or
                                           x == self.red_pos[0] and y + 1 == self.red_pos[1]):
            self.board[self.red_pos[1]][self.red_pos[0]] = 0
            self.red_pos = cell
            self.board[y][x] = 3
            self.cur_person = "blue"

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):

                if self.board[y][x] == 1:
                    color = pygame.Color("white")
                    pygame.draw.rect(screen, color,
                                        (x * self.cell_size + self.left,
                                         y * self.cell_size + self.top, self.cell_size,
                                         self.cell_size))
                elif self.board[y][x] == 2:
                    color = pygame.Color("blue")
                    pygame.draw.ellipse(screen, color,
                                        (x * self.cell_size + self.left,
                                         y * self.cell_size + self.top, self.cell_size,
                                         self.cell_size))
                elif self.board[y][x] == 3:
                    color = pygame.Color("red")
                    pygame.draw.ellipse(screen, color,
                                        (x * self.cell_size + self.left,
                                         y * self.cell_size + self.top, self.cell_size,
                                         self.cell_size))

                pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                  self.cell_size,
                                  self.cell_size), 1)


def main():
    pygame.init()
    size = 650, 650
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Quoridor')

    board = Quoridor(9, 9)
    board.set_view(9, 9, 70)

    ticks = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                board.get_click_wall(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                board.get_click_move(event.pos)

        screen.fill((0, 0, 0))
        board.render(screen)
        if ticks == 50:
            ticks = 0
        pygame.display.flip()
        clock.tick(50)
        ticks += 1
    pygame.quit()


if __name__ == '__main__':
    main()
