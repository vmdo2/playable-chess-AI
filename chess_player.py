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
import chess.engine

def get_best_move(board, time_limit=2):
    with chess.engine.SimpleEngine.popen_uci("C:/Users/vince/Downloads/scid_windows_5.0.2/scid_windows_x64/engines/stockfish.exe") as engine:
        result = engine.play(board, chess.engine.Limit(time=time_limit))
        engine.close()
        return result.move

def evaluate_board(board):
    with chess.engine.SimpleEngine.popen_uci("C:/Users/vince/Downloads/scid_windows_5.0.2/scid_windows_x64/engines/stockfish.exe") as engine:
        info = engine.analyse(board, chess.engine.Limit(time=0.1))
        score = info["score"].white().score(mate_score=10000)  # Convert the score to centipawns
        engine.close()
        return score

def evaluate_board_simple(board):
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 100  # Just an arbitrary high value for simplicity
    }

    score = 0

    # Check for checkmate and return a very high value if it's a checkmate
    if board.is_checkmate():
        return 10000 if board.turn == chess.WHITE else -10000

    for square in chess.SQUARES:
        piece = board.piece_at(square)

        if piece is None:
            continue

        piece_value = piece_values[piece.piece_type]
        if piece.color == chess.WHITE:
            score += piece_value
        else:
            score -= piece_value
    
    # Bonus for giving check or checkmate
    if board.is_check():
        score += 50

    return score

def random_move_player(board):
    legal_moves = list(board.legal_moves)
    if len(legal_moves) == 0:
        return None  # If no legal moves available, return None or any other indication of inability to move

    random_move = random.choice(legal_moves)
    return random_move
    
def alphabeta(side, board, depth, alpha=-math.inf, beta=math.inf):
    best_move = None
    max_eval = float("-inf") if side else float("inf")
    alpha = float("-inf")
    beta = float("inf")

    for move in board.legal_moves:
        board.push(move)
        evaluation = alphabetahelper(board.turn, board, depth - 1, alpha, beta)
        board.pop()
        if side and evaluation > max_eval:
            max_eval = evaluation
            best_move = move
        elif not side and evaluation < max_eval:
            max_eval = evaluation
            best_move = move

    return best_move

def alphabetahelper(side, board, depth, alpha=-math.inf, beta=math.inf):
    if depth == 0 or board.is_game_over() or board.is_checkmate():
      return evaluate_board_simple(board)
    if (side):
      value = -10000
      for move in board.legal_moves:
        board.push(move)
        v = alphabetahelper(board.turn, board, depth - 1, alpha, beta)
        board.pop()
        value = max(value, v)
        if (value >= beta):
          break
        alpha = max(alpha, value)
      return value
    else:
      value = 10000
      for move in board.legal_moves:
        board.push(move)
        v = alphabetahelper(board.turn, board, depth - 1, alpha, beta)
        board.pop()
        value = min(value, v)
        if (value <= alpha):
          break
        beta = min(beta, value)
      return value