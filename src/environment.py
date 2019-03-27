import random
import pygame

board = [[' ' for i in range(8)] for j in range(8)]
uncovered = [[False for i in range(8)] for j in range(8)]
flags = [[False for i in range(8)] for j in range(8)]


def show_board():
    for row in board:
        print(row)


def generate_bombs(bombs):
    i = 0
    while i < bombs:
        x = random.randint(0, 7)
        y = random.randint(0, 7)
        if board[x][y] != '*':
            board[x][y] = '*'
            i += 1


def fill_numbers():
    for y in range(8):
        for x in range(8):
            if board[x][y] == '*':
                continue
            number = 0
            if y - 1 >= 0 and board[x][y - 1] == '*': number += 1
            if y + 1 < 8 and board[x][y + 1] == '*': number += 1
            if x - 1 >= 0 and board[x - 1][y] == '*': number += 1
            if x + 1 < 8 and board[x + 1][y] == '*': number += 1
            if x - 1 >= 0 and y - 1 >= 0 and board[x - 1][y - 1] == '*': number += 1
            if x + 1 < 8 and y - 1 >= 0 and board[x + 1][y - 1] == '*': number += 1
            if x - 1 >= 0 and y + 1 < 8 and board[x - 1][y + 1] == '*': number += 1
            if x + 1 < 8 and y + 1 < 8 and board[x + 1][y + 1] == '*': number += 1
            board[x][y] = number


def uncover_zeros(x, y):
    if uncovered[y][x]:
        return
    uncovered[y][x] = True
    if board[y][x] != 0:
        return
    if y - 1 >= 0: uncover_zeros(x, y - 1)
    if y + 1 < 8: uncover_zeros(x, y + 1)
    if x - 1 >= 0: uncover_zeros(x - 1, y)
    if x + 1 < 8: uncover_zeros(x + 1, y)
    if x - 1 >= 0 and y - 1 >= 0 and board[y - 1][x - 1] != 0: uncovered[y - 1][x - 1] = True
    if x + 1 < 8 and y - 1 >= 0 and board[y - 1][x + 1] != 0: uncovered[y - 1][x + 1] = True
    if x - 1 >= 0 and y + 1 < 8 and board[y + 1][x - 1] != 0: uncovered[y + 1][x - 1] = True
    if x + 1 < 8 and y + 1 < 8 and board[y + 1][x + 1] != 0: uncovered[y + 1][x + 1] = True


bombs = int(input("How many bombs to generate?"))
generate_bombs(bombs)
fill_numbers()
show_board()

pygame.init()
window = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Minesweeper")
pygame.mouse.set_visible(False)

font = pygame.font.SysFont("comicsansms", 40)
cursor = pygame.image.load("resources/cursor.png")
cursor_on_bomb = pygame.image.load("resources/cursor_on_bomb.png")
boom = pygame.image.load("resources/boom.png")
flag = pygame.image.load("resources/flag.png")
bum = pygame.mixer.Sound("resources/bum.wav")

clock = pygame.time.Clock()

x_clicked = False
end_game = False
flag_placed = False
while not x_clicked:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            x_clicked = True

    pressed = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    x = pos[0] // 50
    y = pos[1] // 50
    if pressed[0] and not end_game:
        if not uncovered[y][x] and not flags[y][x]:
            uncover_zeros(x, y)
            uncovered[y][x] = True
            if board[y][x] == '*':
                end_game = True
                bum.play()
        print(x, y)
    if pressed[2] and not end_game:
        if not uncovered[y][x] and not flag_placed:
            flags[y][x] = not flags[y][x]
        flag_placed = True
    else:
        flag_placed = False

    window.fill(0xFFFFFF)

    for y in range(8):
        for x in range(8):
            if uncovered[y][x]:
                pygame.draw.rect(window, (192, 192, 192, 192), pygame.Rect(x * 50, y * 50, 50, 50))
                if board[y][x] == '*':
                    window.blit(boom, (x * 50 - 50, y * 50 - 50))
                elif board[y][x] != 0:
                    window.blit(font.render(str(board[y][x]), True, (0, 255, 0)), (x * 50 + 15, y * 50))
            else:
                pass
            if flags[y][x]:
                window.blit(flag, (x * 50, y * 50))

    for x in range(9):
        pygame.draw.line(window, 0x000000, (x * 50, 0), (x * 50, 400), 3)
    for x in range(9):
        pygame.draw.line(window, 0x000000, (0, x * 50), (400, x * 50), 3)

    if not end_game:
        window.blit(cursor, (pos[0], pos[1] - 20))
    else:
        window.blit(cursor_on_bomb, (pos[0] - 20, pos[1] - 110))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()