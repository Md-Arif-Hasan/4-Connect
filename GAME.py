
import AI_move
from associate_modules import PLAYER

def create_board():
    board = AI_move.associate_modules.np.zeros((AI_move.associate_modules.ROW_COUNT, AI_move.associate_modules.COLUMN_COUNT))  # As empty borad
    return board


def flip_board(board):
    AI_move.associate_modules.np.flip(board, 0)  # For game representation


def print_board(board):
    print(board)




def draw_board_grid(c, r):
    AI_move.associate_modules.pygame.draw.rect(screen, AI_move.associate_modules.WHITE, (c * AI_move.associate_modules.SQUARE_SIZE, boardHeight - int(r * AI_move.associate_modules.SQUARE_SIZE + AI_move.associate_modules.SQUARE_SIZE), AI_move.associate_modules.SQUARE_SIZE, AI_move.associate_modules.SQUARE_SIZE))
    AI_move.associate_modules.pygame.draw.circle(screen, AI_move.associate_modules.BLACK, (int(c * AI_move.associate_modules.SQUARE_SIZE + AI_move.associate_modules.SQUARE_SIZE / 2), boardHeight - int(r * AI_move.associate_modules.SQUARE_SIZE + AI_move.associate_modules.SQUARE_SIZE / 2)), AI_move.associate_modules.RADIUS)


def draw_board_ball(board, c, r):
    COLOR = AI_move.associate_modules.BLACK
    if board[r][c] == AI_move.associate_modules.PLAYER_PIECE:
        COLOR = AI_move.associate_modules.RED
    elif board[r][c] == AI_move.associate_modules.AI_PIECE:
        COLOR = AI_move.associate_modules.GREEN

    AI_move.associate_modules.pygame.draw.circle(screen, COLOR, (int(c * AI_move.associate_modules.SQUARE_SIZE + AI_move.associate_modules.SQUARE_SIZE / 2), boardHeight - int(r * AI_move.associate_modules.SQUARE_SIZE + AI_move.associate_modules.SQUARE_SIZE / 2)), AI_move.associate_modules.RADIUS)


def draw_board(board):
    for c in range(AI_move.associate_modules.COLUMN_COUNT):
        for r in range(AI_move.associate_modules.ROW_COUNT):
            # game board draw without player's ball
            draw_board_grid(c, r)
            # draw player's ball
            draw_board_ball(board, c, r)

    AI_move.associate_modules.pygame.display.update()



def winner(WHO):
    if WHO == AI_move.associate_modules.AI_PIECE:
        message = "GG, Computer win!!"
    else:
        message = "GG, You Win!!"

    label = font.render(message, 1, AI_move.associate_modules.RED)
    screen.blit(label, (40, 10))
    return True


def take_a_move(board, col, TURN, GAME_OVER, WHO):
    row = AI_move.associate_modules.get_next_open_row(board, col)
    AI_move.associate_modules.drop_piece(board, row, col, WHO)

    if AI_move.associate_modules.winning_state(board, WHO):
        GAME_OVER = winner(WHO)

    print_board(board)
    draw_board(board)

    return TURN ^ 1, GAME_OVER


def mouse_click(event, TURN, GAME_OVER):
    AI_move.associate_modules.pygame.draw.rect(screen, AI_move.associate_modules.BLACK, (0, 0, boardWidth, AI_move.associate_modules.SQUARE_SIZE))
    posX = event.pos[0]
    col = int(AI_move.associate_modules.math.floor(posX / AI_move.associate_modules.SQUARE_SIZE))

    if AI_move.associate_modules.is_valid_location(board, col):
        TURN, GAME_OVER = take_a_move(board, col, TURN, GAME_OVER, AI_move.associate_modules.PLAYER_PIECE)

    return TURN, GAME_OVER

def mouse_movement(event):
    AI_move.associate_modules.pygame.draw.rect(screen, AI_move.associate_modules.BLACK, (0, 0, boardWidth, AI_move.associate_modules.SQUARE_SIZE))
    posX = event.pos[0]
    AI_move.associate_modules.pygame.draw.circle(screen, AI_move.associate_modules.RED, (posX, int(AI_move.associate_modules.SQUARE_SIZE / 2)), AI_move.associate_modules.RADIUS)

def game_play(board, TURN, GAME_OVER):
    for event in AI_move.associate_modules.pygame.event.get():
        if event.type == AI_move.associate_modules.pygame.QUIT:
            AI_move.associate_modules.sys.exit()

        if TURN == AI_move.associate_modules.PLAYER:
            if event.type == AI_move.associate_modules.pygame.MOUSEMOTION:
                mouse_movement(event)
            AI_move.associate_modules.pygame.display.update()
            if event.type == AI_move.associate_modules.pygame.MOUSEBUTTONDOWN:
                TURN, GAME_OVER = mouse_click(event, TURN, GAME_OVER)

        elif TURN == AI_move.associate_modules.AI:
            col, value = AI_move.minimax(board,5,-AI_move.associate_modules.math.inf,AI_move.associate_modules.math.inf,True)
            if AI_move.associate_modules.is_valid_location(board, col):
                TURN, GAME_OVER = take_a_move(board, col, TURN, GAME_OVER, AI_move.associate_modules.AI_PIECE)

    return TURN, GAME_OVER
    
board = create_board()
AI_move.associate_modules.pygame.init()
    
boardWidth = AI_move.associate_modules.COLUMN_COUNT * AI_move.associate_modules.SQUARE_SIZE
boardHeight = (AI_move.associate_modules.ROW_COUNT + 1) * AI_move.associate_modules.SQUARE_SIZE

screen = AI_move.associate_modules.pygame.display.set_mode((boardWidth, boardHeight))
font = AI_move.associate_modules.pygame.font.SysFont("ubuntu", 35)



def main():

    #board = create_board()

    flip_board(board)
    print_board(board)

   

   
    draw_board(board)

    AI_move.associate_modules.TURN = AI_move.associate_modules.random.randint(AI_move.associate_modules.PLAYER, AI_move.associate_modules.AI)

    while not AI_move.associate_modules.GAME_OVER:
        AI_move.associate_modules.TURN, AI_move.associate_modules.GAME_OVER = game_play(board, AI_move.associate_modules.TURN, AI_move.associate_modules.GAME_OVER)

    AI_move.associate_modules.pygame.time.wait(1000)

