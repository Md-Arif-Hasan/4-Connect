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
RADIUS = 27   # int(SQUARE_SIZE / 2 - 3)

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


def draw_board_grid(board, c, r):
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
            # game board draw without player's ball
            draw_board_grid(board, c, r)
            # draw player's ball
            draw_board_ball(board, c, r)

    pygame.display.update()
    
    
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