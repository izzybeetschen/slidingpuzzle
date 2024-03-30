import unittest
from sliding import Board
from sliding import Solver
import sliding


class TestBoard(unittest.TestCase):
    def test_board_init(self):
        board = Board(2, 3)
        self.assertEqual(2, board.x)
        self.assertEqual(3, board.y)
        self.assertEqual(board.board, [[0, 0, 0], [0, 0, 0]])

    def test_board_append(self):
        board = Board(3, 3)
        board.append_matrix(0, 0, 2, 2, 1)
        self.assertEqual(board.board, [[1, 1, 0], [1, 1, 0], [0, 0, 0]])


class TestSolver(unittest.TestCase):
    def test_solve_init(self):
        board = Board(2, 2)
        goal = '1 1 0 0'
        solver = Solver(board, goal)
        self.assertEqual([(1, 1, 0, 0)], solver.goal_positions)

    def test_solve_check_solved_true_easy1(self):
        board = Board(2, 2)
        board.append_matrix(0, 0, 1, 1, 1)
        goal = '1 1 0 0'
        solver = Solver(board, goal)
        self.assertEqual([{'goal_index': 0, 'goal_met': True, 'goal_position': (0, 0)}], solver.check_solved())

    def test_solve_check_solved_true_easy2(self):
        board = Board(2, 2)
        board.append_matrix(0, 0, 2, 2, 1)
        goal = '2 2 0 0'
        solver = Solver(board, goal)
        self.assertTrue(solver.check_solved())

    def test_solve_check_solved_false_easy2(self):
        board = Board(4, 4)
        board.append_matrix(0, 0, 2, 1, 1)
        goal = '2 2 0 0'
        solver = Solver(board, goal)
        self.assertEqual([{'goal_index': 0, 'goal_met': False, 'goal_position': (0, 0)}], solver.check_solved())

    def test_already_solved(self):
        board = Board(4, 4)
        board.append_matrix(0, 0, 2, 2, 1)
        goal = '2 2 0 0'
        solver = Solver(board, goal)
        self.assertEqual('0 0 0 0', solver.already_solved())


class EasyTests(unittest.TestCase):
    def test_one_by_one(self):
        question = '1 1 \n1 1 0 0 '
        goal = '1 1 0 0'
        self.assertEqual('0 0 0 0', sliding.main(question, goal))

    def test_one_by_two_one_block(self):
        question = '1 2 \n1 2 0 0 '
        goal = '1 2 0 0'
        self.assertEqual('0 0 0 0', sliding.main(question, goal))

    def test_one_by_two_two_blocks(self):
        question = '1 2 \n1 1 0 0\n 1 1 0 1 '
        goal = '1 1 0 1\n 1 1 0 0'
        self.assertEqual('0 1 0 1\n0 0 0 0', sliding.main(question, goal))

    def test_140x140(self):
        question = '\n'.join(['140 140'] + [f'1 140 {i} 0' for i in range(140)])
        goal = '1 1 139 139'
        self.assertEqual('139 0 139 139', sliding.main(question, goal))


if __name__ == '__main__':
    unittest.main()
