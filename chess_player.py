import math
import os,sys,argparse
import random
import pygame
import mychess.lib
import pgn_parser
import submitted
import chess
import chess.pgn
import chess.svg

def random_move_player(board):
    legal_moves = list(board.legal_moves)
    if len(legal_moves) == 0:
        return None  # If no legal moves available, return None or any other indication of inability to move

    random_move = random.choice(legal_moves)
    return random_move
    
def get_best_move(board):
    with chess.engine.SimpleEngine.popen_uci("C:/Users/vince/Downloads/scid_windows_5.0.2/scid_windows_x64/engines/stockfish.exe") as engine:
        result = engine.play(board, chess.engine.Limit(time=2))
        return result.move

def minimax(side, board, depth, alpha, beta):
    if depth == 0:
        #print(int(pgn_parser.stockfish_evaluation(board)[0]))
        return int(pgn_parser.stockfish_evaluation(board)[0].score())
    tree = {}
    moves = list(board.legal_moves)
    if (not side):
      max_eval = float('-inf')
      for move in moves:
        board.push(move)
        evaluation = minimax(False, board, depth - 1, alpha, beta)
        board.pop()
        max_eval = max(max_eval, evaluation)
        alpha = max(alpha, evaluation)
        if beta <= alpha:
            break
        return max_eval
    else:
      min_eval = float('inf')
      for move in moves:
        board.push(move)
        evaluation = minimax(True, board, depth - 1, alpha, beta)
        board.pop()
        min_eval = min(max_eval, evaluation)
        alpha = min(alpha, evaluation)
        if beta <= alpha:
            break
        return min_eval

def alpha_beta_pruned_move(board, depth):
    legal_moves = list(board.legal_moves)
    best_move = None
    best_eval = float('-inf')

    for move in legal_moves:
        board.push(move)
        evaluation = minimax(False, board, depth - 1, float('-inf'), float('inf'))
        board.pop()

        if evaluation > best_eval:
            best_eval = evaluation
            best_move = move

    return best_move