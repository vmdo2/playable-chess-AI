import chess
import chess.pgn
import sys
import chess.engine

def stockfish_evaluation(board, time_limit = 0.01):
    engine = chess.engine.SimpleEngine.popen_uci("C:/Users/vince/Downloads/scid_windows_5.0.2/scid_windows_x64/engines/stockfish.exe")
    result = engine.analyse(board, chess.engine.Limit(time=time_limit))
    return result['score'], result['pv'][0]

pgn = open("c:/Users/vince/Downloads/magnus.pgn")
mygame=chess.pgn.read_game(pgn)
print(mygame)
while True:  
    while mygame.next():
        fen = mygame.board().fen()
        board = chess.Board(fen)
        result = stockfish_evaluation(board)
        node = mygame.variations[0]
        node.comment = "[%" + "eval: " + str(stockfish_evaluation(board)[0]) + "] [" + "%" + "best_move: " + str(stockfish_evaluation(board)[1]) + "]"
        mygame=mygame.next()
    print("Printing game with evaluation")
    print(mygame.game())
    break
    mygame=chess.pgn.read_game(pgn)
    if mygame is None:
        break
pgn.close()
exit()