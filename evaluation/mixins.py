"""
Used/Modified code from:
Chan Mk, python-chess-engine-extension, (2019), GitHub repository
https://github.com/Mk-Chan/python-chess-engine-extensions
"""

import chess
from evaluation.piece_values import PIECE_VALUES
from evaluation.piece_square_tables import PIECE_SQUARE_TABLES

class BaseEvaluation(object):
    def __init__(self, board: chess.Board):
        if board is None:
            raise ValueError('board must be defined')
        self.board = board

    def evaluate(self):
        return 0

class PieceEvaluate(BaseEvaluation):
    def evaluate(self, square: bool):
        parent_score = super(PieceEvaluate, self).evaluate()
        score = 0
        for piece_type in chess.PIECE_TYPES:
            if not square:
                pieces_mask = self.board.pieces_mask(piece_type, chess.WHITE) # white
                score += chess.popcount(pieces_mask) * PIECE_VALUES[piece_type]
                pieces_mask = self.board.pieces_mask(piece_type, chess.BLACK) # black
                score -= chess.popcount(pieces_mask) * PIECE_VALUES[piece_type]
            else:
                for s in self.board.pieces(piece_type, chess.WHITE):  # white
                    score += PIECE_SQUARE_TABLES[piece_type][s]
                for s in self.board.pieces(piece_type, chess.BLACK):  # black
                    score -= PIECE_SQUARE_TABLES[piece_type][s ^ 56] 
        if self.board.turn == chess.BLACK:
            score = -score
        return score + parent_score
