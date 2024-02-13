import pygame
import sys

result = [['', 0], ['', 0]]


def terminate():
    pygame.quit()
    sys.exit()


all_sprites = pygame.sprite.Group()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("green"), (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = 2
        self.vy = 2
        self.add(balls)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
balls = pygame.sprite.Group()
Ball(20, 400, 400)
Border(10, 300, 640, 300)
Border(10, 590, 640, 590)
Border(10, 300, 10, 590)
Border(640, 300, 640, 590)


def start_screen():
    ticks3 = 0
    intro_text = ["Quoridor", "",
                  "Правила игры:",
                  "Игроке делают ход поочереди, можно ставить стенку",
                  "или перемещать свою фишку. Побеждает тот, чья ",
                  "фишка первая окажется в противоположном конце поле.",
                  "Нажмите, чтобы начать играть."]
    pygame.init()
    size = 650, 600
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Quoridor')
    font = pygame.font.Font(None, 30)
    font1 = pygame.font.Font(None, 80)
    text_coord = 50
    girl = AnimatedSprite(pygame.image.load("girl.png").convert(), 8, 10, 550, -10)
    for line in intro_text:
        if line == "Quoridor":
            string_rendered = font1.render(line, 1, pygame.Color('white'))
        else:
            string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        screen.fill(pygame.Color("black"))
        for line in intro_text:
            if line == "Quoridor":
                string_rendered = font1.render(line, 1, pygame.Color('white'))
            else:
                string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        text_coord = 50
        pygame.draw.rect(screen, pygame.Color('white'), (0, 299, 650, 1))
        all_sprites.draw(screen)
        horizontal_borders.update()
        vertical_borders.update()
        balls.update()
        if ticks3 % 5 == 0:
            girl.update()
        pygame.display.flip()
        clock.tick(50)
        ticks3 += 1


def result_screen_1():
    ticks4 = 0
    intro_text = ["Quoridor", "",
                  f"Выиграл {'синий' if result[0][0] == 'blue' else 'красный'}",
                  f"Сделано {result[0][1]} ходов"]
    pygame.init()
    size = 650, 600
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Quoridor')
    font = pygame.font.Font(None, 30)
    font1 = pygame.font.Font(None, 80)
    text_coord = 50
    girl = AnimatedSprite(pygame.image.load("girl.png").convert(), 8, 10, 550, -10)
    for line in intro_text:
        if line == "Quoridor":
            string_rendered = font1.render(line, 1, pygame.Color('white'))
        else:
            string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        screen.fill(pygame.Color("black"))
        for line in intro_text:
            if line == "Quoridor":
                string_rendered = font1.render(line, 1, pygame.Color('white'))
            else:
                string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        text_coord = 50
        pygame.draw.rect(screen, pygame.Color('white'), (0, 299, 650, 1))
        all_sprites.draw(screen)
        horizontal_borders.update()
        vertical_borders.update()
        balls.update()
        if ticks4 % 5 == 0:
            girl.update()
        pygame.display.flip()
        clock.tick(50)
        ticks4 += 1


def result_screen_2():
    ticks5 = 0
    if result[0][0] == 'blue' and result[1][0] == 'blue':
        a = "Выиграл синий"
    elif result[0][0] == 'red' and result[1][0] == 'red':
        a = "Выиграл красный"
    else:
        a = "Ничья"
    b = f"За первый раунд сделано {result[0][1]} ходов(победа {'синего' if result[0][0] == 'blue' else 'красного'})"
    b1 = f"За второй раунд сделано {result[1][1]} ходов(победа {'синего' if result[1][0] == 'blue' else 'красного'})"
    with open('all_results.txt', 'r') as f:
        games = f.read()
    with open('all_results.txt', 'w') as f:
        if result[0][0] == 'blue' and result[1][0] == 'blue':
            games += "1"
            f.write(games)
        elif result[0][0] == 'red' and result[1][0] == 'red':
            games += "2"
            f.write(games)
        else:
            games += "0"
            f.write(games)
    t = f"{games.count('0')} ничья(-их), {games.count('1')} побед(-а) синего, {games.count('2')} побед(-а) красного"
    intro_text = ["Quoridor", "", a, b, b1, f"Всего сыграно {len(games)} партия(-ий), из которых", t]
    pygame.init()
    size = 650, 600
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Quoridor')
    font = pygame.font.Font(None, 30)
    font1 = pygame.font.Font(None, 80)
    text_coord = 50
    girl = AnimatedSprite(pygame.image.load("girl.png").convert(), 8, 10, 550, -10)
    for line in intro_text:
        if line == "Quoridor":
            string_rendered = font1.render(line, 1, pygame.Color('white'))
        else:
            string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        screen.fill(pygame.Color("black"))
        for line in intro_text:
            if line == "Quoridor":
                string_rendered = font1.render(line, 1, pygame.Color('white'))
            else:
                string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        text_coord = 50
        pygame.draw.rect(screen, pygame.Color('white'), (0, 299, 650, 1))
        all_sprites.draw(screen)
        horizontal_borders.update()
        vertical_borders.update()
        balls.update()
        if ticks5 % 5 == 0:
            girl.update()
        pygame.display.flip()
        clock.tick(50)
        ticks5 += 1


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
        self.steps = 0
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
            if self.blue_pos[1] == self.height - 1:
                self.final()
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
            self.steps += 1
            self.cur_person = "blue"
            if self.red_pos[1] == 0:
                self.final()

    def final(self):
        global result
        if self.cur_person == "red":
            if result == [['', 0], ['', 0]]:
                result[0] = ["blue", self.steps + 1]
            else:
                result[1] = ["blue", self.steps + 1]
        elif self.cur_person == "blue":
            if result == [['', 0], ['', 0]]:
                result[0] = ["red", self.steps]
            else:
                result[1] = ["red", self.steps]

    def render(self, screen, tick):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 1:
                    if tick == 0:
                        color = pygame.Color("white")
                    else:
                        color = pygame.Color("black")
                    pygame.draw.rect(screen, color,
                                     (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                      self.cell_size, self.cell_size))
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


def main_1():
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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if result[0] != ['', 0]:
                return
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


def main_2():
    pygame.init()
    size = 790, 790
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Quoridor')
    last_wall_press = (100, 100)

    board1 = Quoridor(11, 11)
    board1.set_view(11, 11, 70)

    ticks = 0
    ticks2 = 0
    ticks3 = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if result[1] != ['', 0]:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                last_wall_press = event.pos
                board1.get_click_wall(last_wall_press, None)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and board1.curent_wall() == 0:
                board1.get_click_move(event.pos)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and board1.curent_wall() == 1:
                board1.get_click_wall(last_wall_press, "left")
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and board1.curent_wall() == 1:
                board1.get_click_wall(last_wall_press, "right")
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and board1.curent_wall() == 1:
                board1.get_click_wall(last_wall_press, "up")
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and board1.curent_wall() == 1:
                board1.get_click_wall(last_wall_press, "down")

        screen.fill((0, 0, 0))
        board1.render(screen, ticks3)
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


if __name__ == '__main__':
    start_screen()
    main_1()
    result_screen_1()
    main_2()
    result_screen_2()
