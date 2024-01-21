# -*- coding: utf-8 -*-
#
# This file is part of the python-chess-engine-extensions library.
# Copyright (C) 2019 Manik Charan <mkchan2951@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import chess

from search.base import BaseSearch
from definitions import INFINITE, MATE


def antichess_legal_moves(board: chess.Board, legal_moves):
    """Returns legal moves in antiches. (A legal move in antichess: If the player to move has a legal chess move which captures an opponent’s piece, then the
    player to move must make a legal chess move which captures an opponent’s piece.)

    Args:
      board: a chess board
      legal_moves: a dynamic list of legal moves in standard chess
    
    Returns:
      A list of the current position antichess legal moves.
    """
    moves = []
    for m in legal_moves:
        if board.piece_at(chess.parse_square(m.uci()[2:4])) is not None:
            moves.append(m)
    if not moves: #no capture moves, so try all legal moves
        return list(legal_moves)
    else:
        return moves


def is_drawn(board: chess.Board):
    """Determines if the current position is drawn

    Args:
      board: a chess board

    Returns:
      A boolean indicates whether the current position fullfills the drawing conditions
    """
    return board.is_repetition(count=3) \
            or board.is_stalemate() \
            or board.is_fifty_moves() \
            or board.is_insufficient_material()


class AlphaBetaMixin_v1(BaseSearch):
    def search(self, alpha, beta, depth, square, ply=0):
        """
        Search `self.board` with the `self.evaluate` using the
        Alpha-Beta Pruning algorithm.

        The implementation is in a Negamax arrangement.
        -> Here, we try to avoid repeating code for the min and max nodes by
           fixing a positive score for White and negative score for Black.
        -> Consider the root node as a max-node.
        -> When searching a min-node, we can simply maximize the negative score
           to achieve the same effect as minimizing the score.
        -> The score returned to the parent then needs to be negated to retrieve
           the actual value.
        -> Since we are maximizing the negative score of a child and negating the
           return value, our (alpha, beta) bounds become (-beta, -alpha) instead.

        * Note: Alpha-cutoffs become beta-cutoffs since we have normalized all
                nodes to max-nodes.

        :param alpha: Lower limit of the score.
        :param beta: Upper limit of the score.
        :param depth: Remaining depth to search.
        :param ply: Depth of the current node.
                    Default: 0 - for the root node.

        :return: (score, pv).
        """

        if depth <= 0:
            # This is a leaf node. So use plain evaluation or quiescence search.
            score = self.evaluate(square)
            if abs(score) == INFINITE:
                return 0, []
            return self.evaluate(square), []

        if self.board.is_checkmate():
            # Board is in checkmate, return a distance from mate score.
            return -MATE + ply, []

        if is_drawn(self.board):
            # three-fold repetition is a draw.
            return 0, []

        moves = antichess_legal_moves(self.board, self.board.legal_moves)
        #if len(list(moves)) == 1:
        #   print("Only 1 antichess legal move: ", list(moves))
        #   return 5000, moves #since this is the only capture move, we have to take it

        best_score = -INFINITE
        pv = []
        for m in moves:
            self.board.push(m)

            # The bounds are inverted and negated due to Negamax.
            child_score, child_pv = self.search(-beta, -alpha, depth - 1, square, ply + 1)
            # The return value is negated due to Negamax.
            child_score = -child_score

            self.board.pop()

            if child_score >= beta:
                # Beta-cutoff. This was a CUT-node.
                if abs(child_score) == INFINITE:
                    return 0, []
                return beta, []

            if child_score > best_score:
                # The best move till now, but PV is not updated since it
                # does not necessarily beat alpha.
                best_score = child_score

                if best_score > alpha:
                    # The move beats (and therefore raises) alpha. PV
                    # can be updated.
                    alpha = best_score
                    pv = [m] + child_pv

        # If alpha was raised (and did not cause a beta-cutoff), then the node
        # is considered a PV-node. Otherwise it is an ALL-node.
        return alpha, pv
