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
            ["5", "-", "-", "-", "-", "K", "-", "-", "-", "5"],
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
                    self.move_functions[piece](r, c, moves, piece_moved, start_sq)
                    
        print(moves)
        pgn = GameState.get_pgn(self, moves, piece_moved, start_sq)
        print(pgn)
        return pgn, piece_moved, start_sq, moves
                        
    # pawn moves
    def get_pawn_moves(self, r, c, moves, piece_moved, start_sq):
        # white pawns
        if self.white_to_move:
            i = 0
            count = 0
            # white pawn moves forward one space
            if self.board[r-1][c] == "-": 
                moves.append(GameState.rank_file(r-1, c))
                count += 1
                # white pawn moves forward two spaces on first turn 
                if r == 7 and self.board[r-2][c] == "-":
                    moves.append(GameState.rank_file(r-2, c))
                    count += 1
            # white pawn capture left
            if c-1 >= 1:
                if self.board[r-1][c-1].islower():
                    moves.append(GameState.rank_file(r-1, c-1))
                    count += 1
            # white pawn capture right
            if c+1 <= 8:
                if self.board[r-1][c+1].islower():
                    moves.append(GameState.rank_file(r-1, c+1))
                    count += 1
            while i < count:
                piece_moved.append("P")
                start_sq.append((r, c))
                i += 1
                
        # black pawns 
        else:
            i = 0
            count = 0
            # black pawn moves forward one space
            if self.board[r+1][c] == "-": 
                moves.append(GameState.rank_file(r+1, c))
                count += 1
                # black pawn moves forward two spaces on first turn 
                if r == 2 and self.board[r+2][c] == "-":
                    moves.append(GameState.rank_file(r+2, c))
                    count += 1
            # black pawn capture left
            if c-1 >= 1:
                if self.board[r+1][c-1].isupper():
                    moves.append(GameState.rank_file(r+1, c-1))
                    count += 1
            # black pawn capture right
            if c+1 <= 8:
                if self.board[r+1][c+1].islower():
                    moves.append(GameState.rank_file(r+1, c+1))
                    count += 1
            while i < count:
                piece_moved.append("p")
                start_sq.append((r, c))
                i += 1
    
    # pawn moves
    def get_rook_moves(self, r, c, moves, piece_moved, start_sq):
        # white rook
        if self.white_to_move:
            # using north, south, east, west cordinates
            i = 0
            count = 0
            # check if up the board is clear
            n = 1
            while self.board[r-n][c] == "-" or self.board[r-n][c].islower() and r-n != 0:
                moves.append(GameState.rank_file(r-n, c))
                count += 1
                if self.board[r-n][c].islower():
                    break
                else:
                    n += 1
            # check if down the board is clear 
            s = 1
            while self.board[r+s][c] == "-" or self.board[r+s][c].islower() and r+s != 9:
                moves.append(GameState.rank_file(r+s, c))
                count += 1
                if self.board[r+s][c].islower():
                    break
                else:
                    s += 1
            # check if left of the board is clear 
            w = 1
            while self.board[r][c-w] == "-" or self.board[r][c-w].islower() and c-w != 0:
                moves.append(GameState.rank_file(r, c-w))
                count += 1
                if self.board[r][c-w].islower():
                    break
                else:
                    w += 1
            # check if right of the board is clear 
            e = 1
            while self.board[r][c+e] == "-" or self.board[r][c+e].islower() and c+e != 9:
                moves.append(GameState.rank_file(r, c+e))
                count += 1
                if self.board[r][c+e].islower():
                    break
                else:
                    e += 1
            while i < count:
                piece_moved.append("R")
                start_sq.append((r, c))
                i += 1
        # check black rook moves
        else:
            # using north, south, east, west cordinates
            i = 0
            count = 0
            # check if up the board is clear
            n = 1
            while self.board[r-n][c] == "-" or self.board[r-n][c].isupper() and r-n != 0:
                moves.append(GameState.rank_file(r-n, c))
                count += 1
                if self.board[r-n][c].isupper():
                    break
                else:
                    n += 1
            # check if down the board is clear 
            s = 1
            while self.board[r+s][c] == "-" or self.board[r+s][c].isupper() and r+s != 9:
                moves.append(GameState.rank_file(r+s, c))
                count += 1
                if self.board[r+s][c].isupper():
                    break
                else:
                    s += 1
            # check if left of the board is clear 
            w = 1
            while self.board[r][c-w] == "-" or self.board[r][c-w].isupper() and c-w != 0:
                moves.append(GameState.rank_file(r, c-w))
                count += 1
                if self.board[r][c-w].isupper():
                    break
                else:
                    w += 1
            # check if right of the board is clear 
            e = 1
            while self.board[r][c+e] == "-" or self.board[r][c+e].isupper() and c+e != 9:
                moves.append(GameState.rank_file(r, c+e))
                count += 1
                if self.board[r][c+e].isupper():
                    break
                else:
                    e += 1
            while i < count:
                piece_moved.append("r")
                start_sq.append((r, c))
                i += 1
    
    # knight moves
    # pgn is not correct
    # will need to create a pgn def that works
    def get_knight_moves(self, r, c, moves, piece_moved, start_sq):
        # white rook
        if self.white_to_move:
            i = 0
            count = 0
            if r != 1:
                if r != 2:
                    # knight top left move
                    if  c >= 2 and (self.board[r-2][c-1] == "-" or self.board[r-2][c-1].islower()):
                        moves.append(GameState.rank_file(r-2, c-1))
                        count += 1
                    # knight top right move
                    if  c <= 7 and (self.board[r-2][c+1] == "-" or self.board[r-2][c+1].islower()):
                        moves.append(GameState.rank_file(r-2, c+1))
                        count += 1
                # Knight left top move
                if c >= 3 and (self.board[r-1][c-2] == "-" or self.board[r-1][c-2].islower()):
                    moves.append(GameState.rank_file(r-1, c-2))
                    count += 1
                # knight right top move
                if  c <= 6 and (self.board[r-1][c+2] == "-" or self.board[r-1][c+2].islower()):
                    moves.append(GameState.rank_file(r-1, c+2))
                    count += 1

            if r != 8:
                if r != 7:
                    # knight bottom right move
                    if  c <= 7 and (self.board[r+2][c+1] == "-" or self.board[r+2][c+1].islower()):
                        moves.append(GameState.rank_file(r+2, c+1))
                        count += 1
                    # knight bottom left move
                    if  c >= 2 and (self.board[r+2][c-1] == "-" or self.board[r+2][c-1].islower()):
                        moves.append(GameState.rank_file(r+2, c-1))
                        count += 1
                # knight right bottom move
                if  c <= 6 and (self.board[r+1][c+2] == "-" or self.board[r+1][c+2].islower()):
                    moves.append(GameState.rank_file(r+1, c+2))
                    count += 1
                # knight left bottom move
                if  c >= 3 and (self.board[r+1][c-2] == "-" or self.board[r+1][c-2].islower()):
                    moves.append(GameState.rank_file(r+1, c-2))
                    count += 1
                    
            while i < count:
                piece_moved.append("N")
                start_sq.append((r, c))
                i += 1
                    
        # black knight
        else:
            i = 0
            count = 0
            if r != 1:
                if r != 2:
                    # knight top left move
                    if  c >= 2 and (self.board[r-2][c-1] == "-" or self.board[r-2][c-1].isupper()):
                        moves.append(GameState.rank_file(r-2, c-1))
                        count += 1
                    # knight top right move
                    if  c <= 7 and (self.board[r-2][c+1] == "-" or self.board[r-2][c+1].isupper()):
                        moves.append(GameState.rank_file(r-2, c+1))
                        count += 1
                # Knight left top move
                if c >= 3 and (self.board[r-1][c-2] == "-" or self.board[r-1][c-2].isupper()):
                    moves.append(GameState.rank_file(r-1, c-2))
                    count += 1
                # knight right top move
                if  c <= 6 and (self.board[r-1][c+2] == "-" or self.board[r-1][c+2].isupper()):
                    moves.append(GameState.rank_file(r-1, c+2))
                    count += 1

            if r != 8:
                if r != 7:
                    # knight bottom right move
                    if  c <= 7 and (self.board[r+2][c+1] == "-" or self.board[r+2][c+1].isupper()):
                        moves.append(GameState.rank_file(r+2, c+1))
                        count += 1
                    # knight bottom left move
                    if  c >= 2 and (self.board[r+2][c-1] == "-" or self.board[r+2][c-1].isupper()):
                        moves.append(GameState.rank_file(r+2, c-1))
                        count += 1
                # knight right bottom move
                if  c <= 6 and (self.board[r+1][c+2] == "-" or self.board[r+1][c+2].isupper()):
                    moves.append(GameState.rank_file(r+1, c+2))
                    count += 1
                # knight left bottom move
                if  c >= 3 and (self.board[r+1][c-2] == "-" or self.board[r+1][c-2].isupper()):
                    moves.append(GameState.rank_file(r+1, c-2))
                    count += 1
                
                while i < count:
                    piece_moved.append("n")
                    start_sq.append((r, c))
                    i += 1
    
    # bishop moves
    def get_bishop_moves(self, r, c, moves, piece_moved, start_sq):
        # white to move
        if self.white_to_move:
            # using north, south, east, west cordinates
            i = 0
            count = 0
            # check if top left is clear
            n = 1
            w = 1
            while self.board[r+n][c-w] == "-" or self.board[r+n][c-w].islower() and r+n != 9 and c-w != 0:
                moves.append(GameState.rank_file(r+n, c-w))
                count += 1
                if self.board[r+n][c-w].islower():
                    break
                else:
                    n += 1
                    w += 1
            # check if top right is clear
            n = 1
            e = 1
            while self.board[r+n][c+e] == "-" or self.board[r+n][c+e].islower() and r+n != 9 and c+e != 9:
                moves.append(GameState.rank_file(r+n, c+e))
                count += 1
                if self.board[r+n][c+e].islower():
                    break
                else:
                    n += 1
                    e += 1
            # check if bottom left is clear
            s = 1
            w = 1
            while self.board[r-s][c-w] == "-" or self.board[r-s][c-w].islower() and r-s != 0 and c-w != 0:
                moves.append(GameState.rank_file(r-s, c-w))
                count += 1
                if self.board[r-s][c-w].islower():
                    break
                else:
                    s += 1
                    w += 1
            # check if bottom left is clear
            s = 1
            w = 1
            while self.board[r-s][c+w] == "-" or self.board[r-s][c+w].islower() and r-s != 0 and c+w != 9:
                moves.append(GameState.rank_file(r-s, c+w))
                count += 1
                if self.board[r-s][c+w].islower():
                    break
                else:
                    s += 1
                    w += 1
            # append the moves
            while i < count:
                piece_moved.append("B")
                start_sq.append((r, c))
                i += 1
        else:
            # using north, south, east, west cordinates
            i = 0
            count = 0
            # check if top left is clear
            n = 1
            w = 1
            while self.board[r+n][c-w] == "-" or self.board[r+n][c-w].isupper() and r+n != 9 and c-w != 0:
                moves.append(GameState.rank_file(r+n, c-w))
                count += 1
                if self.board[r+n][c-w].isupper():
                    break
                else:
                    n += 1
                    w += 1
            # check if top right is clear
            n = 1
            e = 1
            while self.board[r+n][c+e] == "-" or self.board[r+n][c+e].isupper() and r+n != 9 and c+e != 9:
                moves.append(GameState.rank_file(r+n, c+e))
                count += 1
                if self.board[r+n][c+e].isupper():
                    break
                else:
                    n += 1
                    e += 1
            # check if bottom left is clear
            s = 1
            w = 1
            while self.board[r-s][c-w] == "-" or self.board[r-s][c-w].isupper() and r-s != 0 and c-w != 0:
                moves.append(GameState.rank_file(r-s, c-w))
                count += 1
                if self.board[r-s][c-w].isupper():
                    break
                else:
                    s += 1
                    w += 1
            # check if bottom left is clear
            s = 1
            w = 1
            while self.board[r-s][c+w] == "-" or self.board[r-s][c+w].isupper() and r-s != 0 and c+w != 9:
                moves.append(GameState.rank_file(r-s, c+w))
                count += 1
                if self.board[r-s][c+w].isupper():
                    break
                else:
                    s += 1
                    w += 1
            # append the moves
            while i < count:
                piece_moved.append("b")
                start_sq.append((r, c))
                i += 1
    
    # queen moves
    def get_queen_moves(self, r, c, moves, piece_moved, start_sq):
        # white queen
        if self.white_to_move:
            # using north, south, east, west cordinates
            i = 0
            count = 0
            # check if up the board is clear
            n = 1
            while self.board[r-n][c] == "-" or self.board[r-n][c].islower() and r-n != 0:
                moves.append(GameState.rank_file(r-n, c))
                count += 1
                if self.board[r-n][c].islower():
                    break
                else:
                    n += 1
            # check if down the board is clear 
            s = 1
            while self.board[r+s][c] == "-" or self.board[r+s][c].islower() and r+s != 9:
                moves.append(GameState.rank_file(r+s, c))
                count += 1
                if self.board[r+s][c].islower():
                    break
                else:
                    s += 1
            # check if left of the board is clear 
            w = 1
            while self.board[r][c-w] == "-" or self.board[r][c-w].islower() and c-w != 0:
                moves.append(GameState.rank_file(r, c-w))
                count += 1
                if self.board[r][c-w].islower():
                    break
                else:
                    w += 1
            # check if right of the board is clear 
            e = 1
            while self.board[r][c+e] == "-" or self.board[r][c+e].islower() and c+e != 9:
                moves.append(GameState.rank_file(r, c+e))
                count += 1
                if self.board[r][c+e].islower():
                    break
                else:
                    e += 1
            # check if top left is clear
            n = 1
            w = 1
            while self.board[r+n][c-w] == "-" or self.board[r+n][c-w].islower() and r+n != 9 and c-w != 0:
                moves.append(GameState.rank_file(r+n, c-w))
                count += 1
                if self.board[r+n][c-w].islower():
                    break
                else:
                    n += 1
                    w += 1
            # check if top right is clear
            n = 1
            e = 1
            while self.board[r+n][c+e] == "-" or self.board[r+n][c+e].islower() and r+n != 9 and c+e != 9:
                moves.append(GameState.rank_file(r+n, c+e))
                count += 1
                if self.board[r+n][c+e].islower():
                    break
                else:
                    n += 1
                    e += 1
            # check if bottom left is clear
            s = 1
            w = 1
            while self.board[r-s][c-w] == "-" or self.board[r-s][c-w].islower() and r-s != 0 and c-w != 0:
                moves.append(GameState.rank_file(r-s, c-w))
                count += 1
                if self.board[r-s][c-w].islower():
                    break
                else:
                    s += 1
                    w += 1
            # check if bottom left is clear
            s = 1
            w = 1
            while self.board[r-s][c+w] == "-" or self.board[r-s][c+w].islower() and r-s != 0 and c+w != 9:
                moves.append(GameState.rank_file(r-s, c+w))
                count += 1
                if self.board[r-s][c+w].islower():
                    break
                else:
                    s += 1
                    w += 1
            # append the moves
            while i < count:
                piece_moved.append("Q")
                start_sq.append((r, c))
                i += 1
        # black queen
        else:
            # using north, south, east, west cordinates
            i = 0
            count = 0
            # check if up the board is clear
            n = 1
            while self.board[r-n][c] == "-" or self.board[r-n][c].isupper() and r-n != 0:
                moves.append(GameState.rank_file(r-n, c))
                count += 1
                if self.board[r-n][c].isupper():
                    break
                else:
                    n += 1
            # check if down the board is clear 
            s = 1
            while self.board[r+s][c] == "-" or self.board[r+s][c].isupper() and r+s != 9:
                moves.append(GameState.rank_file(r+s, c))
                count += 1
                if self.board[r+s][c].isupper():
                    break
                else:
                    s += 1
            # check if left of the board is clear 
            w = 1
            while self.board[r][c-w] == "-" or self.board[r][c-w].isupper() and c-w != 0:
                moves.append(GameState.rank_file(r, c-w))
                count += 1
                if self.board[r][c-w].isupper():
                    break
                else:
                    w += 1
            # check if right of the board is clear 
            e = 1
            while self.board[r][c+e] == "-" or self.board[r][c+e].isupper() and c+e != 9:
                moves.append(GameState.rank_file(r, c+e))
                count += 1
                if self.board[r][c+e].isupper():
                    break
                else:
                    e += 1
            # check if top left is clear
            n = 1
            w = 1
            while self.board[r+n][c-w] == "-" or self.board[r+n][c-w].isupper() and r+n != 9 and c-w != 0:
                moves.append(GameState.rank_file(r+n, c-w))
                count += 1
                if self.board[r+n][c-w].isupper():
                    break
                else:
                    n += 1
                    w += 1
            # check if top right is clear
            n = 1
            e = 1
            while self.board[r+n][c+e] == "-" or self.board[r+n][c+e].isupper() and r+n != 9 and c+e != 9:
                moves.append(GameState.rank_file(r+n, c+e))
                count += 1
                if self.board[r+n][c+e].isupper():
                    break
                else:
                    n += 1
                    e += 1
            # check if bottom left is clear
            s = 1
            w = 1
            while self.board[r-s][c-w] == "-" or self.board[r-s][c-w].isupper() and r-s != 0 and c-w != 0:
                moves.append(GameState.rank_file(r-s, c-w))
                count += 1
                if self.board[r-s][c-w].isupper():
                    break
                else:
                    s += 1
                    w += 1
            # check if bottom left is clear
            s = 1
            w = 1
            while self.board[r-s][c+w] == "-" or self.board[r-s][c+w].isupper() and r-s != 0 and c+w != 9:
                moves.append(GameState.rank_file(r-s, c+w))
                count += 1
                if self.board[r-s][c+w].isupper():
                    break
                else:
                    s += 1
                    w += 1
            # append the moves
            while i < count:
                piece_moved.append("q")
                start_sq.append((r, c))
                i += 1
    
    # king moves
    def get_king_moves(self, r, c, moves, piece_moved, start_sq):
        # white king 
        if self.white_to_move:
            i = 0
            count = 0
            # white king up
            if self.board[r-1][c] == "-" or self.board[r-1][c].islower() and r-1 != 0: 
                moves.append(GameState.rank_file(r-1, c))
                count += 1
            # white king down 
            if self.board[r+1][c] == "-" or self.board[r+1][c].islower() and r+1 != 9: 
                moves.append(GameState.rank_file(r+1, c))
                count += 1
            # white king left
            if self.board[r][c-1] == "-" or self.board[r][c-1].islower() and c-1 != 0: 
                moves.append(GameState.rank_file(r, c-1))
                count += 1
            # white king right
            if self.board[r][c+1] == "-" or self.board[r][c+1].islower() and c+1 != 9: 
                moves.append(GameState.rank_file(r, c+1))
                count += 1
            # white king up right
            if self.board[r-1][c+1] == "-" or self.board[r-1][c+1].islower() and r-1 != 0 and c+1 != 9: 
                moves.append(GameState.rank_file(r-1, c+1))
                count += 1
            # white king up left
            if self.board[r-1][c-1] == "-" or self.board[r-1][c-1].islower() and r-1 != 0 and c-1 != 0: 
                moves.append(GameState.rank_file(r-1, c-1))
                count += 1
            # white king down left
            if self.board[r+1][c-1] == "-" or self.board[r+1][c-1].islower() and r+1 != 9 and c-1 != 0: 
                moves.append(GameState.rank_file(r+1, c-1))
                count += 1
            # white king down right
            if self.board[r+1][c+1] == "-" or self.board[r+1][c+1].islower() and r+1 != 9 and c+1 != 9: 
                moves.append(GameState.rank_file(r+1, c+1))
                count += 1

            while i < count:
                piece_moved.append("K")
                start_sq.append((r, c))
                i += 1
    
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
        # also still need to work out PGN for 3 queens on the board
        rank_file = []
        board_sq = []
        for i in range(0, len(start_sq)):
            rank_file.append(GameState.rank_file(start_sq[i][0], start_sq[i][1]))
        for i in range(0, len(moves)):
            board_sq.append(GameState.row_col(moves[i][1], moves[i][0]))
        
        pgn = []
        if self.white_to_move:
            for i in range(0, len(moves)):
                flag = False
                for j in range(0, len(moves)):
                    # check if indexes are the same
                    if i != j:
                        # are the moves to the same square?
                        if moves[i] == moves[j]:
                            # the two pieces that are moving there the same?
                            if piece_moved[i] == piece_moved[j]:
                                # the two pieces that are moved on the same file?
                                ifile = GameState.rank_file(start_sq[i][0], start_sq[i][1])[0]
                                jfile = GameState.rank_file(start_sq[j][0], start_sq[j][1])[0]
                                if ifile == jfile:
                                    check = False
                                    for k in range(0, len(moves)):
                                        if i != k and j != k:
                                            if moves[i] == moves[k]:
                                                if piece_moved[i] == piece_moved[k]:
                                                    # check if a piece was captured
                                                    if self.board[board_sq[i][1]][board_sq[i][0]].islower():
                                                        pgn.append(piece_moved[i] + rank_file[i] + "x" + moves[i])
                                                        check = True
                                                        flag = True
                                                        break
                                                    else:
                                                        pgn.append(piece_moved[i] + rank_file[i] + moves[i])
                                                        check = True 
                                                        flag = True
                                                        break
                                    # check if you broke the for loop
                                    if check:
                                        break
                                    # check if a piece was captured
                                    if self.board[board_sq[i][1]][board_sq[i][0]].islower():
                                        pgn.append(piece_moved[i] + rank_file[i][1] + "x" + moves[i])
                                        flag = True
                                        break
                                    else:
                                        pgn.append(piece_moved[i] + rank_file[i][1] + moves[i])
                                        flag = True
                                        break
                                else:
                                    check = False
                                    for k in range(0, len(moves)):
                                        if i != k and j != k:
                                            if moves[i] == moves[k]:
                                                if piece_moved[i] == piece_moved[k]:
                                                    # check if a piece was captured
                                                    if self.board[board_sq[i][1]][board_sq[i][0]].islower():
                                                        pgn.append(piece_moved[i] + rank_file[i] + "x" + moves[i])
                                                        check = True
                                                        flag = True
                                                        break
                                                    else:
                                                        pgn.append(piece_moved[i] + rank_file[i] + moves[i])
                                                        check = True
                                                        flag = True
                                                        break
                                    # check if you broke the for loop
                                    if check:
                                        break
                                    # check if a piece was caputred
                                    if self.board[board_sq[i][1]][board_sq[i][0]].islower():
                                        if piece_moved[i] == "P":
                                            pgn.append(rank_file[i][0] + "x" + moves[i])
                                            flag = True
                                            break
                                        else:
                                            pgn.append(piece_moved[i] + rank_file[i][0] + "x" + moves[i])
                                            flag = True
                                            break
                                    else:
                                        pgn.append(piece_moved[i] + rank_file[i][0] + moves[i])
                                        flag = True
                                        break
                if not flag:
                    # check if pawn was moved
                    if piece_moved[i] == "P":
                        # check if rank is 2
                        # promotion
                        
                        
                        
                        # check if a piece was captured
                        if self.board[board_sq[i][1]][board_sq[i][0]].islower():
                            pgn.append(rank_file[i][0] + "x" + moves[i])
                        else:
                            pgn.append(moves[i])
                    else:
                        # check if a piece was captured
                        if self.board[board_sq[i][1]][board_sq[i][0]].islower():
                            pgn.append(piece_moved[i] + "x" + moves[i])
                        else:
                            pgn.append(piece_moved[i] + moves[i])
                
                # added in if statement to check for check and checkmate
        else:
            pass
        return pgn
    
