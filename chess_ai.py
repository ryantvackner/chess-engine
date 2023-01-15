# -*- coding: utf-8 -*-
"""
Building a Chess Engine (chess_ai)

Created on Sat Jan 14 19:11:20 2023

@author: ryanv
"""

import random

def get_random_move(get_valid_moves):
    return get_valid_moves[random.randint(0, len(get_valid_moves)-1)]
