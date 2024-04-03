import sys


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


class Checker:
    def __init__(self, board, goal):
        self.board = board
        self.goal = goal
        self.goal_positions = self.parse_goal(goal)

    @staticmethod
    def parse_goal(goal):
        goals = goal.strip().split('\n')
        goal_positions = []
        for goal_str in goals:
            goal_components = goal_str.split()
            goal_size_x = int(goal_components[0])
            goal_size_y = int(goal_components[1])
            goal_pos_x = int(goal_components[2])
            goal_pos_y = int(goal_components[3])
            goal_positions.append((goal_size_x, goal_size_y, goal_pos_x, goal_pos_y))
        return goal_positions

    def check_solved(self):
        results = []
        for idx, goal_pos in enumerate(self.goal_positions):
            goal_size_x, goal_size_y, goal_pos_x, goal_pos_y = goal_pos
            val = self.board.board[goal_pos_x][goal_pos_y]
            goal_met = True

            for i in range(goal_size_x):
                for j in range(goal_size_y):
                    if self.is_valid_index(goal_pos_x + i, goal_pos_y + j):
                        if self.board.board[goal_pos_x + i][goal_pos_y + j] != val:
                            goal_met = False
                            break

            if self.is_valid_index(goal_pos_x + goal_size_x + 1, goal_pos_y + goal_size_y + 1):
                if (self.board.board[goal_pos_x + goal_size_x + 1][goal_pos_y] == val or
                        self.board.board[goal_pos_x][goal_pos_y + goal_size_y + 1] == val):
                    goal_met = False
            elif self.is_valid_index(goal_pos_x - 1, goal_pos_y - 1):
                if (self.board.board[goal_pos_x - 1][goal_pos_y] == val or self.board.board[goal_pos_x][goal_pos_y - 1]
                        == val):
                    goal_met = False

            results.append({
                'goal_index': idx,
                'goal_position': (goal_pos_x, goal_pos_y),
                'goal_met': goal_met
            })

        return results

    def check_impossible(self):
        count = 0
        for row in self.board.board:
            count += row.count(0)  # Count the occurrences of 0 in each row
        goal_area = sum(goal[0] * goal[1] for goal in self.goal_positions)
        if count < goal_area:
            return True
        else:
            return False

    def is_valid_index(self, x, y):
        return 0 <= x < len(self.board.board) and 0 <= y < len(self.board.board[0])

    def find_empty_tile(self):
        empty_tile = set()
        for i in range(len(self.board.board)):
            for j in range(len(self.board.board[i])):
                if self.board.board[i][j] == 0:
                    empty_tile.add((i, j))
        return empty_tile

    def already_solved(self):
        solved_goals = []
        for goal in self.check_solved():
            if goal['goal_met']:
                x, y = goal['goal_position']
                solved_goals.append(f"{x} {y} {x} {y}")
        return '\n'.join(solved_goals)

    def append_output(self):
        pass


class Algorithm:
    def __init__(self, board, checker, question_components):
        self.queue = []
        self.visited = []
        self.can_move = []
        self.board = board
        self.checker = checker
        self.index = []
        self.question_components = question_components
        self.solution = ""

    def find_block_to_move(self):
        for goal_pos_tuple in self.checker.goal_positions:
            goal_size_x, goal_size_y, goal_pos_x, goal_pos_y = goal_pos_tuple
            for i in range(len(self.board.board)):
                for j in range(len(self.board.board[i])):
                    if self.board.board[i][j] != 0:
                        if not self.find_goal_blocks(i, j):
                            z = self.board.board[i][j]
                            row_no, col_no, block_x, block_y = map(int, self.question_components[z].split())
                            if row_no == goal_size_x and col_no == goal_size_y:
                                if z not in self.index:
                                    self.index.append(z)
                                    row_no, col_no, block_x, block_y = map(int, self.question_components[z].split())
                                    self.can_move.append([j, i, row_no, col_no, z])

    def find_goal_blocks(self, x, y):
        for goal_pos in self.checker.goal_positions:
            goal_x, goal_y, goal_pos_x, goal_pos_y = goal_pos
            if goal_pos_x <= x < goal_pos_x + goal_x and goal_pos_y <= y < goal_pos_y + goal_y:
                return True
        return False

    def move_block(self):
        for block in self.can_move:
            x, y, row_no, col_no, a = block
            for goal_pos_tuple in self.checker.goal_positions:
                goal_size_x, goal_size_y, goal_pos_x, goal_pos_y = goal_pos_tuple
                print(x)
                print(goal_pos_x)
                if goal_pos_x > x:
                    new_x, new_y = self.move_right(x, y, row_no, a)
                    self.append_answer(x, y, new_x, new_y)

    def move_up(self):
        pass

    def move_down(self):
        pass

    def move_left(self):
        pass

    def move_right(self, x, y, row_no, a):
        z = x + 1
        while self.board.board[z + row_no][y] != 0:
            self.board.board[z - 1][y] = 0
            self.board.board[z + row_no][y] = a
            z += 1
        new_x, new_y = z - 1, y
        return new_x, new_y

    def append_answer(self, x, y, new_x, new_y):
        self.solution = (self.solution + str(x) + " " + str(y) + " " + str(new_x) + " " + str(new_y) + "\n")


def main(question, goal):
    question_components = question.strip().split('\n')
    x, y = map(int, question_components[0].split())  # Extracting x and y coordinates
    board = Board(x, y)  # Creating the board object

    block_value = 1
    for line in question_components[1:]:
        if line != '':
            row_no, col_no, block_x, block_y = map(int, line.split())
            board.append_matrix(block_x, block_y, row_no, col_no, block_value)
            block_value += 1

    checker = Checker(board, goal)
    for goal_result in checker.check_solved():
        if goal_result['goal_met']:
            return checker.already_solved()
    if checker.check_impossible():
        return -1
    algo = Algorithm(board, checker, question_components)
    algo.find_block_to_move()
    algo.move_block()
    print(algo.can_move)
    print(algo.solution)


if __name__ == '__main__':
    q = sys.argv[1]
    g = sys.argv[2]
    g = open(g)
    q = open(q)
    q = q.read()
    g = g.read()
    print(g)
    print(q)
    print(main(q, g))
