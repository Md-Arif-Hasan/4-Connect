import associate_modules

    
def get_mid_grid(board,piece):
    array = [int(i) for i in list(board[:, associate_modules.COLUMN_COUNT//2])]
    return array.count(piece)*3

def four_grid_value(consecutive_four_grid, piece):
    value = 0

    if piece == associate_modules.PLAYER_PIECE:
        opp_piece = associate_modules.AI_PIECE
    else:
        opp_piece = associate_modules.PLAYER_PIECE
    if consecutive_four_grid.count(piece) == 4:
        value+=100
    elif consecutive_four_grid.count(piece) == 3 and consecutive_four_grid.count(associate_modules.EMPTY) == 1:
        value+=5
    elif consecutive_four_grid.count(piece) == 2 and consecutive_four_grid.count(associate_modules.EMPTY) == 2:
        value+=2
    if consecutive_four_grid.count(opp_piece) == 3 and consecutive_four_grid.count(associate_modules.EMPTY) == 1:
        value-=-4
    return value



def get_horizontal_value(board,piece):
    for r in range(associate_modules.ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(associate_modules.COLUMN_COUNT-3):
            consecutive_four_grid = row_array[c:c+4]
            return four_grid_value(consecutive_four_grid, piece)

def get_vertical_value(board,piece):
    
    for c in range(associate_modules.COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(associate_modules.ROW_COUNT-3):
            consecutive_four_grid = col_array[r:r+4]
            return four_grid_value(consecutive_four_grid, piece)
    
    

def get_positive_diagonal_value(board,piece):
    for r in range(associate_modules.ROW_COUNT-3):
        for c in range(associate_modules.COLUMN_COUNT-3):
            consecutive_four_grid = [board[r+i][c+i] for i in range(4)]
            return four_grid_value(consecutive_four_grid, piece)
    


def get_negative_diagonal_value(board,piece):
    
    for r in range(associate_modules.ROW_COUNT-3):
        for c in range(associate_modules.COLUMN_COUNT-3):
            consecutive_four_grid = [board[r+3-i][c+i] for i in range(4)]
            return four_grid_value(consecutive_four_grid, piece)
    

def moveable_columns(board):
    columns = []
    for col in range(associate_modules.COLUMN_COUNT):
        if associate_modules.is_valid_location(board, col):
            columns.append(col)
    return columns


def is_no_move_available(board):
    return associate_modules.winning_state(board, associate_modules.PLAYER_PIECE) or associate_modules.winning_state(board, associate_modules.AI_PIECE) or len(moveable_columns(board)) == 0



def heurestics_function(board,piece):
    value = 0
    
    mid_grid = get_mid_grid(board,piece)
    #print("mid grid")
    #print(mid_grid)
    #print(mid_grid.count(piece))
    value += mid_grid
    
    value += get_horizontal_value(board,piece)
    value += get_vertical_value(board,piece)
    value += get_positive_diagonal_value(board,piece)
    value += get_negative_diagonal_value(board,piece)
    return value

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = moveable_columns(board)
    is_terminal = is_no_move_available(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if associate_modules.winning_state(board, associate_modules.AI_PIECE):
                return (None, 100000000000000)
            elif associate_modules.winning_state(board, associate_modules.PLAYER_PIECE):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, heurestics_function(board, associate_modules.AI_PIECE))
    
    if maximizingPlayer:
        value = -associate_modules.math.inf
        column = associate_modules.random.choice(valid_locations)
        for col in valid_locations:
            row = associate_modules.get_next_open_row(board, col)
            b_copy = board.copy()
            associate_modules.drop_piece(b_copy, row, col, associate_modules.AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: # Minimizing player
        value = associate_modules.math.inf
        column = associate_modules.random.choice(valid_locations)
        for col in valid_locations:
            row = associate_modules.get_next_open_row(board, col)
            b_copy = board.copy()
            associate_modules.drop_piece(b_copy, row, col, associate_modules.PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value