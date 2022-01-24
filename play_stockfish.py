from stockfish import Stockfish
from chessboard import Board
import os
from time import sleep

def play_sf(): 

    os.system("cls")
    board = Board()
    board.setup_board()
    stockfish = Stockfish(path="C:/Users/fredd/Desktop/stockfish/stockfish")
    stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    play_as_white = True
    while play_as_white: 
        try:
            board.print_board_white()
            move = input("White to move ('r' to resign)\n> ")
            if move == "r": 
                print("You have resigned the game.")
                sleep(3)
                return False
            board.make_move(move)
        except KeyboardInterrupt: 
            print("\nExit program")
            break 
        
        os.system("cls")
        board.print_board_white()
        print("Stockfish to play")
        sleep(3)
        stockfish.make_moves_from_current_position([move])
        best_move = stockfish.get_best_move()
        stockfish.make_moves_from_current_position([best_move])
        board.make_move(best_move)
        os.system("cls")