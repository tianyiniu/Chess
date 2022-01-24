"""Defines legal moves and looks for checks, checkmates, and stalement. 
Supports special moves such as double pawn push, castling, and en passant."""

from collections import defaultdict
from pieces import *
from copy import deepcopy

COLUMN_TO_NUM = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8}
NUM_TO_COLUMN = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f", 7: "g", 8: "h"}

def is_valid_square(square: str) -> bool: 
    if not square[0] in NUM_TO_COLUMN.values(): 
        return False
    if 0 < int(square[1]) and int(square[1]) <= 8: 
        return True
    return False

def square_to_num_board(square: str): 
    """Converts 'd4' to (4, 4)."""
    return (COLUMN_TO_NUM[square[0]], int(square[1]))

def num_board_to_square(coordinates) -> str: 
    if coordinates[1] >= 1 and coordinates[1] <= 8:
        return str(NUM_TO_COLUMN[coordinates[0]]) + str(coordinates[1])
    else: 
        raise Exception()

def build_diagonal(square): 
    """Returns a list of squares that comprises the two diagonals which overlap at the square."""
    col, rank = square_to_num_board(square)
    backwards1 = []
    forwards1 = []
    backwards2 = []
    forwards2 = []
    column_num, rank_num = col, rank
    while column_num <= 8 and rank_num <= 8: 
        forwards1.append(num_board_to_square((column_num, rank_num)))
        column_num += 1
        rank_num += 1
    column_num, rank_num = col, rank
    while column_num >= 1 and rank_num >= 1: 
        backwards1.append(num_board_to_square((column_num, rank_num)))
        column_num -= 1
        rank_num -= 1
    column_num, rank_num = col, rank
    while column_num <= 8 and rank_num >= 1: 
        forwards2.append(num_board_to_square((column_num, rank_num)))
        column_num += 1
        rank_num -= 1
    column_num, rank_num = col, rank
    while column_num >= 1 and rank_num <= 8: 
        backwards2.append(num_board_to_square((column_num, rank_num)))
        column_num -= 1
        rank_num += 1
    return (forwards1[1:], backwards1[1:], forwards2[1:], backwards2[1:])

    
def build_straight(square):
    col, rank = square_to_num_board(square) 
    backwards = []
    forwards = []
    upwards = []
    downwards = []
    column_num, rank_num = col, rank
    while column_num <= 8: 
        forwards.append(num_board_to_square((column_num, rank_num)))
        column_num += 1
    column_num, rank_num = col, rank
    while column_num >= 1: 
        backwards.append(num_board_to_square((column_num, rank_num)))
        column_num -= 1
    column_num, rank_num = col, rank
    while rank_num <= 8: 
        upwards.append(num_board_to_square((column_num, rank_num)))
        rank_num += 1
    column_num, rank_num = col, rank
    while rank_num >= 1: 
        downwards.append(num_board_to_square((column_num, rank_num)))
        rank_num -= 1
    return (forwards[1:], backwards[1:], upwards[1:], downwards[1:])


def build_knight_search(square): 
    col, rank = square_to_num_board(square)
    squares = []
    attempts = [(col + 1, rank + 2), (col - 1, rank - 2), (col - 1, rank + 2), (col + 1, rank - 2), 
                (col + 2, rank + 1), (col - 2, rank - 1), (col - 2, rank + 1), (col + 2, rank - 1)]
    for attempt in attempts: 
        try: 
            squares.append(num_board_to_square(attempt))
        except: 
            continue
    return squares


