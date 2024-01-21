"""
Used/Modified code from:
Chan Mk, python-chess-engine-extension, (2019), GitHub repository
https://github.com/Mk-Chan/python-chess-engine-extensions
"""

import chess

class BaseSearch(object):
    def __init__(self, board: chess.Board):
        if board is None:
            raise ValueError('board must be defined')
        self.board = board
