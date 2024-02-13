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
    intro_text = ["Quoridor", "", a, b, b1,
                  f"Всего сыграно {len(games)} партия(-ий), из которых", t]
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
        girl.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(10)
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