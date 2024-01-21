import sys
import chess
import random
from definitions import INFINITE, MAX_PLY
from evaluation.mixins import PieceEvaluate
from search.alphabeta import AlphaBetaMixin
from search.alphabeta import antichess_legal_moves
from controller.time_controller import TimeController

class Engine(AlphaBetaMixin, PieceEvaluate, TimeController):
    pass

def main():

    if len(sys.argv) != 2:
        print("Incorrect number of arguments!")
        quit()

    if sys.argv[1].lower() == 'white':
        side = True
    elif sys.argv[1].lower() == 'black':
        side = False
    else:
        print("Invalid argument entered!")
        quit()

    board = chess.Board()

    # assuming all losses, draws, and invalid moves are handled by oversight program
    while True:

        if board.turn == side:
            antichess_moves = list(antichess_legal_moves(board, board.legal_moves))
            if len(antichess_moves) == 1:
                board.push(antichess_moves[0]) #since this is the only capture move, we have to take it
            else:
                engine=Engine(board)
                engine.start_signal(2000)
                best_score=-INFINITE
                best_pv=[]
                for depth in range(1, MAX_PLY):
                    score, pv = engine.search(-INFINITE, +INFINITE, depth, square=False)
                    if engine.stop_signal():
                        break
                    if score > best_score:
                        best_pv=pv
                        best_score=score
                if pv == []:
                    move=random.choice(antichess_moves)
                    print(move)
                    board.push(move)
                else:
                    move=best_pv[0]
                    print(move)
                    board.push(move)
        else:
            board.push(chess.Move.from_uci(input()))

main()