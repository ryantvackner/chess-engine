"""
Building a Chess Engine (chess_main)

Created on Wed Aug  3 22:49:14 2022

@author: ryantvackner
"""

# import chess_engine
import chess_engine

def main():
    # create the board/gamestate
    gs = chess_engine.GameState()
    
    # game is running
    running = True
    
    # move number
    move_number = 1
    
    # first move
    while running:
        # print the board
        draw_board(gs.board)
        
        # white to move
        while gs.white_to_move:
            # create the valid moves
            valid_moves = gs.get_valid_moves()
        
            # print valid moves
            print(valid_moves)
        
            # get move 1 input
            move = input(format(move_number) + ". ")
        
            # resign the game 
            if move == "qq":
                running = False
                break
        
            # check if the move is valid
            if move in valid_moves[0]:
                # find the move id and find out what piece made the move
                move_id = valid_moves[0].index(move)
                piece = valid_moves[1][move_id]
                start_sq = valid_moves[2][move_id]
                rank_file_move = valid_moves[3][move_id]
                
                # make the move
                gs.make_move(rank_file_move, piece, start_sq)
                
                # blacks turn now
                gs.white_to_move = False
            
        
        # redraw the board for black
        draw_board(gs.board)
        
        print(gs.enpassant_possible)
        
        # black to move
        while not gs.white_to_move:
            # create the valid moves
            valid_moves = gs.get_valid_moves()
        
            # print valid moves
            print(valid_moves[0])
        
            # get move 1 input
            move = input(format(move_number) + ". ")
        
            # resign the game 
            if move == "qq":
                running = False
                break
        
            # check if the move is valid
            if move in valid_moves[0]:
                # find the move id and find out what piece made the move
                move_id = valid_moves[0].index(move)
                piece = valid_moves[1][move_id]
                start_sq = valid_moves[2][move_id]
                rank_file_move = valid_moves[3][move_id]
                
                # make the move
                gs.make_move(rank_file_move, piece, start_sq)
                
                # blacks turn now
                gs.white_to_move = True
                
        
        # increase the move number
        move_number += 1
        

def draw_board(board):
    # print the board
    for r in board:
       for c in r:
          print(c,end = " ")
       print()


if __name__ == "__main__":
    main()
