import sys
import copy


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
            goal_size_y = int(goal_components[0])
            goal_size_x = int(goal_components[1])
            goal_pos_y = int(goal_components[2])
            goal_pos_x = int(goal_components[3])
            goal_positions.append((goal_size_x, goal_size_y, goal_pos_x, goal_pos_y))
        return goal_positions

    def check_solved(self):
        results = []
        for goal_index, goal_pos in enumerate(self.goal_positions):
            goal_size_x, goal_size_y, goal_pos_x, goal_pos_y = goal_pos
            goal_met = True
            a = self.board.board[goal_pos_x][goal_pos_y]

            if a == 0:
                goal_met = False

            # Check each cell within the goal area
            for i in range(goal_size_x):
                for j in range(goal_size_y):
                    if not self.is_valid_index(goal_pos_x + i, goal_pos_y + j):
                        goal_met = False
                        break
                    if self.board.board[goal_pos_x + i][goal_pos_y + j] != a:
                        goal_met = False
                        break

            # Check if there are any extra blocks beyond the specified goal area
            if (self.is_valid_index(goal_pos_x + goal_size_x, goal_pos_y) and self.board.board[goal_pos_x + goal_size_x][goal_pos_y]) == a:
                goal_met = False

            if (self.is_valid_index(goal_pos_x, goal_pos_y + goal_size_y) and self.board.board[goal_pos_x][goal_pos_y + goal_size_y] == a):
                goal_met = False

            results.append({
                'goal_index': goal_index,
                'goal_position': (goal_pos_x, goal_pos_y),
                'goal_met': goal_met
            })
        return results

    def check_impossible(self):
        count = 0
        for row in self.board.board:
            count += row.count(0)  # Count the occurrences of 0 in each row
        for goal in self.goal_positions:
            goal_area = goal[0] * goal[1]  # Calculate the goal area directly
            if count < goal_area:
                return True
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
                solved_goals.append(f"{y} {x} {y} {x}")
        return '\n'.join(solved_goals)

    def check_board_against_goals(self, copied_board):
        for goal_pos in self.goal_positions:
            goal_size_x, goal_size_y, goal_pos_x, goal_pos_y = goal_pos
            a = copied_board[goal_pos_x][goal_pos_y]

            if a == 0:
                return False  # Goal block is empty, can't be met

            # Check each cell within the goal area
            for i in range(goal_size_x):
                for j in range(goal_size_y):
                    if not self.is_valid_index(goal_pos_x + i, goal_pos_y + j):
                        return False  # Goal area out of board bounds
                    if copied_board[goal_pos_x + i][goal_pos_y + j] != a:
                        return False  # Goal area contains different block value

            # Check if there are any extra blocks beyond the specified goal area

            if (self.is_valid_index(goal_pos_x + goal_size_x, goal_pos_y) and
                    copied_board[goal_pos_x + goal_size_x][goal_pos_y]) == a:
                return False  # Extra block to the right of the goal area

            if (self.is_valid_index(goal_pos_x - 1, goal_pos_y)) and copied_board[goal_pos_x - 1][goal_pos_y] == a:
                return False # Extra block to the left of the goal area

            if (self.is_valid_index(goal_pos_x, goal_pos_y + goal_size_y) and
                    copied_board[goal_pos_x][goal_pos_y + goal_size_y] == a):
                return False  # Extra block below the goal area

            if (self.is_valid_index(goal_pos_x, goal_pos_y - 1)) and copied_board[goal_pos_x][goal_pos_y - 1] == a:
                return False # Extra block below the goal area

        return True  # All goals are met


class Algorithm:
    def __init__(self, board, checker, question_components):
        self.queue = []
        self.visited = set()
        self.can_move = []
        self.board = board
        self.checker = checker
        self.index = []
        self.question_components = question_components
        self.solution = ""

    def append_answer(self, x, y, new_x, new_y):
        if self.solution == "":
            self.solution = (self.solution + str(y) + " " + str(x) + " " + str(new_y) + " " + str(new_x))
        else:
            self.solution = (self.solution + "\n" + str(y) + " " + str(x) + " " + str(new_y) + " " + str(new_x))


