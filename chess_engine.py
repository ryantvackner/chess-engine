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
            ["8", "r", "-", "-", "-", "k", "-", "-", "r", "8"],
            ["7", "-", "-", "-", "-", "-", "-", "-", "-", "7"],
            ["6", "-", "-", "-", "-", "-", "-", "-", "-", "6"],
            ["5", "-", "-", "-", "-", "-", "-", "-", "-", "5"],
            ["4", "-", "-", "-", "-", "-", "-", "-", "-", "4"],
            ["3", "-", "-", "-", "-", "-", "-", "-", "-", "3"],
            ["2", "-", "-", "-", "-", "-", "-", "-", "-", "2"],
            ["1", "R", "-", "-", "-", "K", "-", "-", "R", "1"],
            [" ", "a", "b", "c", "d", "e", "f", "g", "h", " "]
            ]

        self.move_functions = {"P": self.get_pawn_moves,
                               "p": self.get_pawn_moves,
                               "R": self.get_rook_moves,
                               "r": self.get_rook_moves,
                               "N": self.get_knight_moves,
                               "n": self.get_knight_moves,
                               "B": self.get_bishop_moves,
                               "b": self.get_bishop_moves,
                               "Q": self.get_queen_moves,
                               "q": self.get_queen_moves,
                               "K": self.get_king_moves,
                               "k": self.get_king_moves}

        # king location
        self.white_king_location = (8, 5)
        self.black_king_location = (1, 5)

        # other king stuuf
        self.in_check = False
        self.pins = []
        self.checks = []
        self.checkmate = False
        self.stalemate = False
        self.enpassant_possible = ()
        self.current_castle_rights = CastleRights(True, True, True, True)
        self.castle_rights_log = [self.current_castle_rights]

        # white to move
        self.white_to_move = True

        # move log (PGN)
        self.move_log = []

    def make_move(self, move, piece, start_sq):   
        # move square
        move_sq = GameState.row_col(move[1], move[0])  
        
        # check if move is castling
        if piece == "O-O":
            if self.white_to_move:
                self.board[8][8] = "-"
                self.board[8][7] = "K"
                self.board[8][6] = "R"
                self.white_king_location = (move_sq[0], move_sq[1])
                self.current_castle_rights.wks = False
                self.current_castle_rights.wqs = False
            else:
                self.board[1][8] = "-"
                self.board[1][7] = "k"
                self.board[1][6] = "r"
                self.black_king_location = (move_sq[0], move_sq[1])
                self.current_castle_rights.bks = False
                self.current_castle_rights.bqs = False
            self.move_log.append(piece)
        elif piece == "O-O-O":
            if self.white_to_move:
                self.board[8][1] = "-"
                self.board[8][3] = "K"
                self.board[8][4] = "R"
                self.white_king_location = (move_sq[0], move_sq[1])
                self.current_castle_rights.wks = False
                self.current_castle_rights.wqs = False
            else:
                self.board[1][1] = "-"
                self.board[1][3] = "k"
                self.board[1][4] = "r"
                self.black_king_location = (move_sq[0], move_sq[1])
                self.current_castle_rights.bks = False
                self.current_castle_rights.bqs = False
            self.move_log.append(piece)
        else:
            # set piece moved to correct location
            self.board[move_sq[0]][move_sq[1]] = piece
            # add move to move log using proper chess notation
            self.move_log.append(move)
        
        # blacks enpassant
        white_enpassant = False
        
        # make it blank -     
        self.board[start_sq[0]][start_sq[1]] = "-"
        
        # take the pawn for en passant
        if move_sq == self.enpassant_possible:
            if self.white_to_move:
                self.board[move_sq[0]+1][move_sq[1]] = "-"
            else:
                self.board[move_sq[0]-1][move_sq[1]] = "-"
            self.enpassant_possible = ()
        elif white_enpassant == self.white_to_move:
            self.enpassant_possible = ()

        # swap whos turn it is to move
        self.white_to_move = not self.white_to_move

        # update kings location
        if piece == "K":
            self.white_king_location = (move_sq[0], move_sq[1])
            self.current_castle_rights.wks = False
            self.current_castle_rights.wqs = False
        elif piece == "k":
            self.black_king_location = (move_sq[0], move_sq[1])
            self.current_castle_rights.bks = False
            self.current_castle_rights.bqs = False
            
        # update castling rights if rooks moved
        if piece == "R":
            # white queen side 
            if start_sq[0] == 8:
                if start_sq[1] == 1:
                    self.current_castle_rights.wqs = False
                elif start_sq[1] == 8:
                    self.current_castle_rights.wks = False
        elif piece == "r":
            # white queen side 
            if start_sq[0] == 1:
                if start_sq[1] == 1:
                    self.current_castle_rights.bqs = False
                elif start_sq[1] == 8:
                    self.current_castle_rights.bks = False
            
            
        # check if en passent is possible
        # white pawn
        if piece == "P":
            if start_sq[0] == 7 and move_sq[0] == 5:
                self.enpassant_possible = (6, start_sq[1])
                white_enpassant = False
        # black pawn 
        elif piece == "p":
            if start_sq[0] == 2 and move_sq[0] == 4:
                self.enpassant_possible = (3, start_sq[1])
                white_enpassant = True

            
                

    # get all valid moves, can't put yourself in check
    def get_valid_moves(self):
        pgn = []
        piece_moved = []
        start_sq = []
        rank_file_move = []
        moves = []
        
        # get pins and checks
        self.in_check, self.pins, self.checks = self.check_for_pins_and_checks()
        
        # whose move is it?
        if self.white_to_move:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]
        
        # if we are in check, limit the total number of moves
        if self.in_check:
            moves = self.get_all_possible_moves()
            pgn = []
            piece_moved = []
            start_sq = []
            rank_file_move = []
            
            # only 1 check, block or move king
            if len(self.checks) == 1:
                check = self.checks[0]
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col]
                valid_squares = []
                if self.white_to_move:
                    if piece_checking == "n":
                        checking_sq = (check_row, check_col)
                        valid_squares.append(checking_sq)
                    else:
                        for i in range(1, 8):
                            valid_square = (king_row + check[2] * i, king_col + check[3] * i)
                            valid_squares.append(valid_square)
                            if valid_square[0] == check_row and valid_square[1] == check_col:
                                break
                else:
                    if piece_checking == "N":
                        checking_sq = (check_row, check_col)
                        valid_squares.append(checking_sq)
                    else:
                        for i in range(1, 8):
                            valid_square = (king_row + check[2] * i, king_col + check[3] * i)
                            valid_squares.append(valid_square)
                            if valid_square[0] == check_row and valid_square[1] == check_col:
                                break
                print(moves)
                # get rid of moves that dont block check
                for i in range(len(moves[0]) - 1, -1, -1):
                    if self.white_to_move:
                        if moves[1][i] == "K":
                            pgn.append(moves[0][i])
                            piece_moved.append(moves[1][i])
                            start_sq.append(moves[2][i])
                            rank_file_move.append(moves[3][i])
                    else:
                        if moves[1][i] == "k":
                            pgn.append(moves[0][i])
                            piece_moved.append(moves[1][i])
                            start_sq.append(moves[2][i])
                            rank_file_move.append(moves[3][i])
                    if GameState.row_col(moves[3][i][1], moves[3][i][0]) in valid_squares:
                        pgn.append(moves[0][i])
                        piece_moved.append(moves[1][i])
                        start_sq.append(moves[2][i])
                        rank_file_move.append(moves[3][i])

            # double check
            else:
                for i in range(len(moves[0]) - 1, -1, -1):
                    if self.white_to_move:
                        if moves[1][i] == "K":
                            pgn.append(moves[0][i])
                            piece_moved.append(moves[1][i])
                            start_sq.append(moves[2][i])
                            rank_file_move.append(moves[3][i])
                    else:
                        if moves[1][i] == "k":
                            pgn.append(moves[0][i])
                            piece_moved.append(moves[1][i])
                            start_sq.append(moves[2][i])
                            rank_file_move.append(moves[3][i])
        # not in check
        else:
            return self.get_all_possible_moves()
        
        return pgn, piece_moved, start_sq, rank_file_move

    # get all possible moves
    def get_all_possible_moves(self):
        pgn = []
        piece_moved = []
        start_sq = []
        moves = []
        for r in range(1, 9):
            for c in range(1, 9):
                case = self.board[r][c]
                if (case.isupper() and self.white_to_move) or (case.islower() and not self.white_to_move):
                    piece = self.board[r][c]
                    self.move_functions[piece](r, c, moves, piece_moved, start_sq)


        pgn = GameState.get_pgn(self, moves, piece_moved, start_sq)
        return pgn, piece_moved, start_sq, moves

    # returns if the player is in check, a list of pins, and list of checks
    def check_for_pins_and_checks(self):
        # init variables
        pins = []
        checks = []
        in_check = False
        
        # color to move
        color = True if self.white_to_move else False
        
        # determine the start_row and start_col based on whose turn it is
        if color:
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]
            
        # king directions
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        
        # iterate through kings directions
        for j in range(len(directions)):
            d = directions[j]
            possible_pin = ()
            # at a distance of eight squares away from the king
            for i in range(1, 8):
                end_row = start_row + d[0] * i
                end_col = start_col + d[1] * i
                # ensure we are checking only squares on the board
                if 1 <= end_row < 9 and 1 <= end_col < 9:
                    end_piece = self.board[end_row][end_col]
                    end_piece_color = self.board[end_row][end_col].isupper()
                    # the color of the piece in our path is the same as the king and that piece is not a king
                    if end_piece_color == color and ((color and end_piece.upper() != "K") or (not color and end_piece.upper() != "k")) and end_piece != "-":
                        if possible_pin == ():
                            possible_pin = (end_row, end_col, d[0], d[1])
                        else:
                            break
                    elif end_piece != "-":
                        type = end_piece.upper()
                        if (0 <= j <= 3 and type == "R") or \
                                (4 <= j <= 7 and type == "B") or \
                                (i == 1 and type == "P" and ((end_piece_color and 6 <= j <= 7) or (not end_piece_color and 4 <= j <= 5))) or \
                                (type == "Q") or (i == 1 and type == "K"):
                            # no piece blocking so check
                            if possible_pin == ():
                                in_check = True
                                checks.append((end_row, end_col, d[0], d[1]))
                                break
                            # piece blocking so pin
                            else:
                                pins.append(possible_pin)
                                break
                        # enemy piece not applying check
                        else:
                            break
                # off board
                else:
                    break
        

        # check knight moves
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knight_moves:
            end_row = start_row + m[0]
            end_col = start_col + m[1]
            if 1 <= end_row < 9 and 1 <= end_col < 9:
                end_piece = self.board[end_row][end_col]
                if color: #if whites turn to move
                    if end_piece == "n":
                        in_check = True
                        checks.append((end_row, end_col, m[0], m[1]))
                else:
                    if end_piece == "N":
                        in_check = True
                        checks.append((end_row, end_col, m[0], m[1]))
        
        return in_check, pins, checks



    # pawn moves
    def get_pawn_moves(self, r, c, moves, piece_moved, start_sq):
        # pinned piece check
        piece_pinned = False
        pin_direction = ()
        
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        # white pawns
        if self.white_to_move:
            i=0
            count=0
            # white pawn moves forward one space
            if self.board[r-1][c] == "-":
                if not piece_pinned or pin_direction == (-1, 0):
                    if r-1 == 1:
                        for z in range(4):
                            moves.append(GameState.rank_file(r-1, c))
                            start_sq.append((r, c))
                        piece_moved.append("Q")
                        piece_moved.append("R")
                        piece_moved.append("B")
                        piece_moved.append("N")
                    else:
                        moves.append(GameState.rank_file(r-1, c))
                        count += 1
                        # white pawn moves forward two spaces on first turn
                        if r == 7 and self.board[r-2][c] == "-":
                            moves.append(GameState.rank_file(r-2, c))
                            count += 1
            # white pawn capture left
            if c-1 >= 1:
                if self.board[r-1][c-1].islower():
                    if not piece_pinned or pin_direction == (-1, -1):
                        if r-1 == 1:
                            for z in range(4):
                                moves.append(GameState.rank_file(r-1, c-1))
                                start_sq.append((r, c))
                            piece_moved.append("Q")
                            piece_moved.append("R")
                            piece_moved.append("B")
                            piece_moved.append("N")
                        else:
                            moves.append(GameState.rank_file(r-1, c-1))
                            count += 1
                # en passant left
                if self.enpassant_possible == (r-1, c-1):
                    if not piece_pinned or pin_direction == (-1, -1):
                        moves.append(GameState.rank_file(r-1, c-1))
                        count += 1
            # white pawn capture right
            if c+1 <= 8:
                if self.board[r-1][c+1].islower():
                    if not piece_pinned or pin_direction == (-1, 1):
                        if r-1 == 1:
                            for z in range(4):
                                moves.append(GameState.rank_file(r-1, c+1))
                                start_sq.append((r, c))
                            piece_moved.append("Q")
                            piece_moved.append("R")
                            piece_moved.append("B")
                            piece_moved.append("N")
                        else:
                            moves.append(GameState.rank_file(r-1, c+1))
                            count += 1
                # en passant right 
                if self.enpassant_possible == (r-1, c+1):
                    if not piece_pinned or pin_direction == (-1, 1):
                        moves.append(GameState.rank_file(r-1, c+1))
                        count += 1
            # append piece moved
            while i < count:
                piece_moved.append("P")
                start_sq.append((r, c))
                i += 1

        # black pawns
        else:
            i=0
            count=0
            # black pawn moves forward one space
            if self.board[r+1][c] == "-":
                if not piece_pinned or pin_direction == (1, 0):
                    if r+1 == 8:
                        for z in range(4):
                            moves.append(GameState.rank_file(r+1, c))
                            start_sq.append((r, c))
                        piece_moved.append("q")
                        piece_moved.append("r")
                        piece_moved.append("b")
                        piece_moved.append("n")
                    else:
                        moves.append(GameState.rank_file(r+1, c))
                        count += 1
                        # black pawn moves forward two spaces on first turn
                        if r == 2 and self.board[r+2][c] == "-":
                            moves.append(GameState.rank_file(r+2, c))
                            count += 1
            # black pawn capture left
            if c-1 >= 1:
                if self.board[r+1][c-1].isupper():
                    if not piece_pinned or pin_direction == (1, -1):
                        if r+1 == 8:
                            for z in range(4):
                                moves.append(GameState.rank_file(r+1, c-1))
                                start_sq.append((r, c))
                            piece_moved.append("q")
                            piece_moved.append("r")
                            piece_moved.append("b")
                            piece_moved.append("n")
                        else:
                            moves.append(GameState.rank_file(r+1, c-1))
                            count += 1
                # en passant left
                if self.enpassant_possible == (r+1, c-1):
                    if not piece_pinned or pin_direction == (1, -1):
                        moves.append(GameState.rank_file(r+1, c-1))
                        count += 1
            # black pawn capture right
            if c+1 <= 8:
                if self.board[r+1][c+1].isupper():
                    if not piece_pinned or pin_direction == (1, 1):
                        if r+1 == 8:
                            for z in range(4):
                                moves.append(GameState.rank_file(r+1, c+1))
                                start_sq.append((r, c))
                            piece_moved.append("q")
                            piece_moved.append("r")
                            piece_moved.append("b")
                            piece_moved.append("n")
                        else:
                            moves.append(GameState.rank_file(r+1, c+1))
                            count += 1
                # en passant right
                if self.enpassant_possible == (r+1, c+1):
                    if not piece_pinned or pin_direction == (1, 1):
                        moves.append(GameState.rank_file(r+1, c+1))
                        count += 1
            while i < count:
                piece_moved.append("p")
                start_sq.append((r, c))
                i += 1


    # rook moves
    def get_rook_moves(self, r, c, moves, piece_moved, start_sq):
        # pinned piece check
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c] != "Q":
                    self.pins.remove(self.pins[i])
                break
        
        direction=((-1, 0), (0, -1), (1, 0), (0, 1))
        color=True if self.white_to_move else False
        for d in direction:
            for i in range(1, 8):
                end_row=r + d[0] * i
                end_col=c + d[1] * i
                if 1 <= end_row < 9 and 1 <= end_col < 9:
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        end_piece=self.board[end_row][end_col]
                        end_piece_color=self.board[end_row][end_col].islower()
                        if end_piece == "-":
                            moves.append(GameState.rank_file(end_row, end_col))
                            piece_moved.append("R" if color else "r")
                            start_sq.append((r, c))
                        elif end_piece_color == color:
                            moves.append(GameState.rank_file(end_row, end_col))
                            piece_moved.append("R" if color else "r")
                            start_sq.append((r, c))
                            break
                        else:
                            break
                else:
                    break



    # knight moves
    def get_knight_moves(self, r, c, moves, piece_moved, start_sq):
        # pinned piece check
        piece_pinned = False
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break
        
        direction=((-2, -1), (-2, 1), (-1, -2), (-1, 2),
                   (1, -2), (1, 2), (2, -1), (2, 1))
        color=True if self.white_to_move else False
        for d in direction:
            end_row=r + d[0]
            end_col=c + d[1]
            if 1 <= end_row < 9 and 1 <= end_col < 9:
                if not piece_pinned:
                    end_piece=self.board[end_row][end_col]
                    end_piece_color=self.board[end_row][end_col].islower()
                    if end_piece == "-" or end_piece_color == color:
                        moves.append(GameState.rank_file(end_row, end_col))
                        piece_moved.append("N" if color else "n")
                        start_sq.append((r, c))

    # bishop moves
    def get_bishop_moves(self, r, c, moves, piece_moved, start_sq):
        # pinned piece check
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        direction=((-1, -1), (-1, 1), (1, -1), (1, 1))
        color=True if self.white_to_move else False
        for d in direction:
            for i in range(1, 8):
                end_row=r + d[0] * i
                end_col=c + d[1] * i
                if 1 <= end_row < 9 and 1 <= end_col < 9:
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        end_piece=self.board[end_row][end_col]
                        end_piece_color=self.board[end_row][end_col].islower()
                        if end_piece == "-":
                            moves.append(GameState.rank_file(end_row, end_col))
                            piece_moved.append("B" if color else "b")
                            start_sq.append((r, c))
                        elif end_piece_color == color:
                            moves.append(GameState.rank_file(end_row, end_col))
                            piece_moved.append("B" if color else "b")
                            start_sq.append((r, c))
                            break
                        else:
                            break
                else:
                    break

    # queen moves
    def get_queen_moves(self, r, c, moves, piece_moved, start_sq):
        # pinned piece check
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        direction=((-1, 0), (0, -1), (1, 0), (0, 1),
                   (-1, -1), (-1, 1), (1, -1), (1, 1))
        color=True if self.white_to_move else False
        for d in direction:
            for i in range(1, 8):
                end_row=r + d[0] * i
                end_col=c + d[1] * i
                if 1 <= end_row < 9 and 1 <= end_col < 9:
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        end_piece=self.board[end_row][end_col]
                        end_piece_color=self.board[end_row][end_col].islower()
                        if end_piece == "-":
                            moves.append(GameState.rank_file(end_row, end_col))
                            piece_moved.append("Q" if color else "q")
                            start_sq.append((r, c))
                        elif end_piece_color == color:
                            moves.append(GameState.rank_file(end_row, end_col))
                            piece_moved.append("Q" if color else "q")
                            start_sq.append((r, c))
                            break
                        else:
                            break
                else:
                    break

    # king moves
    def get_king_moves(self, r, c, moves, piece_moved, start_sq):
        # directions the king can move
        direction=((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        
        # color to move
        color=True if self.white_to_move else False
        
        # iterate through all king movements
        for i in range(8):
            end_row = r + direction[i][0]
            end_col = c + direction[i][1]
            
            # ensure king stays on the board
            if 1 <= end_row < 9 and 1 <= end_col < 9:
                end_piece=self.board[end_row][end_col]
                end_piece_color=self.board[end_row][end_col].islower()
                
                # space looking to move to is empty or enemy piece
                if end_piece == "-" or end_piece_color == color:
                    
                    # temporarily move king to that location 
                    if color:
                        king_start_row = self.white_king_location[0]
                        king_start_col = self.white_king_location[1]
                        self.board[self.white_king_location[0]][self.white_king_location[1]] = '-'
                        self.white_king_location = (end_row, end_col)
                    else:
                        king_start_row = self.black_king_location[0]
                        king_start_col = self.black_king_location[1]
                        self.board[self.black_king_location[0]][self.black_king_location[1]] = '-'
                        self.black_king_location = (end_row, end_col)
                    
                    # check if in that temporary position we are in check
                    in_check, pins, checks = self.check_for_pins_and_checks()
                    
                    # if we aren't in check then that is a valid space we can move to
                    if not in_check:
                        moves.append(GameState.rank_file(end_row, end_col))
                        piece_moved.append("K" if color else "k")
                        start_sq.append((r, c))
                        
                    # move king back to original position
                    if color:
                        self.white_king_location = (r, c)
                        self.board[king_start_row][king_start_col] = 'K'
                    else:
                        self.black_king_location = (r, c)
                        self.board[king_start_row][king_start_col] = 'k'
        
        # castling
        if color:
            if self.current_castle_rights.wks:
                if self.board[8][6] == "-" and self.board[8][7] == "-":
                    king_start_row = self.white_king_location[0]
                    king_start_col = self.white_king_location[1]
                    self.board[self.white_king_location[0]][self.white_king_location[1]] = '-'
                    self.white_king_location = (8, 6)
                    
                    in_check, pins, checks = self.check_for_pins_and_checks()
                    
                    if in_check:
                        self.current_castle_rights.wks = False
                    
                    self.board[self.white_king_location[0]][self.white_king_location[1]] = '-'
                    self.white_king_location = (8, 7)
                    
                    in_check, pins, checks = self.check_for_pins_and_checks()
                    
                    if in_check:
                        self.current_castle_rights.wks = False
                        
                    self.white_king_location = (r, c)
                    self.board[king_start_row][king_start_col] = 'K'
            
            if self.current_castle_rights.wqs:
                if self.board[8][4] == "-" and self.board[8][3] == "-" and self.board[8][2] == "-":
                    king_start_row = self.white_king_location[0]
                    king_start_col = self.white_king_location[1]
                    self.board[self.white_king_location[0]][self.white_king_location[1]] = '-'
                    self.white_king_location = (8, 4)
                    
                    in_check, pins, checks = self.check_for_pins_and_checks()
                    
                    if in_check:
                        self.current_castle_rights.wqs = False
                    
                    self.board[self.white_king_location[0]][self.white_king_location[1]] = '-'
                    self.white_king_location = (8, 3)
                    
                    in_check, pins, checks = self.check_for_pins_and_checks()
                    
                    if in_check:
                        self.current_castle_rights.wqs = False
                        
                    self.white_king_location = (r, c)
                    self.board[king_start_row][king_start_col] = 'K'
                   
        else:
            if self.current_castle_rights.bks:
                if self.board[1][6] == "-" and self.board[1][7] == "-":
                    king_start_row = self.black_king_location[0]
                    king_start_col = self.black_king_location[1]
                    self.board[self.black_king_location[0]][self.black_king_location[1]] = '-'
                    self.black_king_location = (1, 6)
                    
                    in_check, pins, checks = self.check_for_pins_and_checks()
                    
                    if in_check:
                        self.current_castle_rights.bks = False
                    
                    self.board[self.black_king_location[0]][self.black_king_location[1]] = '-'
                    self.black_king_location = (1, 7)
                    
                    in_check, pins, checks = self.check_for_pins_and_checks()
                    
                    if in_check:
                        self.current_castle_rights.bks = False
                        
                    self.black_king_location = (r, c)
                    self.board[king_start_row][king_start_col] = 'K'
            
            if self.current_castle_rights.bqs:
                if self.board[1][4] == "-" and self.board[1][3] == "-" and self.board[1][2] == "-":
                    king_start_row = self.black_king_location[0]
                    king_start_col = self.black_king_location[1]
                    self.board[self.black_king_location[0]][self.black_king_location[1]] = '-'
                    self.black_king_location = (1, 4)
                    
                    in_check, pins, checks = self.check_for_pins_and_checks()
                    
                    if in_check:
                        self.current_castle_rights.bqs = False
                    
                    self.board[self.black_king_location[0]][self.black_king_location[1]] = '-'
                    self.black_king_location = (1, 3)
                    
                    in_check, pins, checks = self.check_for_pins_and_checks()
                    
                    if in_check:
                        self.current_castle_rights.bqs = False
                        
                    self.black_king_location = (r, c)
                    self.board[king_start_row][king_start_col] = 'k'
        
        # add the castling moves
        if color:
            if self.current_castle_rights.wks:
                if self.board[8][6] == "-" and self.board[8][7] == "-":
                    moves.append(GameState.rank_file(8, 7))
                    piece_moved.append("O-O")
                    start_sq.append((r, c))
            if self.current_castle_rights.wqs:
                if self.board[8][4] == "-" and self.board[8][3] == "-" and self.board[8][2] == "-":
                    moves.append(GameState.rank_file(8, 3))
                    piece_moved.append("O-O-O")
                    start_sq.append((r, c))
        else:
            if self.current_castle_rights.bks:
                if self.board[1][6] == "-" and self.board[1][7] == "-":
                    moves.append(GameState.rank_file(1, 7))
                    piece_moved.append("O-O")
                    start_sq.append((r, c))
            if self.current_castle_rights.bqs:
                if self.board[1][4] == "-" and self.board[1][3] == "-" and self.board[1][2] == "-":
                    moves.append(GameState.rank_file(1, 3))
                    piece_moved.append("O-O-O")
                    start_sq.append((r, c))
                        





    # rank file
    def rank_file(r, c):
        # maps keys to values
        # key : value
        ranks_to_rows = {"1": 8, "2": 7, "3": 6, "4" : 5,
                         "5": 4, "6": 3, "7": 2, "8" : 1}
        rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}

        files_to_cols = {"a": 1, "b": 2, "c": 3, "d" : 4,
                         "e": 5, "f": 6, "g": 7, "h" : 8}
        cols_to_files = {v: k for k, v in files_to_cols.items()}
        return cols_to_files[c] + rows_to_ranks[r]

    # rank file
    def row_col(r, c):
        # maps keys to values
        # key : value
        ranks_to_rows = {"1": 8, "2": 7, "3": 6, "4" : 5,
                         "5": 4, "6": 3, "7": 2, "8" : 1}
        rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}

        files_to_cols = {"a": 1, "b": 2, "c": 3, "d" : 4,
                         "e": 5, "f": 6, "g": 7, "h" : 8}
        cols_to_files = {v: k for k, v in files_to_cols.items()}
        return ranks_to_rows[r], files_to_cols[c] 


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
        for i in range(0, len(moves)):
            if piece_moved[i] == "O-O" or piece_moved[i] == "O-O-O":
                pgn.append(piece_moved[i])
            else:
                flag = False
                
                end_sq_val = True if self.board[board_sq[i][0]][board_sq[i][1]] != "-" else False
                pawn_moved = True if self.board[start_sq[i][0]][start_sq[i][1]] == "P" or self.board[start_sq[i][0]][start_sq[i][1]] == "p" else False
                is_promotion = True if pawn_moved and (piece_moved[i] != "P" or piece_moved[i] != "p") else False
                promotion = "=" + str(piece_moved[i].upper()) if is_promotion else ""
                take = "x" if end_sq_val else ""
                piece = "" if pawn_moved else piece_moved[i].upper()
                isenpassant = True if self.enpassant_possible != () else False
                for j in range(0, len(moves)):
                    # check if indexes are the same
                    # are the moves to the same square?
                    # the two pieces that are moving there the same?
                    if i != j and moves[i] == moves[j] and piece_moved[i] == piece_moved[j]:
                        flag = True
                        # the two pieces that are moved on the same file?
                        ifile = GameState.rank_file(start_sq[i][0], start_sq[i][1])[0]
                        jfile = GameState.rank_file(start_sq[j][0], start_sq[j][1])[0]
                        file_or_row = 1 if ifile == jfile else 0
                        check = False
                        for k in range(0, len(moves)):
                            if i != k and j != k and moves[i] == moves[k] and piece_moved[i] == piece_moved[k]:
                                pgn.append(piece + rank_file[i] + take + moves[i])
                                check=True
                                break
                        # check if you broke the for loop
                        if check:
                            break
                        
                        
                        # check if pawn and en passant
                        if pawn_moved:
                            # check if a piece was captured
                            # check if en passant
                            if board_sq[i] == self.enpassant_possible: 
                                pgn.append(rank_file[i][0] + "x" + moves[i])
                            else:
                                # append pgn
                                pgn.append(piece + rank_file[i][file_or_row] + take + moves[i] + promotion)
                                break
    
    
                if not flag:
                    # check if pawn was moved
                    if pawn_moved:
                        # check if a piece was captured
                        if end_sq_val:
                            pgn.append(rank_file[i][0] + take + moves[i] + promotion)
                        else:
                            # check if en passant
                            if board_sq[i] == self.enpassant_possible: 
                                pgn.append(rank_file[i][0] + "x" + moves[i])
                            else:
                                pgn.append(moves[i])
    
                    else:
                        pgn.append(piece + take + moves[i])
    
    
                # added in if statement to check for check and checkmate
        return pgn
    
class CastleRights():
    def __init__(self, white_king_side, white_queen_side, black_king_side, black_queen_side):
        self.wks = white_king_side
        self.wqs = white_queen_side
        self.bks = black_king_side
        self.bqs = black_queen_side
        
        
    
    
    
    
    
    
    
    
    
    
