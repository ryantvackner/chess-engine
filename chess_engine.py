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
        self.board[move_sq[0]][move_sq[1]] = piece

        # add move to move log using proper chess notation
        self.move_log.append(move)

        # swap whos turn it is to move
        self.white_to_move = not self.white_to_move

        # update kings location
        if piece == "K":
            self.white_king_location = (move_sq[1], move_sq[0])
        elif piece == "k":
            self.black_king_location = (move_sq[1], move_sq[0])

    # get all valid moves, can't put yourself in check
    def get_valid_moves(self):
        pgn = []
        piece_moved = []
        start_sq = []
        rank_file_move = []
        moves = []
        self.in_check, self.pins, self.checks = self.check_for_pins_and_checks()
        if self.white_to_move:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]
        if self.in_check:
            moves = self.get_all_possible_moves()
            pgn = []
            piece_moved = []
            start_sq = []
            rank_file_move = []
            # only 1 check, block or move king
            print(self.checks)
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
                
                # get rid of moves that dont block check
                for i in range(len(moves[0]) - 1, -1, -1):
                    move_sq = GameState.row_col(moves[3][i][1], moves[3][i][0])
                    if self.white_to_move:
                        if moves[1][i] == "K":
                            valid_squares.append(GameState.row_col(moves[3][i][1], moves[3][i][0]))
                        if move_sq in valid_squares:
                            pgn.append(moves[0][i])
                            piece_moved.append(moves[1][i])
                            start_sq.append(moves[2][i])
                            rank_file_move.append(moves[3][i])
                    else:
                        if moves[1][i] == "k":
                            valid_squares.append(GameState.row_col(moves[3][i][1], moves[3][i][0]))
                        if move_sq in valid_squares:
                            pgn.append(moves[0][i])
                            piece_moved.append(moves[1][i])
                            start_sq.append(moves[2][i])
                            rank_file_move.append(moves[3][i])
            # double check
            else:
                print(moves)
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
                    self.move_functions[piece](
                        r, c, moves, piece_moved, start_sq)


        pgn = GameState.get_pgn(self, moves, piece_moved, start_sq)
        return pgn, piece_moved, start_sq, moves

    # returns if the player is in check, a list of pins, and list of checks
    def check_for_pins_and_checks(self):
        pins = []
        checks = []
        in_check = False
        color = True if self.white_to_move else False
        if self.white_to_move:
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possible_pin = ()
            for i in range(1, 8):
                end_row = start_row + d[0] * i
                end_col = start_col + d[1] * i
                if 1 <= end_row < 9 and 1 <= end_col < 9:
                    end_piece = self.board[end_row][end_col]
                    end_piece_color = self.board[end_row][end_col].isupper()
                    if end_piece_color == color and end_piece.upper() != "K":
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
                        moves.append(GameState.rank_file(r-1, c-1))
                        count += 1
            # white pawn capture right
            if c+1 <= 8:
                if self.board[r-1][c+1].islower():
                    if not piece_pinned or pin_direction == (-1, 1):
                        moves.append(GameState.rank_file(r-1, c+1))
                        count += 1
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
                        moves.append(GameState.rank_file(r+1, c-1))
                        count += 1
            # black pawn capture right
            if c+1 <= 8:
                if self.board[r+1][c+1].islower():
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
        pin_direction = ()
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
        direction=((-1, -1), (-1, 0), (-1, 1), (0, -1),
                   (0, 1), (1, -1), (1, 0), (1, 1))
        color=True if self.white_to_move else False
        for i in range(8):
            end_row = r + direction[i][0]
            end_col = c + direction[i][1]
            if 1 <= end_row < 9 and 1 <= end_col < 9:
                end_piece=self.board[end_row][end_col]
                end_piece_color=self.board[end_row][end_col].islower()
                if end_piece == "-" or end_piece_color == color:
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
                    in_check, pins, checks = self.check_for_pins_and_checks()
                    if not in_check:
                        moves.append(GameState.rank_file(end_row, end_col))
                        piece_moved.append("K" if color else "k")
                        start_sq.append((r, c))
                    if color:
                        self.white_king_location = (r, c)
                        self.board[king_start_row][king_start_col] = 'K'
                    else:
                        self.black_king_location = (r, c)
                        self.board[king_start_row][king_start_col] = 'k'
    

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
            flag = False
            end_sq_val = True if self.board[board_sq[i][0]][board_sq[i][1]] != "-" else False
            pawn_moved = True if piece_moved[i] == "P" or piece_moved[i] == "p" else False
            take = "x" if end_sq_val else ""
            piece = "" if pawn_moved else piece_moved[i].upper()
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
                    # append pgn
                    pgn.append(piece + rank_file[i][file_or_row] + take + moves[i])
                    break


            if not flag:
                # check if pawn was moved
                if pawn_moved:
                    # check if rank is 2
                    # promotion



                    # check if a piece was captured
                    if end_sq_val:
                        pgn.append(rank_file[i][0] + take + moves[i])
                    else:
                        pgn.append(moves[i])
                else:
                    pgn.append(piece + take + moves[i])


            # added in if statement to check for check and checkmate
        return pgn

