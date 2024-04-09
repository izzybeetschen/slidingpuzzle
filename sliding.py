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
            if (self.is_valid_index(goal_pos_x + goal_size_x, goal_pos_y) and
                self.board.board[goal_pos_x + goal_size_x][goal_pos_y]) == a:
                goal_met = False

            if (self.is_valid_index(goal_pos_x, goal_pos_y + goal_size_y) and
                    self.board.board[goal_pos_x][goal_pos_y + goal_size_y] == a):
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
            print(goal_size_x, goal_size_y, goal_pos_x, goal_pos_y)
            for i in range(len(self.board.board)):
                for j in range(len(self.board.board[i])):
                    if self.board.board[i][j] != 0:
                        print(self.find_goal_blocks(i, j))
                        if not self.find_goal_blocks(i, j):
                            z = self.board.board[i][j]
                            print(z)
                            col_no, row_no, block_x, block_y = map(int, self.question_components[z].split())
                            if row_no == goal_size_x and col_no == goal_size_y:
                                if z not in self.index:
                                    self.index.append(z)
                                    row_no, col_no, block_x, block_y = map(int, self.question_components[z].split())
                                    self.can_move.append([i, j, row_no, col_no, z])

    def find_goal_blocks(self, x, y):
        for goal_pos in self.checker.goal_positions:
            goal_x, goal_y, goal_pos_x, goal_pos_y = goal_pos

            # Check if the block (x, y) is within the bounds of the goal area
            if goal_pos_x <= x < goal_pos_x + goal_x and goal_pos_y <= y < goal_pos_y + goal_y:
                z = self.board.board[goal_pos_x][goal_pos_y]

                # Check if all cells within the goal area match the block value at the top-left corner
                for i in range(goal_x):
                    for j in range(goal_y):
                        if not self.checker.is_valid_index(goal_pos_x + i, goal_pos_y + j):
                            return False
                        if self.board.board[goal_pos_x + i][goal_pos_y + j] != z:
                            return False

                # Check if there are no blocks outside the specified goal area adjacent to it
                if (not self.checker.is_valid_index(goal_pos_x + goal_x, goal_pos_y) or
                        self.board.board[goal_pos_x + goal_x][goal_pos_y] == z):
                    return True

                if (not self.checker.is_valid_index(goal_pos_x, goal_pos_y + goal_y) or
                        self.board.board[goal_pos_x][goal_pos_y + goal_y] == z):
                    return True

        return False

    def move_block(self, unsolved_goals):
        for block in self.can_move:
            x, y, row_no, col_no, a = block

            goal_met = False  # Initialize goal_met flag
            while unsolved_goals:
                for goal in unsolved_goals:
                    goal_pos_x, goal_pos_y = goal['goal_position']

                    if goal_pos_x == x and goal_pos_y == y:
                        goal_met = True
                        break  # No need to move this block, it's already at its goal position

                    # Move the block towards the goal position
                    while not goal_met:
                        if goal_pos_x > x and self.board.board[x+col_no][y] == 0:
                            # print("right")
                            new_x, new_y = self.move_right(x, y, col_no, a, goal_pos_x, goal_pos_y)
                            if (new_x, new_y) == (x, y):  # Check if no movement occurred
                                break
                            self.append_answer(x, y, new_x, new_y)
                            x, y = new_x, new_y
                        elif goal_pos_x < x and self.board.board[x-1][y] == 0:
                            # print('left')
                            new_x, new_y = self.move_left(x, y, row_no, a, goal_pos_x, goal_pos_y)
                            if (new_x, new_y) == (x, y):  # Check if no movement occurred
                                break
                            self.append_answer(x, y, new_x, new_y)
                            x, y = new_x, new_y
                        elif goal_pos_y > y:
                            # print('down')
                            new_x, new_y = self.move_down(x, y, col_no, row_no, a, goal_pos_x, goal_pos_y)
                            if (new_x, new_y) == (x, y):  # Check if no movement occurred
                                break
                            self.append_answer(x, y, new_x, new_y)
                            x, y = new_x, new_y
                        elif goal_pos_y < y:
                            # print('up')
                            new_x, new_y = self.move_up(x, y, col_no, row_no, a, goal_pos_x, goal_pos_y)
                            if (new_x, new_y) == (x, y):  # Check if no movement occurred
                                break
                            self.append_answer(x, y, new_x, new_y)
                            x, y = new_x, new_y

                        # Check if the block has reached the goal position
                        if (x, y) == (goal_pos_x, goal_pos_y):
                            goal_met = True  # Block has reached its goal position
                            break  # Exit the while loop
                    if goal_met is True:
                        self.can_move.remove(block)
                        unsolved_goals.remove(goal)

    def move_up(self, x, y, col_no, row_no, a, goal_x, goal_y):
        z = y - 1
        new_x, new_y = x, y

        last_dist = 1000
        while self.checker.is_valid_index(x, z - 1):
            current_dist = self.manhatten_distance(goal_x, goal_y, x, z)
            if current_dist < last_dist:
                if self.board.board[x][z] == 0:
                    for i in range(row_no):
                        self.board.board[x+i][z + 1] = 0
                        self.board.board[x+i][z] = a
                        new_y, new_x = z, y
                        z -= 1
                        last_dist = current_dist
                else:
                    return new_x, new_y
            else:
                return new_x, new_y
        return new_x, new_y

    def move_down(self, x, y, col_no, row_no, a, goal_x, goal_y):
        z = y
        new_x, new_y = x, y

        last_dist = 1000
        while self.checker.is_valid_index(x, z+row_no):
            current_dist = self.manhatten_distance(goal_x, goal_y, x, z)
            if current_dist < last_dist:
                if self.board.board[x][z+row_no] == 0:
                    for i in range(row_no):
                        self.board.board[x + i][z] = 0
                        self.board.board[x + i][z+row_no] = a
                        z += 1
                        new_y, new_x = z, x
                        last_dist = current_dist
                else:
                    return new_x, new_y
            else:
                return new_x, new_y
        return new_x, new_y

    def move_left(self, x, y, row_no, a, goal_x, goal_y):
        z = x - 1
        new_x, new_y = x, y

        last_dist = 1000

        while self.checker.is_valid_index(z, y):
            current_dist = self.manhatten_distance(goal_x, goal_y, z, y)
            if current_dist < last_dist:
                if self.board.board[z][y] == 0:
                    self.board.board[z + row_no][y] = 0
                    self.board.board[z][y] = a
                    new_x, new_y = z, y
                    z -= 1
                    last_dist = current_dist
                else:
                    return new_x, new_y
            else:
                return new_x, new_y
        return new_x, new_y

    def move_right(self, x, y, row_no, a, goal_x, goal_y):
        z = x
        new_x, new_y = x, y
        last_dist = 10000
        while self.checker.is_valid_index(z + row_no, y):
            current_dist = self.manhatten_distance(goal_x, goal_y, z - 1, y)
            if current_dist < last_dist:
                if self.board.board[z + row_no][y] == 0:
                    self.board.board[z][y] = 0
                    self.board.board[z + row_no][y] = a
                    z += 1
                    new_x, new_y = z, y
                    last_dist = current_dist
                else:
                    return new_x, new_y
            else:
                return new_x, new_y
        return new_x, new_y

    @staticmethod
    def manhatten_distance(goal_x, goal_y, current_x, current_y):
        return abs(goal_x - current_x) + abs(goal_y - current_y)

    def append_answer(self, x, y, new_x, new_y):
        if self.solution == "":
            self.solution = (self.solution + str(y) + " " + str(x) + " " + str(new_y) + " " + str(new_x))
        else:
            self.solution = (self.solution + "\n" + str(y) + " " + str(x) + " " + str(new_y) + " " + str(new_x))


def main(question, goal):
    question_components = question.strip().split('\n')
    y, x = map(int, question_components[0].split())  # Extracting x and y coordinates
    board = Board(x, y)  # Creating the board object

    block_value = 1
    for line in question_components[1:]:
        if line != '':
            col_no, row_no, block_y, block_x = map(int, line.split())
            board.append_matrix(block_x, block_y, row_no, col_no, block_value)
            block_value += 1

    checker = Checker(board, goal)
    algo = Algorithm(board, checker, question_components)

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
        if len(unsolved_goals) == 1:
            algo.find_block_to_move()
            algo.move_block(unsolved_goals)
        else:
            algo.find_block_to_move()
            print(algo.can_move)

    return algo.solution


if __name__ == '__main__':
    q = sys.argv[1]
    g = sys.argv[2]
    g = open(g)
    q = open(q)
    q = q.read()
    g = g.read()
    print(main(q, g))
