"""Implements chess board and provides board-level operations: show/print board, move pieces. """

from copy import copy, deepcopy
from tkinter.font import BOLD
from pieces import *
NUMS_BLANK = "12345678" # Used for setting up board from FEN
NUM_TO_COLUMN = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f", 7: "g", 8: "h"}

class Board: 
    def __init__(self): 
        """Initialize board."""
        self.squares = [[Empty() for i in range(8)] for n in range(8)]
        self.rank_dict = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        self.white_pieces = []
        self.black_pieces = []
        self.piece_positions = {"white": {"P": [], "R": [], "N": [], "B": [], "Q": [], "K": []}, "black": {"p": [], "r": [], "n": [], "b": [], "q": [], "k": []}}
    
    def print_line(self, rank, board): 
        """Formats and prints a single line of the chess board."""
        piece_names = [piece.shorthand for piece in board[rank-1]]
        print(f"{rank} | " + " | ".join(piece_names) + " |")
        print("  |---|---|---|---|---|---|---|---|")

    def print_board_white(self):
        """Print chess from white's perspective.""" 
        print("  |---|---|---|---|---|---|---|---|")
        for i in range(8, 0, -1): 
           self.print_line(i, self.squares)
        print("    a   b   c   d   e   f   g   h  ")

    def print_board_black(self):
        """Prints board from black's perspective."""
        print("  |---|---|---|---|---|---|---|---|") 
        temp = deepcopy(self.squares)
        for i in range(8): 
            temp[i] = temp[i][::-1]
        for i in range(1, 9): 
           self.print_line(i, temp)
        print("   h   g   f   e   d   c   b   a  ")
    
    def setup_board(self): 
        """Set up a new game board."""
        # Set up white pieces
        c = "white"
        self.squares[1] = [Pawn(c, "a2"), Pawn(c, "b2"), Pawn(c, "c2"), Pawn(c, "d2"), Pawn(c, "e2"), Pawn(c, "f2"), Pawn(c, "g2"), Pawn(c, "h2")]
        self.squares[0] = [Rook(c, "a1"), Knight(c, "b1"), Bishop(c, "c1"), Queen(c, "d1"), King(c, "e1"), Bishop(c, "f1"), Knight(c, "g1"), Rook(c, "h1")]

        # Set up black pieces
        c = "black"
        self.squares[6] = [Pawn(c, "a7"), Pawn(c, "b7"), Pawn(c, "c7"), Pawn(c, "d7"), Pawn(c, "e7"), Pawn(c, "f7"), Pawn(c, "g7"), Pawn(c, "h7")]
        self.squares[7] = [Rook(c, "a8"), Knight(c, "b8"), Bishop(c, "c8"), Queen(c, "d8"), King(c, "e8"), Bishop(c, "f8"), Knight(c, "g8"), Rook(c, "h8")]

        # Initializes list contains pieces on the board. Will change as pieces get taken.
        self.white_pieces = copy(self.squares[0]) + copy(self.squares[1])
        self.black_pieces = copy(self.squares[7]) + copy(self.squares[6])

        # Update board pieces positions
        for piece in self.white_pieces: 
            self.piece_positions["white"][piece.shorthand].append(piece.position)
        for piece in self.black_pieces: 
            self.piece_positions["black"][piece.shorthand].append(piece.position)

    def get_piece(self, pos: str):
        """Takes in a square ('d4') and returns a piece object."""
        pos_column, pos_row = self.rank_dict[pos[0]], int(pos[1]) - 1
        return self.squares[pos_row][pos_column]

    def make_move(self, move): 
        """Makes a move on the chess board. Ex: 'd2d4'."""

        # Initialize coordinates
        pos1_rank, pos1_row = self.rank_dict[move[0]], int(move[1]) - 1
        pos2_rank, pos2_row = self.rank_dict[move[2]], int(move[3]) - 1

        # Locate piece and increment move counter
        chess_piece = self.get_piece(move[:2])
        self.piece_positions[chess_piece.color][chess_piece.shorthand].remove(chess_piece.position)
        chess_piece.position = move[2:]
        self.piece_positions[chess_piece.color][chess_piece.shorthand].append(chess_piece.position)
        chess_piece.move_counter += 1

        # If opponenent picece at target location, delete piece
        opp_piece = self.get_piece(move[2:])
        if not isinstance(opp_piece, Empty): 
            if opp_piece in self.white_pieces: 
                self.white_pieces.remove(opp_piece)
            else: 
                self.black_pieces.remove(opp_piece)
            self.piece_positions[opp_piece.color][opp_piece.shorthand].remove(opp_piece.position)

        # Change piece position
        self.squares[pos2_row][pos2_rank] = chess_piece
        self.squares[pos1_row][pos1_rank] = Empty()


    def promote(self, square, color): 
        """Call promote when a pawn reaches 8th rank for white and 1st rank for black."""
        piece = self.get_piece(square)
        promote_choice = input("Promote pawn to\n1.Queen\n2.Rook\n3.Bishop\n4.Knight\n> ")
        if promote_choice == "1": 
            new_piece = Queen(color, square)
        elif promote_choice == "2": 
            new_piece = Rook(color, square)
        elif promote_choice == "3": 
            new_piece = Bishop(color, square)
        elif promote_choice == "4": 
            new_piece = Knight(color, square)
        else: 
            print("Invalid selection. Enter 1, 2, 3, or 4.")
            return self.promote(self, square, color)
        
        # Update self.pieces and self.piece_positions
        if color == "white": 
            if type(piece) != Empty: 
                self.white_pieces.remove(piece)
            self.white_pieces.append(new_piece)
        else: 
            if type(piece) != Empty:
                self.black_pieces.remove(piece)
            self.white_pieces.append(new_piece)

        if type(piece) != Empty:
            self.piece_positions[color][piece.shorthand].remove(piece.position)
        self.piece_positions[color][new_piece.shorthand].append(piece.position)
        return 


    def piece_from_shorthand(self, shorthand):
        """Returns a new piece given it's shorthand notation."""
        if shorthand.lower() == "p": 
            if shorthand.isupper(): 
                return Pawn(color="white")
            else: 
                return Pawn(color="black")
        elif shorthand.lower() == "r": 
            if shorthand.isupper(): 
                return Rook(color="white")
            else: 
                return Rook(color="black")
        elif shorthand.lower() == "b": 
            if shorthand.isupper(): 
                return Bishop(color="white")
            else: 
                return Bishop(color="black")
        elif shorthand.lower() == "n": 
            if shorthand.isupper(): 
                return Knight(color="white")
            else: 
                return Knight(color="black")
        elif shorthand.lower() == "q": 
            if shorthand.isupper(): 
                return Queen(color="white")
            else: 
                return Queen(color="black")
        elif shorthand.lower() == "k": 
            if shorthand.isupper(): 
                return King(color="white")
            else: 
                return King(color="black")
        return Empty()

    def create_empty_pieces(self, num):
        "Returns a list of 'Empty' pieces length a certain length. Used to initialize empty squares from FEN."
        if not isinstance(num, int): 
            num = int(num)
        lst = []
        for i in range(num): 
            lst.append(Empty())
        return lst


    def import_from_fen(self, fen:str='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1') -> bool: 
        """Setup board according to FEN string, defaults to initial position. 
        Ex. 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'"""
        piece_placement, active_color, casting_availability, en_passent, halfmove_clock, fullmove_clock = fen.split(" ")
        lines = piece_placement.split("/")

        # Sets up board.
        for i in range(len(self.squares)):
            pieces = lines[7 - i]
            lst = []
            for piece in pieces: 
                if piece in NUMS_BLANK: 
                    lst += self.create_empty_pieces(piece)
                else: 
                    piece_obj = self.piece_from_shorthand(piece)
                    lst.append(piece_obj)
                    if piece_obj.color == "white": 
                        self.white_pieces.append(piece_obj)
                    else: 
                        self.black_pieces.append(piece_obj)

            self.squares[i] = lst
        
        # Sets up piece.position for each piece.
        for rank_num in range(8):
            for col_num in range(8): 
                piece = self.squares[rank_num][col_num]
                piece.position = NUM_TO_COLUMN[rank_num + 1] + str(col_num + 1)
        
        # Setup piece position dictionary. 
        for pieces in [self.white_pieces, self.black_pieces]:
            for piece in pieces: 
                self.piece_positions[piece.color][piece.shorthand].append(piece.position)
                
        white_to_move = True if active_color == "w" else False
        return white_to_move