import numpy as np
import pygame
import random
import sys
import math

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (34, 139, 34)
WHITE = (240, 240, 240)

ROW_COUNT = 6
COLUMN_COUNT = 7
GAME_OVER = False
SQUARE_SIZE = 60
RADIUS = 27  # int(SQUARE_SIZE / 2 - 3)

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))  # As empty borad
    return board


def flip_board(board):
    np.flip(board, 0)  # For game representation


def print_board(board):
    print(board)


def is_valid_location(board, col):
    return COLUMN_COUNT > col >= 0 and board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def draw_board_grid(c, r):
    pygame.draw.rect(screen, WHITE, (c * SQUARE_SIZE, boardHeight - int(r * SQUARE_SIZE + SQUARE_SIZE), SQUARE_SIZE, SQUARE_SIZE))
    pygame.draw.circle(screen, BLACK, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), boardHeight - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)


def draw_board_ball(board, c, r):
    COLOR = BLACK
    if board[r][c] == PLAYER_PIECE:
        COLOR = RED
    elif board[r][c] == AI_PIECE:
        COLOR = GREEN

    pygame.draw.circle(screen, COLOR, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), boardHeight - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            draw_board_grid(c, r)
            draw_board_ball(board, c, r)

    pygame.display.update()


def check_for_horizontal_win(board, piece):
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == board[r][c + 1] == board[r][c + 2] == board[r][c + 3] == piece:
                return True

    return False


def check_for_vertical_win(board, piece):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == board[r + 1][c] == board[r + 2][c] == board[r + 3][c] == piece:
                return True

    return False


def check_for_positively_sloped_diagonals_win(board, piece):
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == board[r + 3][c + 3] == piece:
                return True

    return False


def check_for_negatively_sloped_diagonals_win(board, piece):
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == board[r - 1][c + 1] == board[r - 2][c + 2] == board[r - 3][c + 3] == piece:
                return True

    return False


def winning_state(board, piece):
    if check_for_horizontal_win(board, piece):
        return True
    elif check_for_vertical_win(board, piece):
        return True
    elif check_for_positively_sloped_diagonals_win(board, piece):
        return True
    elif check_for_negatively_sloped_diagonals_win(board, piece):
        return True
    else:
        return False


def game_paly(board):
    # baki
    print("Game Start")


board = create_board()
flip_board(board)
print_board(board)

pygame.init()

boardWidth = COLUMN_COUNT * SQUARE_SIZE
boardHeight = (ROW_COUNT + 1) * SQUARE_SIZE

screen = pygame.display.set_mode((boardWidth, boardHeight))
draw_board(board)

font = pygame.font.SysFont("ubuntu", 75)

TURN = random.randint(PLAYER, AI)

game_paly(board)