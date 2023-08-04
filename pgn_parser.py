import chess
import chess.pgn
import sys
import chess.engine

def stockfish_evaluation(board, time_limit = 0.0001):
    #print(board)
    engine = chess.engine.SimpleEngine.popen_uci("C:/Users/vince/Downloads/scid_windows_5.0.2/scid_windows_x64/engines/stockfish.exe")
    result = engine.analyse(board, chess.engine.Limit(time=time_limit))
    engine.close()
    return result['score'].white(), result['pv'][0]
    
def pgn_parse():
    pgn = open("c:/Users/vince/Downloads/magnus.pgn")
    mygame=chess.pgn.read_game(pgn)
    num = 1
    engine = chess.engine.SimpleEngine.popen_uci("C:/Users/vince/Downloads/scid_windows_5.0.2/scid_windows_x64/engines/stockfish.exe")
    f = open("c:/Users/vince/Downloads/magnus_eval.pgn", "a")
    while True:  
        while mygame.next():
            fen = mygame.board().fen()
            board = chess.Board(fen)
            print(board)
            result = stockfish_evaluation(board)
            node = mygame.variations[0]
            node.comment = "[%" + "eval: " + str(stockfish_evaluation(board)[0]) + "] [" + "%" + "best_move: " + str(stockfish_evaluation(board)[1]) + "]"
            mygame=mygame.next()
        print("Printing game " + str(num) + " with evaluation")
        print(mygame.game(), file=f, end="\n\n")
        num += 1
        mygame=chess.pgn.read_game(pgn)
        if mygame is None:
            break
    f.close()
    engine.close()
    pgn.close()
    print("COMPLETE")
    return