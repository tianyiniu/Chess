"""Initialize and play a game of chess."""

from chessboard import Board
import os
from time import sleep
from moves import is_checkmate_stalemate, is_in_check
from pieces import *
# from mouse_move import mouse_move_black, mouse_move_white, calibrate_window

class Game(): 
    def __init__(self, board=None):
        self.board = board 
        if self.board == None: 
            self.board = Board()
            self.board.setup_board()
        
    def make_move_white(self, status_message=None):
        if status_message: 
            print(status_message)
        print("White to play")
        self.board.print_board_white()

        # Check for checkmate or stalemate.
        legal_moves = is_checkmate_stalemate(self.board, "white")
        if legal_moves == "checkmate": 
            print("White has been checkmated")
            sleep(3)
            return False
        elif legal_moves == "stalemate": 
            print("White has been stalemated")
            sleep(3)
            return False

        # White plays a move or resigns
        move = input("White to move ('r' to resign)\n> ")
        #move = mouse_move_white()
        if move == "r": 
            print("White has resigned the game.")
            sleep(3)
            return False

        # Checks if white's move is valid.
        piece = self.board.get_piece(move[:2])
        if isinstance(piece, Empty): 
            print("That is an empty square")
            return self.make_move_white()
        elif piece.color != "white": 
            print("That is not your piece!")
            return self.make_move_white()
        elif move not in legal_moves[piece.shorthand]:
            print("That is not a legal move!")
            return self.make_move_white() 

        os.system("cls")

        # Additional implicit moves if en passant, promotation, or castles
        self.board.make_move(move)
        if type(piece) == Pawn and move[-1] == "8":
            self.board.promote(move[2:], "white")
        return move
    
    def make_move_black(self, status_message=None): 
        if status_message: 
            print(status_message)
        print("Black to play")
        self.board.print_board_black()

        legal_moves = is_checkmate_stalemate(self.board, "black")
        if legal_moves == "checkmate": 
            print("Black has been checkmated")
            sleep(3)
            return False
        elif legal_moves == "stalemate": 
            print("Black has been stalemated")
            sleep(3)
            return False

        move = input("Black to move ('r' to resign)\n> ")
        #move = mouse_move_black()

        if move == "r": 
            print("Black has resigned the game.")
            sleep(3)
            return False
        piece = self.board.get_piece(move[:2])
        if isinstance(piece, Empty):
            print("That is an empty square")
            return self.make_move_black()
        elif piece.color != "black":
            print("That is not your piece!")
            return self.make_move_black()
        elif move not in legal_moves[piece.shorthand]:
            print("That is not a legal move!")
            return self.make_move_black() 

        os.system("cls")
        self.board.make_move(move)
        if type(piece) == Pawn and move[-1] == "1":
            self.board.promote(move[2:], "black")
        return move

    def play_game(self):
        #self.board.print_board_white()
        #calibrate_window()
        os.system("cls")
        play = True
        # Loops completes when 1) One side resigns 2) One side checkmakes 3) One side stalemates 
        while play: 
            try:

                # White to play
                print("Is white in check: ", is_in_check(self.board, "white"))
                # White makes move
                result = self.make_move_white()
                if result == False: 
                    print("Black wins")
                    break


                # Black to play
                print("Is Black in check: ", is_in_check(self.board, "black"))
                # Black makes move
                result = self.make_move_black()
                if result == False: 
                    print("White wins")
                    break

            except KeyboardInterrupt: 
                print("\nExit program")
                break 