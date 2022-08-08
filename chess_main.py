"""
Building a Chess Engine (chess_main)

Created on Wed Aug  3 22:49:14 2022

@author: ryantvackner
"""
  
#import pygame as p
import chess_engine


def main():
    # create the board/gamestate
    gs = chess_engine.GameState()
    
    # print the board
    draw_board(gs.board)


def draw_board(board):
    # print the board
    for r in board:
       for c in r:
          print(c,end = " ")
       print()


if __name__ == "__main__":
    main()