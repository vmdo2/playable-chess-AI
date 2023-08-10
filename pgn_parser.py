import chess
import chess.pgn
import sys
import chess.engine

def stockfish_evaluation(board, engine, time_limit = 0.0001):
    result = engine.analyse(board, chess.engine.Limit(time=time_limit))
    return result['score'].white(), result['pv'][0]
    
def pgn_parse(path_open, path_save):
    pgn = open(path_open)
    mygame=chess.pgn.read_game(pgn)
    num = 1
    engine = chess.engine.SimpleEngine.popen_uci("C:/Users/vince/Downloads/scid_windows_5.0.2/scid_windows_x64/engines/stockfish.exe")
    f = open(path_save, "w")
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
def read_pgn():
    pgn = open("c:/Users/vince/Downloads/magnus_evalv2.pgn", "r")
    mygame=chess.pgn.read_game(pgn)
    false = 0
    true = 0
    num = 0
    while True:  
        while mygame.next():
            fen = mygame.board().fen()
            board = chess.Board(fen)
            node = mygame.variations[0]
            if (board.turn and mygame.game().headers["White"] == "Carlsen, Magnus" or not board.turn and mygame.game().headers["Black"] == "Carlsen, Magnus"):
                true += node.comment.count("True")
                false += node.comment.count("False")
            mygame=mygame.next()
        mygame=chess.pgn.read_game(pgn)
        print("Finishing game " + str(num))
        num += 1
        if mygame is None:
            break
    print("False: " + str(false))
    print("True: " + str(true))
    pgn.close()
if __name__ == '__main__':
    pgn_parse("c:/Users/vince/Downloads/GM_games_2600_pt2.pgn", "c:/Users/vince/Downloads/GM_games_eval.pgn")