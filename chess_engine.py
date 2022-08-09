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
        
    def make_move(self, move):
        # find the starting square using the move notation input
        # make it blank - 
        self.board[7][5] = "-"
        
        # set piece moved to correct location
        self.board[5][5] = "P"
        
        # add move to move log using proper chess notation
        self.move_log.append(move)
        
        # swap whos turn it is to move
        self.white_to_move = not self.white_to_move
        pass
    

class Move():
    
    # maps keys to vallues
    # key : value
    ranks_to_rows = {"1" : 8, "2" : 7, "3" : 6, "4" : 5,
                     "5" : 4, "6" : 3, "7" : 2, "8" : 1}
    rows_to_ranks = {v : k for k, v in ranks_to_rows.items()}

    files_to_cols = {"a" : 1, "b" : 2, "c" : 3, "d" : 4,
                     "e" : 5, "f" : 6, "g" : 7, "h" : 8}
    cols_to_files = {v : k for k, v in files_to_cols.items()}
    
    
    def __init__(self, move, board):
        self.move = move
        
        
    def get_chess_notation(self):
        pass
        
        
    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]
    
