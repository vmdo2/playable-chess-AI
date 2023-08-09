import chess
import chess.pgn
import sys
import chess.engine

def stockfish_evaluation(board, engine, time_limit = 0.0001):
    result = engine.analyse(board, chess.engine.Limit(time=time_limit))
    return result['score'].white(), result['pv'][0]
    
def pgn_parse():
    pgn = open("c:/Users/vince/Downloads/magnus.pgn")
    mygame=chess.pgn.read_game(pgn)
    num = 1
    engine = chess.engine.SimpleEngine.popen_uci("C:/Users/vince/Downloads/scid_windows_5.0.2/scid_windows_x64/engines/stockfish.exe")
    f = open("c:/Users/vince/Downloads/magnus_evalv2.pgn", "w")
    while True:  
        while mygame.next():
            fen = mygame.board().fen()
            board = chess.Board(fen)
            result = stockfish_evaluation(board, engine)
            node = mygame.variations[0]
            mygame=mygame.next()
            prev = board
            board.push(result[1])
            best_move_played = board == chess.Board(mygame.board().fen())
            board.pop()
            node.comment = "[%" + "eval: " + str(result[0]) + "] [" + "%" + "best_move: " + str(result[1]) + "] [" + "%" + "played_best_move: " + str(best_move_played) + "]" 
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
if __name__ == '__main__':
    pgn_parse()