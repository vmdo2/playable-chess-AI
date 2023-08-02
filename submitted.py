import math
import mychess.lib
from mychess.lib.utils import encode, decode
from mychess.lib.heuristics import evaluate
from mychess.lib.core import makeMove

###########################################################################################
# Utility function: Determine all the legal moves available for the side.
# This is modified from chess.lib.core.legalMoves:
#  each move has a third element specifying whether the move ends in pawn promotion
def generateMoves(side, board, flags):
    for piece in board[side]:
        fro = piece[:2]
        for to in mychess.lib.availableMoves(side, board, piece, flags):
            promote = mychess.lib.getPromote(None, side, board, fro, to, single=True)
            yield [fro, to, promote]
            
###########################################################################################
# Example of a move-generating function:
# Randomly choose a move.
def random(side, board, flags, chooser):
    '''
    Return a random move, resulting board, and value of the resulting board.
    Return: (value, moveList, boardList)
      value (int or float): value of the board after making the chosen move
      moveList (list): list with one element, the chosen move
      moveTree (dict: encode(*move)->dict): a tree of moves that were evaluated in the search process
    Input:
      side (boolean): True if player1 (Min) plays next, otherwise False
      board (2-tuple of lists): current board layout, used by generateMoves and makeMove
      flags (list of flags): list of flags, used by generateMoves and makeMove
      chooser: a function similar to random.choice, but during autograding, might not be random.
    '''
    moves = [ move for move in generateMoves(side, board, flags) ]
    if len(moves) > 0:
        move = chooser(moves)
        newside, newboard, newflags = makeMove(side, board, move[0], move[1], flags, move[2])
        value = evaluate(newboard)
        return (value, [ move ], { encode(*move): {} })
    else:
        return (evaluate(board), [], {})

###########################################################################################
def minimaxHelper(value, currentMoveList, addTree, side, board, flags, depth):
    if depth == 0:
      return evaluate(board), currentMoveList, addTree
    if (not side):
      value = -10000
      for move in generateMoves(side, board, flags):
        addTree[encode(*move)] = {}
        newside, newboard, newflags = makeMove(side, board, move[0], move[1], flags, move[2])
        v, m, t = minimaxHelper(value, currentMoveList + [move], addTree[encode(*move)], newside, newboard, newflags, depth - 1)
        old = value
        value = max(value, v)
        if value != old: moves = m 
      return value, moves, addTree
    else:
      value = 10000
      for move in generateMoves(side, board, flags):
        addTree[encode(*move)] = {}
        newside, newboard, newflags = makeMove(side, board, move[0], move[1], flags, move[2])
        v, m, t = minimaxHelper(value, currentMoveList + [move], addTree[encode(*move)], newside, newboard, newflags, depth - 1)
        old = value
        value = min(value, v)
        if value != old: moves = m 
      return value, moves, addTree
# Move-generating functions using minimax, alphabeta, and stochastic search.
def minimax(side, board, flags, depth):
    '''
    Return a minimax-optimal move sequence, tree of all boards evaluated, and value of best path.
    Return: (value, moveList, moveTree)
      value (float): value of the final board in the minimax-optimal move sequence
      moveList (list): the minimax-optimal move sequence, as a list of moves
      moveTree (dict: encode(*move)->dict): a tree of moves that were evaluated in the search process
    Input:
      side (boolean): True if player1 (Min) plays next, otherwise False
      board (2-tuple of lists): current board layout, used by generateMoves and makeMove
      flags (list of flags): list of flags, used by generateMoves and makeMove
      depth (int >=0): depth of the search (number of moves)
    '''
    if depth == 0:
      return evaluate(board), [], {}
    tree = {}
    moves = []
    if (not side):
      value = -10000
      for move in generateMoves(side, board, flags):
        newside, newboard, newflags = makeMove(side, board, move[0], move[1], flags, move[2])
        tree[encode(*move)] = {}
        v, m, t = minimaxHelper(value, [move], tree[encode(*move)], newside, newboard, newflags, depth - 1)
        old = value
        value = max(value, v)
        if value != old: moves = m 
      return value, moves, tree
    else:
      value = 10000
      for move in generateMoves(side, board, flags):
        newside, newboard, newflags = makeMove(side, board, move[0], move[1], flags, move[2])
        tree[encode(*move)] = {}
        v, m, t = minimaxHelper(value, [move], tree[encode(*move)], newside, newboard, newflags, depth - 1)
        old = value
        value = min(value, v)
        if value != old: moves = m 
      return value, moves, tree

def alphabetaHelper(value, currentMoveList, addTree, side, board, flags, depth, alpha, beta):
    if depth == 0:
      return evaluate(board), currentMoveList, addTree
    if (not side):
      value = -10000
      moves = currentMoveList
      for move in generateMoves(side, board, flags):
        addTree[encode(*move)] = {}
        newside, newboard, newflags = makeMove(side, board, move[0], move[1], flags, move[2])
        v, m, t = alphabetaHelper(value, currentMoveList + [move], addTree[encode(*move)], newside, newboard, newflags, depth - 1, alpha, beta)
        old = value
        value = max(value, v)
        if value != old: moves = m 
        if (value >= beta):
          break
        alpha = max(alpha, value)
      return value, moves, addTree
    else:
      value = 10000
      for move in generateMoves(side, board, flags):
        addTree[encode(*move)] = {}
        newside, newboard, newflags = makeMove(side, board, move[0], move[1], flags, move[2])
        v, m, t = alphabetaHelper(value, currentMoveList + [move], addTree[encode(*move)], newside, newboard, newflags, depth - 1, alpha, beta)
        old = value
        value = min(value, v)
        if value != old: moves = m 
        if (value <= alpha):
          break
        beta = min(beta, value)
      return value, moves, addTree

def alphabeta(side, board, flags, depth, alpha=-math.inf, beta=math.inf):
    '''
    Return minimax-optimal move sequence, and a tree that exhibits alphabeta pruning.
    Return: (value, moveList, moveTree)
      value (float): value of the final board in the minimax-optimal move sequence
      moveList (list): the minimax-optimal move sequence, as a list of moves
      moveTree (dict: encode(*move)->dict): a tree of moves that were evaluated in the search process
    Input:
      side (boolean): True if player1 (Min) plays next, otherwise False
      board (2-tuple of lists): current board layout, used by generateMoves and makeMove
      flags (list of flags): list of flags, used by generateMoves and makeMove
      depth (int >=0): depth of the search (number of moves)
    '''
    if depth == 0:
      return evaluate(board), [], {}
    tree = {}
    moves = []
    if (not side):
      value = -10000
      for move in generateMoves(side, board, flags):
        newside, newboard, newflags = makeMove(side, board, move[0], move[1], flags, move[2])
        tree[encode(*move)] = {}
        v, m, t = alphabetaHelper(value, [move], tree[encode(*move)], newside, newboard, newflags, depth - 1, alpha, beta)
        old = value
        value = max(value, v)
        if value != old: moves = m 
        if (value >= beta):
          break
        alpha = max(alpha, value)
      return value, moves, tree
    else:
      value = 10000
      for move in generateMoves(side, board, flags):
        newside, newboard, newflags = makeMove(side, board, move[0], move[1], flags, move[2])
        tree[encode(*move)] = {}
        v, m, t = alphabetaHelper(value, [move], tree[encode(*move)], newside, newboard, newflags, depth - 1, alpha, beta)
        old = value
        value = min(value, v)
        if value != old: moves = m 
        if (value <= alpha):
          break
        beta = min(beta, value)
      return value, moves, tree
