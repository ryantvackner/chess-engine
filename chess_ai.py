# -*- coding: utf-8 -*-
"""
Building a Chess Engine (chess_ai)

Created on Sat Jan 14 19:11:20 2023

@author: ryanv
"""

import random

piece_value = {"K": 100, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1, "k": -100, "q": -10, "r": -5, "b": -3, "n": -3, "p": -1,  
               "-": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2

def get_random_move(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves)-1)]


def get_best_move(gs, valid_moves, piece, start_sq, rank_file_move):
    # currently check white to move, if recursion do i have to switch to test white to move?
    turn_multiplier = 1 if gs.white_to_move else -1
    
    
    max_score = -CHECKMATE
    best_move = None
    for move in valid_moves:
        move_id = valid_moves.index(move)
        gs.copy_board(rank_file_move[move_id], piece[move_id], start_sq[move_id])
        if gs.test_checkmate:
            score = CHECKMATE
        elif gs.test_stalemate:
            score = STALEMATE
        else:
            score = turn_multiplier * get_material_value(gs.test_board)
        if score > max_score:
            max_score = score
            best_move = move

    
    
    return best_move


def get_best_min_max(gs, valid_moves, piece, start_sq, rank_file_move):
    global next_move
    next_move = None
    get_min_max(gs, valid_moves, DEPTH, gs.white_to_move)
    return next_move
    

def get_min_max(gs, valid_moves, depth, white_to_move):
    global next_move
    if depth == 0:
        return get_material_value(gs.test_board)
    
    if white_to_move:
        max_score = -CHECKMATE
        for move in valid_moves:
            gs.test_move()
            #next_moves = gs.get_valid_moves()
            # i need to get the next valid moves for the recursive algo
            # but get valid moves gets the valid moves for the actual
            # board in which no new moves were currently made 
            # i need to simply and make my code more generic 
            score = get_min_max(gs, valid_moves, depth, white_to_move)






def get_material_value(board):
    score = 0
    for row in board:
            for square in row:
                if square[0] == ' ':
                    break
                else:
                    score += piece_value[square]
                    
    return score


# 
def get_score_board(gs):
    if gs.test_checkmate:
        if gs.test_white_to_move:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.test_stalemate:
        return STALEMATE
            
    
    score = 0
    for row in gs.test_board:
            for square in row:
                if square[0] == ' ':
                    break
                else:
                    score += piece_value[square]
                    
    return score
    
    
    
    
    

