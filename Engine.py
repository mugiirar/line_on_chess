"""
manage moves
"""

class State():
    def __init__(self):
        self.board = [
                 ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],  # Black back rank
                 ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],  # Black pawns
                 ["--", "--", "--", "--", "--", "--", "--", "--"],  # Empty squares
                 ["--", "--", "--", "--", "--", "--", "--", "--"],  # Empty squares
                 ["--", "--", "--", "--", "--", "--", "--", "--"],  # Empty squares
                 ["--", "--", "--", "--", "--", "--", "--", "--"],  # Empty squares
                 ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],  # White pawns
                 ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]   # White back rank
        ]


class move():
    def __init__(self, sq_one, sq_two, board):
        self.rowOne = sq_one[0]
        self.colOne = sq_one[1]

        self.rowTwo = sq_two[0]
        self.colTwo = sq_two[1]

        self.pieceChange = board[self.rowOne][self.colOne]
        self.pieceCaptured = board[self.rowTwo][self.colTwo]

        board[self.rowTwo][self.colTwo] = board[self.rowOne][self.colOne]
        board[self.rowOne][self.colOne] = "--"
