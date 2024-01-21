import sys
import chess
import random
import datetime as dt 
from alphabeta_v1 import AlphaBetaMixin_v1
from search.alphabeta import AlphaBetaMixin
from evaluation.mixins import PieceEvaluate
from definitions import INFINITE, MAX_PLY
from search.alphabeta import antichess_legal_moves
from controller.time_controller import TimeController
        
class Engine(AlphaBetaMixin, PieceEvaluate, TimeController): #Final version of our algorithm
    pass

class v1Engine(AlphaBetaMixin_v1, PieceEvaluate, TimeController): #An older version of our algorithm
    pass

def test():
    
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
    while not board.is_game_over():

        print(board)
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
                    score, pv = engine.search(-INFINITE, +INFINITE, depth, square=True)
                    print(depth, score, pv)
                    if engine.stop_signal():
                        break
                    if score > best_score:
                        best_pv=pv
                        best_score = score
                if pv == []:
                    board.push(random.choice(antichess_moves))
                else:
                    board.push(best_pv[0])
        else:
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
                    print(depth, score, pv)
                    if engine.stop_signal():
                        break
                    if score > best_score:
                        best_pv=pv
                        best_score = score
                if pv == []:
                    board.push(random.choice(antichess_moves))
                else:
                    board.push(best_pv[0])

    print(board)
    if board.is_checkmate():
        print('Checkmate!')
        print(board.outcome())
    elif board.is_insufficient_material():
        print('Draw by insufficient material!')
    elif board.is_stalemate():
        print('Draw by stalemate!')
    elif board.is_fifty_moves():
        print('Draw by 50-move rule!')
    elif board.is_repetition(count=3):
        print('Draw by 3-fold repetition!')
    else:
        print('Unexpected game over!?')

    return 

test()
