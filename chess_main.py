"""
Building a Chess Engine (chess_main)

Created on Wed Aug  3 22:49:14 2022

@author: ryantvackner
"""
  
import chess_engine


def main():
    # create the board/gamestate
    gs = chess_engine.GameState()
    
    # print the board
    draw_board(gs.board)
    
    # game is running
    running = True
    
    # first move
    if running:
        m1 = input("1. ")
        print(m1)
        move = chess_engine.Move(m1, gs.board)
        gs.make_move(move)
        draw_board(gs.board)
        

def draw_board(board):
    # print the board
    for r in board:
       for c in r:
          print(c,end = " ")
       print()


if __name__ == "__main__":
    main()
