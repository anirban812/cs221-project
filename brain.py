#!/usr/bin/env python

import random

# Abstract class, defining what needs to be implemented to be an AI.
class PPLBrain:

  # Given a board, return a list of moves that the agent should take.
  # Each element of the list should be a tuple: ((rowIndex, colIndex), clear)
  # Indices are 0-indexed counting from the bottom-left corner.
  # Set the clear boolean flag to True if the move results in a clear.
  # So, moving to the bottom-left corner to clear blocks would be ((0, 0), True)
  def getNextMoves(self, board): raise NotImplementedError('Override me')


class BaselineBrain(PPLBrain):
  # Return a 5 random moves.
  def getNextMoves(self, board):
    max_row_index = 11
    max_col_index = 5
    moves = []
    for _ in range(5):
      clear = False
      row_index = random.randint(0, max_row_index)
      col_index = random.randint(0, max_col_index)
      move = ((row_index, col_index), clear)
      moves.append(move)
    return moves