class BFS:
    def __init__(self, board, checker, algo, question_components):
        self.board = board
        self.checker = checker
        self.algo = algo
        self.queue = []
        self.visited = []
        self.question_components = question_components

    def BFS(self):
        block_queue = []
        for block_str in self.question_components[1:]:
            col_no, row_no, block_y, block_x = map(int, block_str.split())
            block_queue.append([col_no, row_no, block_y, block_x])
        inside_queue = [self.board.board, block_queue, []]
        self.queue.append(inside_queue)
        self.visited.append(self.board.board)

        while self.queue:
            current = self.queue.pop(0)
            current_state, block, path = current
            first_block = block.pop(0)
            current_block = first_block
            count = 1
            while count <= len(block) + 1:
                if self.checker.check_board_against_goals(current_state):
                    for vals in path:
                        x, y, new_x, new_y = vals
                        self.algo.append_answer(x, y, new_x, new_y)
                    return

                col_no, row_no, block_y, block_x = current_block
                # print(current_block)
                # print("Columns:", col_no, "Rows:", row_no, "X:", block_x, "Y:", block_y)
                a = current_state[block_x][block_y]
                # print("A:", a)
                copied_board = copy.deepcopy(current_state)
                new_x, new_y = block_x, block_y
                for z in range(len(copied_board) + 1):
                    if self.checker.is_valid_index(new_x + row_no, new_y):
                        if self.checker.is_valid_index(new_x + row_no, new_y) and copied_board[new_x + row_no][new_y] == 0:
                            new_x, new_y, copied_board = self.move_right(new_x, new_y, row_no, col_no, a, copied_board)
                    else:
                        break
                if copied_board not in self.visited:
                    self.visited.append(copied_board)
                    add_block = copy.deepcopy(block)
                    add_path = copy.deepcopy(path)
                    add_block.append([col_no, row_no, new_y, new_x])
                    add_path.append([block_x, block_y, new_x, new_y])
                    self.queue.append([copied_board, add_block, add_path])

                copied_board = copy.deepcopy(current_state)
                new_x, new_y = block_x, block_y
                for z in range(len(copied_board) + 1):
                    if self.checker.is_valid_index(new_x - 1, new_y):
                        if copied_board[new_x - 1][new_y] == 0 and self.checker.is_valid_index(new_x - 1, new_y):
                            # print("left")
                            new_x, new_y, copied_board = self.move_left(new_x, new_y, row_no, col_no, a, copied_board)
                    else:
                        break
                if copied_board not in self.visited:
                    self.visited.append(copied_board)
                    add_block = copy.deepcopy(block)
                    add_path = copy.deepcopy(path)
                    add_block.append([col_no, row_no, new_y, new_x])
                    add_path.append([block_x, block_y, new_x, new_y])
                    self.queue.append([copied_board, add_block, add_path])

                copied_board = copy.deepcopy(current_state)
                new_x, new_y = block_x, block_y
                for z in range(len(copied_board) + 1):
                    if self.checker.is_valid_index(new_x, new_y - 1):
                        if self.checker.is_valid_index(new_x, new_y - 1) and copied_board[new_x][new_y - 1] == 0:
                            new_x, new_y, copied_board = self.move_up(new_x, new_y, row_no, col_no, a, copied_board)
                    else:
                        break
                if copied_board not in self.visited:
                    self.visited.append(copied_board)
                    add_block = copy.deepcopy(block)
                    add_path = copy.deepcopy(path)
                    add_block.append([col_no, row_no, new_y, new_x])
                    add_path.append([block_x, block_y, new_x, new_y])
                    self.queue.append([copied_board, add_block, add_path])

                copied_board = copy.deepcopy(current_state)
                new_x, new_y = block_x, block_y
                for z in range(len(copied_board) + 1):
                    if self.checker.is_valid_index(new_x, new_y + col_no):
                         if self.checker.is_valid_index(new_x, new_y + col_no) and copied_board[new_x][new_y + col_no] == 0:
                            new_x, new_y, copied_board = self.move_down(new_x, new_y, row_no, col_no, a, copied_board)
                    else:
                        break
                if copied_board not in self.visited:
                    self.visited.append(copied_board)
                    add_block = copy.deepcopy(block)
                    add_path = copy.deepcopy(path)
                    add_block.append([col_no, row_no, new_y, new_x])
                    add_path.append([block_x, block_y, new_x, new_y])
                    self.queue.append([copied_board, add_block, add_path])

                block.append([col_no, row_no, block_y, block_x])
                current_block = block.pop(0)
                count += 1

        return -1

    def move_right(self, x, y, row_no, col_no, a, copied_board):
        current_x = x
        if self.checker.is_valid_index(current_x + row_no, y):
            for i in range(col_no):
                if copied_board[current_x + row_no][y + i] != 0:
                    return current_x, y, copied_board

            if copied_board[current_x + row_no][y] == 0:
                for i in range(col_no):
                    copied_board[current_x][y + i] = 0
                    copied_board[current_x + row_no][y + i] = a
                current_x += 1  # Move to the next position
        # Return the final position after all valid moves
        return current_x, y, copied_board

    def move_left(self, x, y, row_no, col_no, a, copied_board):
        current_x = x
        if self.checker.is_valid_index(current_x - 1, y) and self.checker.is_valid_index(current_x - 1 + row_no, y):
            for i in range(col_no):
                if copied_board[current_x - 1][y + i] != 0:
                    return current_x, y, copied_board

            if copied_board[current_x - 1][y] == 0:
                for i in range(col_no):
                    copied_board[current_x - 1+ row_no][y + i] = 0
                    copied_board[current_x - 1][y + i] = a
                current_x -= 1  # Move to the next position
        # Return the final position after all valid moves
        return current_x, y, copied_board

    def move_up(self, x, y, row_no, col_no, a, copied_board):
        current_y = y

        for i in range(row_no):
            if copied_board[x + i][current_y - 1] != 0:
                return x, current_y, copied_board

        if copied_board[x][current_y - 1] == 0:
            for i in range(row_no):
                copied_board[x + i][current_y - 1 + col_no] = 0
                copied_board[x + i][current_y - 1] = a
            current_y -= 1  # Move to the next position

        # Return the final position after all valid moves
        return x, current_y, copied_board

    def move_down(self, x, y, row_no, col_no, a, copied_board):
        current_y = y

        for i in range(row_no):
            if copied_board[x + i][current_y + col_no] != 0:
                return x, current_y, copied_board

        if copied_board[x][current_y + col_no] == 0:
            for i in range(row_no):
                copied_board[x + i][current_y] = 0
                copied_board[x + i][current_y + col_no] = a
            current_y += 1  # Move to the next position

        # Return the final position after all valid moves
        return x, current_y, copied_board

    def is_board_in_visited(self, board):
        for new in self.visited:
            if board == new:
                return True
        return False


