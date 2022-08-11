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
        
        self.move_functions = {"P" : self.get_pawn_moves,
                               "p" : self.get_pawn_moves,
                               "R" : self.get_rook_moves,
                               "r" : self.get_rook_moves,
                               "N" : self.get_knight_moves,
                               "n" : self.get_knight_moves,
                               "B" : self.get_bishop_moves,
                               "b" : self.get_bishop_moves,
                               "Q" : self.get_queen_moves,
                               "q" : self.get_queen_moves,
                               "K" : self.get_king_moves,
                               "k" : self.get_king_moves}
        
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
        pgn = []
        for r in range(1, 9):
            for c in range(1, 9):
                case = self.board[r][c]
                if (case.isupper() and self.white_to_move) or (case.islower() and not self.white_to_move):
                    piece = self.board[r][c]
                    self.move_functions[piece](r, c, moves, piece_moved, start_sq, pgn)
                    
        print(moves)
        print(piece_moved)
        print(start_sq)
        print(pgn)
        return pgn, piece_moved, start_sq, moves
                        
    # pawn moves
    def get_pawn_moves(self, r, c, moves, piece_moved, start_sq, pgn):
        # white pawns
        if self.white_to_move:
            # white pawn moves forward one space
            if self.board[r-1][c] == "-": 
                moves.append(GameState.rank_file(r-1, c))
                piece_moved.append("P")
                start_sq.append((r, c))
                pgn.append(GameState.rank_file(r-1, c))
                # white pawn moves forward two spaces on first turn 
                if r == 7 and self.board[r-2][c] == "-":
                    moves.append(GameState.rank_file(r-2, c))
                    piece_moved.append("P")
                    start_sq.append((r, c))
                    pgn.append(GameState.rank_file(r-2, c))
            # white pawn capture left
            if c-1 >= 1:
                if self.board[r-1][c-1].islower():
                    moves.append(GameState.rank_file(r-1, c-1))
                    piece_moved.append("P")
                    start_sq.append((r, c))
                    pgn.append(GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r-1, c-1))
            # white pawn capture right
            if c+1 <= 8:
                if self.board[r-1][c+1].islower():
                    moves.append(GameState.rank_file(r-1, c+1))
                    piece_moved.append("P")
                    start_sq.append((r, c))
                    pgn.append(GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r-1, c+1))
        # black pawns 
        else:
            # black pawn moves forward one space
            if self.board[r+1][c] == "-": 
                moves.append(GameState.rank_file(r+1, c))
                piece_moved.append("p")
                start_sq.append((r, c))
                pgn.append(GameState.rank_file(r+1, c))
                # black pawn moves forward two spaces on first turn 
                if r == 2 and self.board[r+2][c] == "-":
                    moves.append(GameState.rank_file(r+2, c))
                    piece_moved.append("p")
                    start_sq.append((r, c))
                    pgn.append(GameState.rank_file(r+2, c))
            # black pawn capture left
            if c-1 >= 1:
                if self.board[r+1][c-1].isupper():
                    moves.append(GameState.rank_file(r+1, c-1))
                    piece_moved.append("p")
                    start_sq.append((r, c))
                    pgn.append(GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r+1, c-1))
            # black pawn capture right
            if c+1 <= 8:
                if self.board[r+1][c+1].islower():
                    moves.append(GameState.rank_file(r+1, c+1))
                    piece_moved.append("p")
                    start_sq.append((r, c))
                    pgn.append(GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r+1, c+1))
    
    # pawn moves
    def get_rook_moves(self, r, c, moves, piece_moved, start_sq, pgn):
        # white rook
        if self.white_to_move:
            # check if up the board is clear
            u = 1
            while self.board[r-u][c] == "-" or self.board[r-u][c].islower() and r-u != 0:
                moves.append(GameState.rank_file(r-u, c))
                piece_moved.append("R")
                start_sq.append((r, c))
                if self.board[r-u][c].islower():
                    pgn.append("R" + GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r-u, c))
                    break
                else:
                    pgn.append("R" + GameState.rank_file(r-u, c))
                    u += 1
            # check if down the board is clear 
            d = 1
            while self.board[r+d][c] == "-" or self.board[r+d][c].islower() and r+d != 9:
                moves.append(GameState.rank_file(r+d, c))
                piece_moved.append("R")
                start_sq.append((r, c))
                if self.board[r+d][c].islower():
                    pgn.append("R" + GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r+d, c))
                    break
                else:
                    pgn.append("R" + GameState.rank_file(r+d, c))
                    d += 1
            # check if left of the board is clear 
            l = 1
            while self.board[r][c-l] == "-" or self.board[r][c-l].islower() and c-l != 0:
                moves.append(GameState.rank_file(r, c-l))
                piece_moved.append("R")
                start_sq.append((r, c))
                if self.board[r][c-l].islower():
                    pgn.append("R" + GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r, c-l))
                    break
                else:
                    pgn.append("R" + GameState.rank_file(r, c-l))
                    l += 1
            # check if right of the board is clear 
            l = 1
            while self.board[r][c+l] == "-" or self.board[r][c+l].islower() and c+l != 9:
                moves.append(GameState.rank_file(r, c+l))
                piece_moved.append("R")
                start_sq.append((r, c))
                if self.board[r][c+l].islower():
                    pgn.append("R" + GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r, c+l))
                    break
                else:
                    pgn.append("R" + GameState.rank_file(r, c+l))
                    l += 1
        # check black rook moves
        else:
            # check if up the board is clear
            u = 1
            while self.board[r-u][c] == "-" or self.board[r-u][c].isupper() and r-u != 0:
                moves.append(GameState.rank_file(r-u, c))
                piece_moved.append("R")
                start_sq.append((r, c))
                if self.board[r-u][c].isupper():
                    pgn.append("R" + GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r-u, c))
                    break
                else:
                    pgn.append("R" + GameState.rank_file(r-u, c))
                    u += 1
            # check if down the board is clear 
            d = 1
            while self.board[r+d][c] == "-" or self.board[r+d][c].isupper() and r+d != 9:
                moves.append(GameState.rank_file(r+d, c))
                piece_moved.append("R")
                start_sq.append((r, c))
                if self.board[r+d][c].isupper():
                    pgn.append("R" + GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r+d, c))
                    break
                else:
                    pgn.append("R" + GameState.rank_file(r+d, c))
                    d += 1
            # check if left of the board is clear 
            l = 1
            while self.board[r][c-l] == "-" or self.board[r][c-l].isupper() and c-l != 0:
                moves.append(GameState.rank_file(r, c-l))
                piece_moved.append("R")
                start_sq.append((r, c))
                if self.board[r][c-l].isupper():
                    pgn.append("R" + GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r, c-l))
                    break
                else:
                    pgn.append("R" + GameState.rank_file(r, c-l))
                    l += 1
            # check if right of the board is clear 
            l = 1
            while self.board[r][c+l] == "-" or self.board[r][c+l].isupper() and c+l != 9:
                moves.append(GameState.rank_file(r, c+l))
                piece_moved.append("R")
                start_sq.append((r, c))
                if self.board[r][c+l].isupper():
                    pgn.append("R" + GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r, c+l))
                    break
                else:
                    pgn.append("R" + GameState.rank_file(r, c+l))
                    l += 1
    
    # knight moves
    # pgn is not correct
    # will need to create a pgn def that works
    def get_knight_moves(self, r, c, moves, piece_moved, start_sq, pgn):
        # white rook
        if self.white_to_move:
            if r != 1:
                if r != 2:
                    # knight top left move
                    if  c >= 2 and (self.board[r-2][c-1] == "-" or self.board[r-2][c-1].islower()):
                        moves.append(GameState.rank_file(r-2, c-1))
                        piece_moved.append("N")
                        start_sq.append((r, c))
                        if self.board[r-2][c-1].islower():
                            pgn.append("N" + GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r-2, c-1))
                        else:
                            pgn.append("N" + GameState.rank_file(r-2, c-1))
                    # knight top right move
                    if  c <= 7 and (self.board[r-2][c+1] == "-" or self.board[r-2][c+1].islower()):
                        moves.append(GameState.rank_file(r-2, c+1))
                        piece_moved.append("N")
                        start_sq.append((r, c))
                        if self.board[r-2][c+1].islower():
                            pgn.append("N" + GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r-2, c+1))
                        else:
                            pgn.append("N" + GameState.rank_file(r-2, c+1))
                # Knight left top move
                if c >= 3 and (self.board[r-1][c-2] == "-" or self.board[r-1][c-2].islower()):
                    moves.append(GameState.rank_file(r-1, c-2))
                    piece_moved.append("N")
                    start_sq.append((r, c))
                    if self.board[r-1][c-2].islower():
                        pgn.append("N" + GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r-1, c-2))
                    else:
                        pgn.append("N" + GameState.rank_file(r-1, c-2))
                # knight right top move
                if  c <= 6 and (self.board[r-1][c+2] == "-" or self.board[r-1][c+2].islower()):
                    moves.append(GameState.rank_file(r-1, c+2))
                    piece_moved.append("N")
                    start_sq.append((r, c))
                    if self.board[r-1][c+2].islower():
                        pgn.append("N" + GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r-1, c+2))
                    else:
                        pgn.append("N" + GameState.rank_file(r-1, c+2))

            if r != 8:
                if r != 7:
                    # knight bottom right move
                    if  c <= 7 and (self.board[r+2][c+1] == "-" or self.board[r+2][c+1].islower()):
                        moves.append(GameState.rank_file(r+2, c+1))
                        piece_moved.append("N")
                        start_sq.append((r, c))
                        if self.board[r+2][c+1].islower():
                            pgn.append("N" + GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r+2, c+1))
                        else:
                            pgn.append("N" + GameState.rank_file(r+2, c+1))
                    # knight bottom left move
                    if  c >= 2 and (self.board[r+2][c-1] == "-" or self.board[r+2][c-1].islower()):
                        moves.append(GameState.rank_file(r+2, c-1))
                        piece_moved.append("N")
                        start_sq.append((r, c))
                        if self.board[r+2][c-1].islower():
                            pgn.append("N" + GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r+2, c-1))
                        else:
                            pgn.append("N" + GameState.rank_file(r+2, c-1))
                # knight right bottom move
                if  c <= 6 and (self.board[r+1][c+2] == "-" or self.board[r+1][c+2].islower()):
                    moves.append(GameState.rank_file(r+1, c+2))
                    piece_moved.append("N")
                    start_sq.append((r, c))
                    if self.board[r+1][c+2].islower():
                        pgn.append("N" + GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r+1, c+2))
                    else:
                        pgn.append("N" + GameState.rank_file(r+1, c+2))
                # knight left bottom move
                if  c >= 3 and (self.board[r+1][c-2] == "-" or self.board[r+1][c-2].islower()):
                    moves.append(GameState.rank_file(r+1, c-2))
                    piece_moved.append("N")
                    start_sq.append((r, c))
                    if self.board[r+1][c-2].islower():
                        pgn.append("N" + GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r+1, c-2))
                    else:
                        pgn.append("N" + GameState.rank_file(r+1, c-2))
                    
        # black knight
        else:
            if r != 1:
                if r != 2:
                    # knight top left move
                    if  c >= 2 and (self.board[r-2][c-1] == "-" or self.board[r-2][c-1].isupper()):
                        moves.append(GameState.rank_file(r-2, c-1))
                        piece_moved.append("N")
                        start_sq.append((r, c))
                        if self.board[r-2][c-1].isupper():
                            pgn.append("N" + GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r-2, c-1))
                        else:
                            pgn.append("N" + GameState.rank_file(r-2, c-1))
                    # knight top right move
                    if  c <= 7 and (self.board[r-2][c+1] == "-" or self.board[r-2][c+1].isupper()):
                        moves.append(GameState.rank_file(r-2, c+1))
                        piece_moved.append("N")
                        start_sq.append((r, c))
                        if self.board[r-2][c+1].isupper():
                            pgn.append("N" + GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r-2, c+1))
                        else:
                            pgn.append("N" + GameState.rank_file(r-2, c+1))
                # Knight left top move
                if c >= 3 and (self.board[r-1][c-2] == "-" or self.board[r-1][c-2].isupper()):
                    moves.append(GameState.rank_file(r-1, c-2))
                    piece_moved.append("N")
                    start_sq.append((r, c))
                    if self.board[r-1][c-2].isupper():
                        pgn.append("N" + GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r-1, c-2))
                    else:
                        pgn.append("N" + GameState.rank_file(r-1, c-2))
                # knight right top move
                if  c <= 6 and (self.board[r-1][c+2] == "-" or self.board[r-1][c+2].isupper()):
                    moves.append(GameState.rank_file(r-1, c+2))
                    piece_moved.append("N")
                    start_sq.append((r, c))
                    if self.board[r-1][c+2].isupper():
                        pgn.append("N" + GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r-1, c+2))
                    else:
                        pgn.append("N" + GameState.rank_file(r-1, c+2))

            if r != 8:
                if r != 7:
                    # knight bottom right move
                    if  c <= 7 and (self.board[r+2][c+1] == "-" or self.board[r+2][c+1].isupper()):
                        moves.append(GameState.rank_file(r+2, c+1))
                        piece_moved.append("N")
                        start_sq.append((r, c))
                        if self.board[r+2][c+1].isupper():
                            pgn.append("N" + GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r+2, c+1))
                        else:
                            pgn.append("N" + GameState.rank_file(r+2, c+1))
                    # knight bottom left move
                    if  c >= 2 and (self.board[r+2][c-1] == "-" or self.board[r+2][c-1].isupper()):
                        moves.append(GameState.rank_file(r+2, c-1))
                        piece_moved.append("N")
                        start_sq.append((r, c))
                        if self.board[r+2][c-1].isupper():
                            pgn.append("N" + GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r+2, c-1))
                        else:
                            pgn.append("N" + GameState.rank_file(r+2, c-1))
                # knight right bottom move
                if  c <= 6 and (self.board[r+1][c+2] == "-" or self.board[r+1][c+2].isupper()):
                    moves.append(GameState.rank_file(r+1, c+2))
                    piece_moved.append("N")
                    start_sq.append((r, c))
                    if self.board[r+1][c+2].isupper():
                        pgn.append("N" + GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r+1, c+2))
                    else:
                        pgn.append("N" + GameState.rank_file(r+1, c+2))
                # knight left bottom move
                if  c >= 3 and (self.board[r+1][c-2] == "-" or self.board[r+1][c-2].isupper()):
                    moves.append(GameState.rank_file(r+1, c-2))
                    piece_moved.append("N")
                    start_sq.append((r, c))
                    if self.board[r+1][c-2].isupper():
                        pgn.append("N" + GameState.rank_file(r, c)[0] + "x" + GameState.rank_file(r+1, c-2))
                    else:
                        pgn.append("N" + GameState.rank_file(r+1, c-2))
    
    # pawn moves
    def get_bishop_moves(self, r, c, moves, piece_moved, start_sq, pgn):
        pass
    
    # pawn moves
    def get_queen_moves(self, r, c, moves, piece_moved, start_sq, pgn):
        pass
    
    # pawn moves
    def get_king_moves(self, r, c, moves, piece_moved, start_sq, pgn):
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
    

    def get_pgn(self, moves, piece_moved, start_sq):
        # temporarily good
        # still need to add it check, promotions, and checkmate
        pgn = []
        if self.white_to_move:
            for i in range(0, len(moves)):
                for j in range(0, len(moves)):
                    # are the moves to the same square?
                    if (moves[i] == moves[j]):
                        # the two pieces that are moving there the same?
                        if (piece_moved[i] == piece_moved[j]):
                            # the two pieces that are moved on the same file?
                            if (GameState.rank_file(start_sq[i][0], start_sq[i][1])[0] == GameState.rank_file(start_sq[j][0], start_sq[j][1])[0]):
                                # check if a piece was captured
                                if(moves[i].islower()):
                                    pgn.append(piece_moved[i] + start_sq[i][1] + "x" + moves[i])
                                else:
                                    pgn.append(piece_moved[i] + start_sq[i][1] + moves[i])
                            else:
                                # check if a piece was caputred
                                if(moves[i].islower()):
                                    pgn.append(piece_moved[i] + start_sq[i][0] + "x" + moves[i])
                                else:
                                    pgn.append(piece_moved[i] + start_sq[i][0] + moves[i])
                        else:
                            # check if a piece was captured
                            if(moves[i].islower()):
                                pgn.append(piece_moved[i] + "x" + moves[i])
                            else:
                                pgn.append(piece_moved[i] + moves[i])
                    else:
                        # check if pawn was moved
                        if (piece_moved[i] == "P"):
                            # check if a piece was captured
                            if(moves[i].islower()):
                                pgn.append(start_sq[i][0] + "x" + moves[i])
                            else:
                                pgn.append(moves[i])
                        else:
                            # check if a piece was captured
                            if(moves[i].islower()):
                                pgn.append(piece_moved[i] + "x" + moves[i])
                            else:
                                pgn.append(piece_moved[i] + moves[i])
        else:
            pass
        return pgn
    
