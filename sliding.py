import sys

"""Collects data on th question and goal to be used in the code"""
question = sys.argv[1]
goal = sys.argv[2]
goal = open(goal)
question = open(question)
question = question.read()
goal = goal.read()
print(question)  # Remove this
print(goal)  # Remove this


class Board:
    def __init__(self, x, y):
        self.board = self.create_blank_matrix()
        self.x = x
        self.y = y

    def create_blank_matrix(self):
        matrix = []
        for i in range(self.x):
            row = []
            for j in range(self.y):
                row.append(0)
            matrix.append(row)
        return matrix

    def append_matrix(self, block_x, block_y, row_no, col_no, block_value):
        for i in range(row_no):  # row = x
            for j in range(col_no):  # col = y
                self.board[block_x + i][block_y + j] = block_value
