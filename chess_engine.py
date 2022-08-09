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
        
    def make_move(self, move, piece, start_sq):
        # find the starting square using the move notation input
        # make it blank - 
        move_sq = GameState.row_col(move[1], move[0])
        self.board[start_sq[0]][start_sq[1]] = "-"
        
        
        # set piece moved to correct location
        self.board[move_sq[1]][move_sq[0]] = piece
        
        # add move to move log using proper chess notation
        self.move_log.append(move)
        
        # swap whos turn it is to move
        self.white_to_move = not self.white_to_move
        pass
    
    # get all valid moves, can't put yourself in check
    def get_valid_moves(self):
        return self.get_all_possible_moves()
    
    # get all possible moves
    def get_all_possible_moves(self):
        moves = []
        piece_moved = []
        start_sq = []
        for r in range(1, 9):
            for c in range(1, 9):
                case = self.board[r][c]
                if (case.isupper() and self.white_to_move) or (case.islower() and not self.white_to_move):
                    piece = self.board[r][c]
                    if piece == 'P' or 'p':
                        self.get_pawn_moves(r, c, moves, piece_moved, start_sq)
                    elif piece == 'R' or 'r':
                        self.get_rook_moves(r, c, moves, piece_moved, start_sq)
                    elif piece == 'N' or 'n':
                        self.get_knight_moves(r, c, moves, piece_moved, start_sq)
                    elif piece == 'B' or 'b':
                        self.get_bishop_moves(r, c, moves, piece_moved, start_sq)
                    elif piece == 'Q' or 'q':
                        self.get_queen_moves(r, c, moves, piece_moved, start_sq)
                    elif piece == 'K' or 'k':
                        self.get_king_moves(r, c, moves, piece_moved, start_sq)
        return moves, piece_moved, start_sq
                        
    # pawn moves
    def get_pawn_moves(self, r, c, moves, piece_moved, start_sq):
        if self.white_to_move:
            if self.board[r-1][c] == "-": 
                moves.append(GameState.rank_file(r-1, c))
                piece_moved.append("P")
                start_sq.append((r, c))
                if r == 7 and self.board[r-2][c] == "-":
                    moves.append(GameState.rank_file(r-2, c))
                    piece_moved.append("P")
                    start_sq.append((r, c))
            if c-1 >= 1:
                if self.board[r-1][c-1].islower():
                    moves.append(GameState.rank_file(r-1, c-1))
                    piece_moved.append("P")
                    start_sq.append((r, c))
            if c+1 <= 8:
                if self.board[r-1][c+1].islower():
                    moves.append(GameState.rank_file(r-1, c+1))
                    piece_moved.append("P")
                    start_sq.append((r, c))
                    
    
    # pawn moves
    def get_rook_moves(self, r, c, moves, piece_moved, start_sq):
        pass
    
    # pawn moves
    def get_knight_moves(self, r, c, moves, piece_moved, start_sq):
        pass
    
    # pawn moves
    def get_bishop_moves(self, r, c, moves, piece_moved, start_sq):
        pass
    
    # pawn moves
    def get_queen_moves(self, r, c, moves, piece_moved, start_sq):
        pass
    
    # pawn moves
    def get_king_moves(self, r, c, moves, piece_moved, start_sq):
        pass
    
    # rank file
    def rank_file(r, c):
        # maps keys to values
        # key : value
        ranks_to_rows = {"1" : 8, "2" : 7, "3" : 6, "4" : 5,
                         "5" : 4, "6" : 3, "7" : 2, "8" : 1}
        rows_to_ranks = {v : k for k, v in ranks_to_rows.items()}

        files_to_cols = {"a" : 1, "b" : 2, "c" : 3, "d" : 4,
                         "e" : 5, "f" : 6, "g" : 7, "h" : 8}
        cols_to_files = {v : k for k, v in files_to_cols.items()}
        return cols_to_files[c] + rows_to_ranks[r]
    
    # rank file
    def row_col(r, c):
        # maps keys to values
        # key : value
        ranks_to_rows = {"1" : 8, "2" : 7, "3" : 6, "4" : 5,
                         "5" : 4, "6" : 3, "7" : 2, "8" : 1}
        rows_to_ranks = {v : k for k, v in ranks_to_rows.items()}

        files_to_cols = {"a" : 1, "b" : 2, "c" : 3, "d" : 4,
                         "e" : 5, "f" : 6, "g" : 7, "h" : 8}
        cols_to_files = {v : k for k, v in files_to_cols.items()}
        return files_to_cols[c], ranks_to_rows[r]

    
