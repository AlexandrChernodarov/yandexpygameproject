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

    def curent_wall(self):
        pass

    def render(self, screen, tick):
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
    def on_click_wall(self, cell, elem):
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

    def get_click_wall(self, mouse_pos, ev):
        cell = self.get_cell(mouse_pos)
        if cell and cell < (self.width, self.height):
            self.on_click_wall(cell, ev)

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
        self.walls1 = [[0] * (width - 1)for _ in range(height)]
        self.walls2 = [[0] * width for _ in range(height - 1)]
        self.cur_wall = 0
        self.cur_wall_cell = None

    def curent_wall(self):
        return self.cur_wall

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
                    if self.board[y + dy][x + dx] in [0, 1, 2, 3]:
                        if ((dy == 0 and dx != 0 and self.walls1[y][min(x, x + dx)] == 0) or
                                (dx == 0 and dy != 0 and self.walls2[min(y, y + dy)][x] == 0)):
                            dn = d.get((x + dx, y + dy), -1)
                            if dn == -1:
                                d[(x + dx, y + dy)] = d.get((x, y), -1) + 1
                                v.append((x + dx, y + dy))
        dist = d.get((x2, y2), -1)
        return dist >= 0

    def on_click_wall(self, cell, elem):
        x = cell[0]
        y = cell[1]
        if self.cur_person == "blue" and self.board[y][x] in [0, 1]:
            if not elem:
                self.board[y][x] = 1
                if self.cur_wall_cell:
                    self.board[self.cur_wall_cell[1]][self.cur_wall_cell[0]] = 0
                self.cur_wall_cell = (x, y)
                self.cur_wall = 1
            else:
                if elem == "left" and self.cur_wall_cell[0] != 0:
                    if self.walls1[y][x - 1] == 0:
                        self.walls1[y][x - 1] = 1
                    else:
                        return
                    paths1 = []
                    paths2 = []
                    for i in range(0, self.width):
                        paths1.append(self.has_path(i, self.height - 1, self.blue_pos[0], self.blue_pos[1]))
                    for i in range(0, self.width):
                        paths2.append(self.has_path(i, 0, self.red_pos[0], self.red_pos[1]))
                    if not (any(paths1) and any(paths2)):
                        self.walls1[y][x - 1] = 0
                    else:
                        self.board[self.cur_wall_cell[1]][self.cur_wall_cell[0]] = 0
                        self.cur_person = "red"
                        self.cur_wall_cell = None
                        self.cur_wall = 0
                elif elem == "right" and self.cur_wall_cell[0] != self.width - 1:
                    if self.walls1[y][x] == 0:
                        self.walls1[y][x] = 1
                    else:
                        return
                    paths1 = []
                    paths2 = []
                    for i in range(0, self.width):
                        paths1.append(self.has_path(i, self.height - 1, self.blue_pos[0], self.blue_pos[1]))
                    for i in range(0, self.width):
                        paths2.append(self.has_path(i, 0, self.red_pos[0], self.red_pos[1]))
                    if not (any(paths1) and any(paths2)):
                        self.walls1[y][x] = 0
                    else:
                        self.board[self.cur_wall_cell[1]][self.cur_wall_cell[0]] = 0
                        self.cur_person = "red"
                        self.cur_wall_cell = None
                        self.cur_wall = 0
                elif elem == "up" and self.cur_wall_cell[1] != 0:
                    if self.walls2[y - 1][x] == 0:
                        self.walls2[y - 1][x] = 1
                    else:
                        return
                    paths1 = []
                    paths2 = []
                    for i in range(0, self.width):
                        paths1.append(self.has_path(i, self.height - 1, self.blue_pos[0], self.blue_pos[1]))
                    for i in range(0, self.width):
                        paths2.append(self.has_path(i, 0, self.red_pos[0], self.red_pos[1]))
                    if not (any(paths1) and any(paths2)):
                        self.walls2[y - 1][x] = 0
                    else:
                        self.board[self.cur_wall_cell[1]][self.cur_wall_cell[0]] = 0
                        self.cur_person = "red"
                        self.cur_wall_cell = None
                        self.cur_wall = 0
                elif elem == "down" and self.cur_wall_cell[1] != self.height - 1:
                    if self.walls2[y][x] == 0:
                        self.walls2[y][x] = 1
                    else:
                        return
                    paths1 = []
                    paths2 = []
                    for i in range(0, self.width):
                        paths1.append(self.has_path(i, self.height - 1, self.blue_pos[0], self.blue_pos[1]))
                    for i in range(0, self.width):
                        paths2.append(self.has_path(i, 0, self.red_pos[0], self.red_pos[1]))
                    if not (any(paths1) and any(paths2)):
                        self.walls2[y][x] = 0
                    else:
                        self.board[self.cur_wall_cell[1]][self.cur_wall_cell[0]] = 0
                        self.cur_person = "red"
                        self.cur_wall_cell = None
                        self.cur_wall = 0
        elif self.cur_person == "red" and self.board[y][x] in [0, 1]:
            if not elem:
                self.board[y][x] = 1
                if self.cur_wall_cell:
                    self.board[self.cur_wall_cell[1]][self.cur_wall_cell[0]] = 0
                self.cur_wall_cell = (x, y)
                self.cur_wall = 1
            else:
                if elem == "left" and self.cur_wall_cell[0] != 0:
                    if self.walls1[y][x - 1] == 0:
                        self.walls1[y][x - 1] = 1
                    else:
                        return
                    paths1 = []
                    paths2 = []
                    for i in range(0, self.width):
                        paths1.append(self.has_path(i, self.height - 1, self.blue_pos[0], self.blue_pos[1]))
                    for i in range(0, self.width):
                        paths2.append(self.has_path(i, 0, self.red_pos[0], self.red_pos[1]))
                    if not (any(paths1) and any(paths2)):
                        self.walls1[y][x - 1] = 0
                    else:
                        self.board[self.cur_wall_cell[1]][self.cur_wall_cell[0]] = 0
                        self.cur_person = "blue"
                        self.cur_wall_cell = None
                        self.cur_wall = 0

                elif elem == "right" and self.cur_wall_cell[0] != self.width - 1:
                    if self.walls1[y][x] == 0:
                        self.walls1[y][x] = 1
                    else:
                        return
                    paths1 = []
                    paths2 = []
                    for i in range(0, self.width):
                        paths1.append(self.has_path(i, self.height - 1, self.blue_pos[0], self.blue_pos[1]))
                    for i in range(0, self.width):
                        paths2.append(self.has_path(i, 0, self.red_pos[0], self.red_pos[1]))
                    if not (any(paths1) and any(paths2)):
                        self.walls1[y][x] = 0
                    else:
                        self.board[self.cur_wall_cell[1]][self.cur_wall_cell[0]] = 0
                        self.cur_person = "blue"
                        self.cur_wall_cell = None
                        self.cur_wall = 0
                elif elem == "up" and self.cur_wall_cell[1] != 0:
                    if self.walls2[y - 1][x] == 0:
                        self.walls2[y - 1][x] = 1
                    else:
                        return
                    paths1 = []
                    paths2 = []
                    for i in range(0, self.width):
                        paths1.append(self.has_path(i, self.height - 1, self.blue_pos[0], self.blue_pos[1]))
                    for i in range(0, self.width):
                        paths2.append(self.has_path(i, 0, self.red_pos[0], self.red_pos[1]))
                    if not (any(paths1) and any(paths2)):
                        self.walls2[y - 1][x] = 0
                    else:
                        self.board[self.cur_wall_cell[1]][self.cur_wall_cell[0]] = 0
                        self.cur_person = "blue"
                        self.cur_wall_cell = None
                        self.cur_wall = 0
                elif elem == "down" and self.cur_wall_cell[1] != self.height - 1:
                    if self.walls2[y][x] == 0:
                        self.walls2[y][x] = 1
                    else:
                        return
                    paths1 = []
                    paths2 = []
                    for i in range(0, self.width):
                        paths1.append(self.has_path(i, self.height - 1, self.blue_pos[0], self.blue_pos[1]))
                    for i in range(0, self.width):
                        paths2.append(self.has_path(i, 0, self.red_pos[0], self.red_pos[1]))
                    if not (any(paths1) and any(paths2)):
                        self.walls2[y][x] = 0
                    else:
                        self.board[self.cur_wall_cell[1]][self.cur_wall_cell[0]] = 0
                        self.cur_person = "blue"
                        self.cur_wall_cell = None
                        self.cur_wall = 0

    def on_click_move(self, cell):
        x = cell[0]
        y = cell[1]
        if self.cur_person == "blue" and (x - 1 == self.blue_pos[0] and y == self.blue_pos[1] and
                                          self.walls1[y][min(x, x - 1)] == 0 or
                                          x + 1 == self.blue_pos[0] and y == self.blue_pos[1] and
                                          self.walls1[y][min(x, x + 1)] == 0 or
                                          x == self.blue_pos[0] and y - 1 == self.blue_pos[1] and
                                          self.walls2[min(y, y - 1)][x] == 0 or
                                          x == self.blue_pos[0] and y + 1 == self.blue_pos[1] and
                                          self.walls2[min(y, y + 1)][x] == 0):
            self.board[self.blue_pos[1]][self.blue_pos[0]] = 0
            self.blue_pos = cell
            self.board[y][x] = 2
            self.cur_person = "red"
        elif self.cur_person == "red" and (x - 1 == self.red_pos[0] and y == self.red_pos[1] and
                                           self.walls1[y][min(x, x - 1)] == 0 or
                                           x + 1 == self.red_pos[0] and y == self.red_pos[1] and
                                           self.walls1[y][min(x, x + 1)] == 0 or
                                           x == self.red_pos[0] and y - 1 == self.red_pos[1] and
                                           self.walls2[min(y, y - 1)][x] == 0 or
                                           x == self.red_pos[0] and y + 1 == self.red_pos[1] and
                                           self.walls2[min(y, y + 1)][x] == 0):
            self.board[self.red_pos[1]][self.red_pos[0]] = 0
            self.red_pos = cell
            self.board[y][x] = 3
            self.cur_person = "blue"

    def render(self, screen, tick):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 1:
                    if tick == 0:
                        color = pygame.Color("white")
                    else:
                        color = pygame.Color("black")
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
        for y in range(self.height):
            for x in range(self.width - 1):
                if self.walls1[y][x] == 1:
                    color = pygame.Color("green")
                    pygame.draw.rect(screen, color,
                                     (x * self.cell_size + self.left + self.cell_size * 7 // 8,
                                      y * self.cell_size + self.top, self.cell_size / 4,
                                      self.cell_size))
        for y in range(self.height - 1):
            for x in range(self.width):
                if self.walls2[y][x] == 1:
                    color = pygame.Color("green")
                    pygame.draw.rect(screen, color,
                                     (x * self.cell_size + self.left,
                                      y * self.cell_size + self.top + self.cell_size * 7 // 8, self.cell_size,
                                      self.cell_size / 4))


def main():
    pygame.init()
    size = 650, 650
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Quoridor')
    last_wall_press = (100, 100)

    board = Quoridor(9, 9)
    board.set_view(9, 9, 70)

    ticks = 0
    ticks2 = 0
    ticks3 = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                last_wall_press = event.pos
                board.get_click_wall(last_wall_press, None)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and board.curent_wall() == 0:
                board.get_click_move(event.pos)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and board.curent_wall() == 1:
                board.get_click_wall(last_wall_press, "left")
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and board.curent_wall() == 1:
                board.get_click_wall(last_wall_press, "right")
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and board.curent_wall() == 1:
                board.get_click_wall(last_wall_press, "up")
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and board.curent_wall() == 1:
                board.get_click_wall(last_wall_press, "down")

        screen.fill((0, 0, 0))
        board.render(screen, ticks3)
        if ticks == 60:
            ticks = 0
        if ticks2 == 20:
            ticks2 = 0
            if ticks3 == 1:
                ticks3 = 0
            else:
                ticks3 = 1

        pygame.display.flip()
        clock.tick(60)
        ticks += 1
        ticks2 += 1
    pygame.quit()


if __name__ == '__main__':
    main()
