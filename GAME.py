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
SQUARE_SIZE = 60
RADIUS = 27  # int(SQUARE_SIZE / 2 - 3)

PLAYER = 0
AI = 1


EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4


GAME_OVER = False
TURN = 0


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
            # game board draw without player's ball
            draw_board_grid(c, r)
            # draw player's ball
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


def mouse_movement(event):
    pygame.draw.rect(screen, BLACK, (0, 0, boardWidth, SQUARE_SIZE))
    posX = event.pos[0]
    pygame.draw.circle(screen, RED, (posX, int(SQUARE_SIZE / 2)), RADIUS)


def winner(WHO):
    if WHO == AI_PIECE:
        message = "GG, Computer win!!"
    else:
        message = "GG, You Win!!"

    label = font.render(message, 1, RED)
    screen.blit(label, (40, 10))
    return True


def take_a_move(board, col, TURN, GAME_OVER, WHO):
    row = get_next_open_row(board, col)
    drop_piece(board, row, col, WHO)

    if winning_state(board, WHO):
        GAME_OVER = winner(WHO)

    print_board(board)
    draw_board(board)

    return TURN ^ 1, GAME_OVER


def mouse_click(event, TURN, GAME_OVER):
    pygame.draw.rect(screen, BLACK, (0, 0, boardWidth, SQUARE_SIZE))
    posX = event.pos[0]
    col = int(math.floor(posX / SQUARE_SIZE))

    if is_valid_location(board, col):
        TURN, GAME_OVER = take_a_move(board, col, TURN, GAME_OVER, PLAYER_PIECE)

    return TURN, GAME_OVER

def get_mid_grid(board):
    array = list()
    for i in range(ROW_COUNT):
        #print(i)
        array.append((board[i][COLUMN_COUNT//2]))
    return array

def four_grid_value(consecutive_four_grid, piece):
    value = 0

    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE
    else:
        opp_piece = PLAYER_PIECE
    if consecutive_four_grid.count(piece) == 4:
        value+=1000
    elif consecutive_four_grid.count(piece) == 3 and consecutive_four_grid.count(EMPTY) == 1:
        value+=10
    elif consecutive_four_grid.count(piece) == 2 and consecutive_four_grid.count(EMPTY) == 2:
        value+=4
    if consecutive_four_grid.count(opp_piece) == 3 and consecutive_four_grid.count(EMPTY) == 1:
        value-=8
    return value



def get_horizontal_value(board,piece):
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            consecutive_four_grid = row_array[c:c+4]
            return four_grid_value(consecutive_four_grid, piece)

def get_vertical_value(board,piece):
    
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            consecutive_four_grid = col_array[r:r+4]
            return four_grid_value(consecutive_four_grid, piece)
    
    

def get_positive_diagonal_value(board,piece):
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            consecutive_four_grid = [board[r+i][c+i] for i in range(4)]
            return four_grid_value(consecutive_four_grid, piece)
    


def get_negative_diagonal_value(board,piece):
    
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            consecutive_four_grid = [board[r+3-i][c+i] for i in range(4)]
            return four_grid_value(consecutive_four_grid, piece)
    

def moveable_colums(board):
	columns = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			columns.append(col)
	return columns


def is_no_move_available(board):
    return winning_state(board, PLAYER_PIECE) or winning_state(board, AI_PIECE) or len(moveable_colums(board)) == 0



def heurestics_function(board,piece):
    value = 0
    
    mid_grid = get_mid_grid(board)
    #print("mid grid")
    #print(mid_grid)
    #print(mid_grid.count(piece))
    value += mid_grid.count(piece)*3
    
    value += get_horizontal_value(board,piece)
    value += get_vertical_value(board,piece)
    value += get_positive_diagonal_value(board,piece)
    value += get_negative_diagonal_value(board,piece)
    return value
    

def game_play(board, TURN, GAME_OVER):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if TURN == PLAYER:
            if event.type == pygame.MOUSEMOTION:
                mouse_movement(event)
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                TURN, GAME_OVER = mouse_click(event, TURN, GAME_OVER)

        elif TURN == AI:
            col = random.randint(0, COLUMN_COUNT-1)
            if is_valid_location(board, col):
                TURN, GAME_OVER = take_a_move(board, col, TURN, GAME_OVER, AI_PIECE)

    return TURN, GAME_OVER


board = create_board()
flip_board(board)
print_board(board)

pygame.init()

boardWidth = COLUMN_COUNT * SQUARE_SIZE
boardHeight = (ROW_COUNT + 1) * SQUARE_SIZE

screen = pygame.display.set_mode((boardWidth, boardHeight))
draw_board(board)

font = pygame.font.SysFont("ubuntu", 35)
TURN = random.randint(PLAYER, AI)

while not GAME_OVER:
    TURN, GAME_OVER = game_play(board, TURN, GAME_OVER)

pygame.time.wait(3000)