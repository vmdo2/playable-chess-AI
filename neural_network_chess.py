import chess
import chess.pgn
import sys
import chess.engine

def stockfish_evaluation(board, time_limit = 0.01):
    engine = chess.engine.SimpleEngine.popen_uci("C:/Users/vince/Downloads/scid_windows_5.0.2/scid_windows_x64/engines/stockfish.exe")
    result = engine.analyse(board, chess.engine.Limit(time=time_limit))
    return result['score']

pgn = open("c:/Users/vince/Downloads/magnus.pgn")
mygame=chess.pgn.read_game(pgn)
while mygame.next():
    mygame=mygame.next()
    print(mygame.board().fen())

# board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
# result = stockfish_evaluation(board)
# eval = set_eval()
pgn = close("Users/vince/Downloads/magnus.pgn")