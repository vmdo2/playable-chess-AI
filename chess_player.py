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
        return score

def evaluate_board_simple(board):
    material_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9
    }

    total_white_material = 0
    total_black_material = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            value = material_values.get(piece.piece_type, 0)
            if piece.color == chess.WHITE:
                total_white_material += value
            else:
                total_black_material += value

    return total_white_material - total_black_material

def random_move_player(board):
    legal_moves = list(board.legal_moves)
    if len(legal_moves) == 0:
        return None  # If no legal moves available, return None or any other indication of inability to move

    random_move = random.choice(legal_moves)
    return random_move
    
def alphabeta(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board_simple(board)

    if maximizing_player:
        value = float("-inf")
        for move in board.legal_moves:
            board.push(move)
            value = max(value, alphabeta(board, depth - 1, alpha, beta, False))
            board.pop()
            alpha = max(alpha, value)
            if value >= beta:
                break  # Beta cutoff
        return value
    else:
        value = float("inf")
        for move in board.legal_moves:
            board.push(move)
            value = min(value, alphabeta(board, depth - 1, alpha, beta, True))
            board.pop()
            beta = min(beta, value)
            if value <= alpha:
                break  # Alpha cutoff
        return value

def get_best_move_alphabeta(board, depth):
    best_move = None
    max_eval = float("inf") if not board.turn else float("-inf")
    alpha = float("-inf")
    beta = float("inf")
    for move in board.legal_moves:
        board.push(move)
        evaluate = alphabeta(board, depth - 1, alpha, beta, board.turn)
        board.pop()
        if evaluate > max_eval and board.turn:
            max_eval = evaluate
            best_move = move
        elif evaluate < max_eval and not board.turn:
            max_eval = evaluate
            best_move = move
        alpha = max(alpha, max_eval)
    return best_move