"""
Building a Chess Engine (chess_main)

Created on Wed Aug  3 22:49:14 2022

@author: ryantvackner
"""
  
import chess_engine

def main():
    # create the board/gamestate
    gs = chess_engine.GameState()
    
    # create the valid moves
    valid_moves = gs.get_valid_moves()
    print(valid_moves)
    
    # flag var to indicate a move has been made
    move_made = False
    
    # print the board
    draw_board(gs.board)
    
    # game is running
    running = True
    
    # first move
    if running:
        # get move 1 input
        move = input("1. ")
        
        # check if the move is valid
        if move in valid_moves[0]:
            # find the move id and find out what piece made the move
            move_id = valid_moves[0].index(move)
            piece = valid_moves[1][move_id]
            start_sq = valid_moves[2][move_id]
            rank_file_move = valid_moves[3][move_id]
            
            # make the move
            gs.make_move(rank_file_move, piece, start_sq)
            
            # flag that the move has been made
            move_made = True
    
        
        draw_board(gs.board)
        
    if move_made:
        valid_moves = gs.get_valid_moves()
        move_made = False
        

def draw_board(board):
    # print the board
    for r in board:
       for c in r:
          print(c,end = " ")
       print()


if __name__ == "__main__":
    main()
