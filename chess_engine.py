"""
Building a Chess Engine (chess_engine)

Created on Wed Aug  3 22:11:00 2022

@author: ryantvackner
"""

# initalize the board
init_board = [
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
white_to_move = True

# move log in PGN
move_log = []

# print the inital board
for r in init_board:
   for c in r:
      print(c,end = " ")
   print()