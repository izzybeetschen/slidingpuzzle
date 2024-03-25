import unittest
from sliding import Board
from sliding import Solver


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
        self.assertEqual(1, solver.goal_size_x)
        self.assertEqual(1, solver.goal_size_y)


if __name__ == '__main__':
    unittest.main()
