"""Main menu for users to select gamemode and adjust settings."""

import play_stockfish, hotseat
import os

if __name__ == "__main__":
    game_mode = input("What would you like to play?\n1. Hotspeat Multiplayer\n2. Stockfish\n3. LAN Multiplayer\n> ")
    if game_mode == "1": 
        hotseat.play_hotseat()
    elif game_mode == "2": 
        play_stockfish.play_sf()
    elif game_mode == "3": 
        print("Not yet implemented.")
    