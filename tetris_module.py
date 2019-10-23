import pygame
import time
import random
import pyautogui
import os
import sys

os.environ['SDL_VIDEO_WINDOW_POS'] = "0, 40"

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (185, 185, 185)
BLUE = (0, 0, 155)
RED = (155, 0 , 0)

FPS = 0.5
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOARDWIDTH = 10
BOARDHEIGHT = 20

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
BASICFONT = pygame.font.Font('freesansbold.ttf', 10)
STAGEFONT = pygame.font.Font('freesansbold.ttf', 15)
FPSCLOCK = pygame.time.Clock()



def terminate():
    pygame.quit()
    sys.exit()

def get_blank_board(x):
    board = []
    for _ in range(BOARDWIDTH):
        board.append([x] * BOARDHEIGHT)
    return board

def show_text_screen(text):
    title_surf = BIGFONT.render(text, True, WHITE)
    title_rect = title_surf.get_rect()
    title_rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(title_surf, title_rect)
    pygame.display.flip()
    FPSCLOCK.tick()
    time.sleep(1)

def fill_background(stage):
    DISPLAYSURF.fill(BGCOLOR)
    pygame.draw.rect(DISPLAYSURF, GRAY, [220, 75, 200, 400], 2)
    score_surf = STAGEFONT.render('Stage: %s' % stage, True, GRAY)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (WINDOWWIDTH - 300, 20)
    DISPLAYSURF.blit(score_surf, score_rect)

def get_pos_press():
    pos = pygame.mouse.get_pos()
    press = pygame.mouse.get_pressed()
    return pos, press[0]

def draw_catches(pos, press, board):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == '0':
                block = pygame.draw.rect(DISPLAYSURF, BLUE, [220 + x*20 + 1, 75+y*20 + 1, 20-1, 20-1])
            else :
                block = pygame.draw.rect(DISPLAYSURF, BLACK, [220 + x*20 + 1, 75+y*20 + 1, 20-1, 20-1])
            if block.collidepoint(pos) and press and board[x][y] == '0':
                board[x][y] = 1
    return board

def pop_up(board):
    rand_x = random.randint(0, BOARDWIDTH-1)
    rand_y = random.randint(0, BOARDHEIGHT-1)
    board[rand_x][rand_y] = '0'

def go_next_stage(stage, speed):
    stage += 1
    speed = speed * 0.95
    first = 1
    playing_time = 0
    return stage, speed, first, playing_time

def count_blue_box(board):
    counts = 0
    for i in board:
        counts += i.count('0')
    return counts

def check_for_fail(board, playing_time):
    check = False
    half = count_blue_box(board)
    if half >= 10:
        check = True
    elif playing_time >= 50:
        check = True
    return check

def use_macro(board):
    for i in range(BOARDWIDTH):
        for j in range(BOARDHEIGHT):
            if board[i][j] == '0':
                pyautogui.mouseDown(x=230+i*20, y=130+j*20)
                break

def run_game():


    speed = 1
    stage = 0
    time_taken = 0
    playing_time = 0
    first = 0

    board = get_blank_board(1)
    finished_board = get_blank_board(1)
    failed_board = get_blank_board('0')

    pop_up(board)

    while True:
        start_time = time.time()
        fill_background(stage)

        if time_taken > speed :
            pop_up(board)
            time_taken = 0
            first = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        pos, press = get_pos_press()
        board = draw_catches(pos, press, board)

        # use_macro(board)

        pygame.display.flip()

        if board == finished_board and first == 0:
            stage, speed, first, playing_time = go_next_stage(stage, speed)


        check = check_for_fail(board, playing_time)
        if check == True:
            break

        end_time = time.time()
        time_taken += (end_time - start_time)
        playing_time += (end_time - start_time)


if __name__ == '__main__':
    pygame.display.set_caption("Catch")
    show_text_screen("Catch")


    while True:
        run_game()
        DISPLAYSURF.fill(BGCOLOR)
        show_text_screen("Game Over")