def main(question, goal):
    question_components = question.strip().split('\n')
    y, x = map(int, question_components[0].split())  # Extracting x and y coordinates
    board = Board(x, y)  # Creating the board object
    goal_board = Board(x, y)

    block_value = 1
    for line in question_components[1:]:
        if line != '':
            col_no, row_no, block_y, block_x = map(int, line.split())
            board.append_matrix(block_x, block_y, row_no, col_no, block_value)
            block_value += 1

    checker = Checker(board, goal)
    algo = Algorithm(board, checker, question_components)
    bfs = BFS(board, checker, algo, question_components)

    # Get the list of all goals and their statuses
    goal_results = checker.check_solved()

    # Separate goals into solved and unsolved categories
    solved_goals = [goal for goal in goal_results if goal['goal_met']]
    unsolved_goals = [goal for goal in goal_results if not goal['goal_met']]

    # Process already solved goals
    if solved_goals:
        already_solved_output = checker.already_solved()
        if algo.solution != "":
            algo.solution = "\n" + algo.solution + str(already_solved_output)
        else:
            algo.solution = algo.solution + str(already_solved_output)

    for goal in goal_results:
        if not goal['goal_met']:
            if checker.check_impossible():
                return '-1'

    # Process unsolved goals
    if unsolved_goals:
        result = bfs.BFS()
        if result == -1:
            return -1

    return algo.solution


if __name__ == '__main__':
    q = sys.argv[1]
    g = sys.argv[2]
    g = open(g)
    q = open(q)
    q = q.read()
    g = g.read()
    print(main(q, g))
