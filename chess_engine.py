"""
Building a Chess Engine (chess_engine)

Created on Wed Aug  3 22:11:00 2022

@author: ryantvackner
"""

class GameState():
    def __init__(self):
        # initialize the board
        self.board = [
            [" ", "a", "b", "c", "d", "e", "f", "g", "h", " "],
            ["8", "r", "n", "b", "q", "k", "b", "n", "r", "8"],
            ["7", "p", "p", "p", "p", "p", "p", "p", "p", "7"],
            ["6", "-", "-", "-", "-", "-", "-", "-", "-", "6"],
            ["5", "-", "-", "-", "-", "-", "-", "-", "-", "5"],
            ["4", "-", "-", "-", "-", "-", "-", "-", "-", "4"],
            ["3", "-", "-", "-", "-", "-", "-", "-", "-", "3"],
            ["2", "P", "P", "P", "P", "P", "P", "P", "P", "2"],
            ["1", "R", "N", "B", "Q", "K", "B", "N", "R", "1"],
            [" ", "a", "b", "c", "d", "e", "f", "g", "h", " "]
            ]
        
        # white to move
        self.white_to_move = True
        
        # move log (PGN)
        self.move_log = []