def is_in_check(board, color): 
    king_square = board.piece_positions[color]["K"][0] if color == "white" else board.piece_positions[color]["k"][0]
    k_col, k_rank = square_to_num_board(king_square)

    # Any pawn checks, pawns can only check in to positions. 
    if color == "white": 
        possible_squares = [(k_col - 1, k_rank + 1), (k_col + 1, k_rank + 1)]
    elif color == "black":
        possible_squares = [(k_col - 1, k_rank - 1), (k_col + 1, k_rank - 1)]
    for pos in possible_squares: 
        try: 
            square = num_board_to_square(pos)
            piece = board.get_piece(square)
        except: 
            continue
        if type(piece) == Empty: 
            continue
        elif type(piece) == Pawn and piece.color != color: 
            return True

    # Any diagonal checks (Bishop Queen)
    sequences = build_diagonal(king_square)
    for sequence in sequences: 
        for square in sequence: 
            piece = board.get_piece(square)
            if type(piece) == Empty: 
                continue
            elif piece.color == color: 
                break 
            elif (type(piece) == Bishop or type(piece) == Queen): 
                return True

    # Any linear checks (Rook Queen)
    sequences = build_straight(king_square)
    for sequence in sequences:
        for square in sequence: 
            piece = board.get_piece(square)
            if type(piece) == Empty: 
                continue
            elif piece.color == color: 
                break
            elif (type(piece) == Rook or type(piece) == Queen): 
                return True

    # Any knight checks
    squares = build_knight_search(king_square)
    for square in squares: 
        piece = board.get_piece(square)
        if type(piece) == Empty: 
            continue
        elif type(piece) == Knight and piece.color != color: 
            return True
    
    # Any King checks
    for pos in [(k_col + 1, k_rank + 1), (k_col - 1, k_rank - 1), (k_col + 1, k_rank - 1), (k_col - 1, k_rank + 1), 
                (k_col, k_rank + 1), (k_col, k_rank - 1), (k_col + 1, k_rank), (k_col - 1, k_rank)]:
        try: 
            square = num_board_to_square(pos)
            piece = board.get_piece(square)
            if type(piece) == Empty: 
                continue
            elif type(piece) == King: 
                return True
        except: 
            continue
    return False

def is_in_check_after_move(board, move, color):
    new_board = deepcopy(board)
    new_board.make_move(move)
    return is_in_check(new_board, color)

def legal_moves_pawn(board, piece):
    # En passant, double push
    return []

def legal_moves_rook(board, piece): 
    # Long and short castle
    return []

def legal_moves_knight(board, piece): 
    moves = []
    possible_moves = build_knight_search(piece.position)
    for move in possible_moves: 
        target_piece = board.get_piece(move)
        if target_piece.color == piece.color: 
            continue
        move_str = piece.position + move
        if not is_in_check_after_move(board, move_str, piece.color):
            moves.append(move)
    return moves

def legal_moves_bishop(board, piece): 
    moves = []
    possible_moves = 
    return []

def legal_moves_queen(board, piece): 
    return []

def legal_moves_king(board, piece): 
    # Long and short castle
    return []


def get_all_legal_moves(board, color):
    all_pieces = board.white_pieces if color == "white" else board.black_pieces
    all_moves = defaultdict(list)
    for piece in all_pieces: 
        if isinstance(piece, Pawn):
            all_moves[piece.shorthand] += legal_moves_pawn(board, piece)
        elif isinstance(piece, Rook):  
            all_moves[piece.shorthand] += legal_moves_rook(board, piece)
        elif isinstance(piece, Knight): 
            all_moves[piece.shorthand] += legal_moves_rook(board, piece)
        elif isinstance(piece, Bishop): 
            all_moves[piece.shorthand] += legal_moves_bishop(board, piece)
        elif isinstance(piece, Queen): 
            all_moves[piece.shorthand] += legal_moves_queen(board, piece)
        elif isinstance(piece, King): 
            all_moves[piece.shorthand] += legal_moves_king(board, piece)
    return all_moves

def no_moves(legal_moves): 
    for moves in legal_moves.values(): 
        if len(moves) != 0: 
            return False
    return True

def is_checkmate_stalemate(board, color): 
    is_check = is_in_check(board, color)
    legal_moves = get_all_legal_moves(board, color)
    is_moves = no_moves(legal_moves)
    if is_check and is_moves: 
        return "checkmate"
    elif not is_check and is_moves: 
        return "stalemate"
    else:  
        return legal_moves