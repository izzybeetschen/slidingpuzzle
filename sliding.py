import sys

"""Collects data on th question and goal to be used in the code"""
def get_data():
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
        self.x = x
        self.y = y
        self.board = self.create_blank_matrix()

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


class Solver:
    def __init__(self, board, goal):
        self.board = board
        self.goal = goal
        goal_components = goal.split()
        self.goal_size_x = int(goal_components[0])
        self.goal_size_y = int(goal_components[1])
        self.goal_pos_x = int(goal_components[2])
        self.goal_pos_y = int(goal_components[3])

    def check_solved(self, board, goal_size_x, goal_size_y, goal_pos_x, goal_pos_y):
        if board[goal_pos_x][goal_pos_y] != 0:
            pass
        else:
            return False

    def check_impossible(self, board, goal_size_x, goal_size_y, goal_pos_x, goal_pos_y):
        count = 0
        for row in self.board:
            count += row.count(0)  # Count the occurrences of 0 in each row
        goal_area = goal_size_x * goal_size_y
        if count < goal_area:
            return True
        else:
            return False
