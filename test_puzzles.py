import unittest
import subprocess
from sliding import Board
from sliding import Checker
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


class TestChecker(unittest.TestCase):
    def test_solve_init(self):
        board = Board(2, 2)
        goal = '1 1 0 0'
        checker = Checker(board, goal)
        self.assertEqual([(1, 1, 0, 0)], checker.goal_positions)

    def test_solve_check_solved_true_easy1(self):
        board = Board(2, 2)
        board.append_matrix(0, 0, 1, 1, 1)
        goal = '1 1 0 0'
        checker = Checker(board, goal)
        self.assertEqual([{'goal_index': 0, 'goal_met': True, 'goal_position': (0, 0)}], checker.check_solved())

    def test_solve_check_solved_true_easy2(self):
        board = Board(2, 2)
        board.append_matrix(0, 0, 2, 2, 1)
        goal = '2 2 0 0'
        checker = Checker(board, goal)
        self.assertTrue(checker.check_solved())

    def test_solve_check_solved_false_easy2(self):
        board = Board(4, 4)
        board.append_matrix(0, 0, 2, 1, 1)
        goal = '2 2 0 0'
        checker = Checker(board, goal)
        self.assertEqual([{'goal_index': 0, 'goal_met': False, 'goal_position': (0, 0)}], checker.check_solved())

    def test_already_solved(self):
        board = Board(4, 4)
        board.append_matrix(0, 0, 2, 2, 1)
        goal = '2 2 0 0'
        checker = Checker(board, goal)
        self.assertEqual('0 0 0 0', checker.already_solved())


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
        question = '1 2\n1 1 0 0\n 1 1 0 1 '
        goal = '1 1 0 1\n1 1 0 0'
        self.assertEqual('0 1 0 1\n0 0 0 0', sliding.main(question, goal))

    def test_140x140(self):
        command = 'python3 sliding.py puzzles/easy/140x140 puzzles/easy/140x140.goal'
        output = subprocess.check_output(command, shell=True)
        output_str = output.decode("utf-8")
        output_str = output_str.strip()
        self.assertEqual('139 0 139 139', output_str)

    def test_140x140_impossible(self):
        command = 'python3 sliding.py puzzles/easy/140x140 puzzles/easy/140x140.impossible.goal'
        output = subprocess.check_output(command, shell=True)
        output_str = output.decode("utf-8")
        output_str = output_str.strip()
        self.assertEqual('-1', output_str)

    def test_140x140_goal2(self):
        command = 'python3 sliding.py puzzles/easy/140x140 puzzles/easy/140x140.goal.2'
        output = subprocess.check_output(command, shell=True)
        output_str = output.decode("utf-8")
        output_str = output_str.strip()
        self.assertEqual('\n'.join([f'{i} 0 {i} 0' for i in range(140)]), output_str)

    def test_big_block_1(self):
        command = 'python3 sliding.py puzzles/easy/big.block.1 puzzles/easy/big.block.1.goal'
        output = subprocess.check_output(command, shell=True)
        output_str = output.decode("utf-8")
        output_str = output_str.strip()
        self.assertEqual('0 0 0 0\n0 2 0 2\n2 0 2 0\n2 0 1 0\n2 2 2 0', output_str)

    def test_big_block_2(self):
        command = 'python3 sliding.py puzzles/easy/big.block.2 puzzles/easy/big.block.2.goal'
        output = subprocess.check_output(command, shell=True)
        output_str = output.decode("utf-8")
        output_str = output_str.strip()
        self.assertEqual('0 0 0 0\n0 2 0 2\n2 0 2 0\n2 0 2 2\n1 0 2 0', output_str)

    def test_big_block_3(self):
        command = 'python3 sliding.py puzzles/easy/big.block.3 puzzles/easy/big.block.3.goal'
        output = subprocess.check_output(command, shell=True)
        output_str = output.decode("utf-8")
        output_str = output_str.strip()
        self.assertEqual('0 0 0 0\n0 2 0 2\n2 0 2 0\n0 2 2 2\n0 1 0 2', output_str)

    def test_big_block_4(self):
        command = 'python3 sliding.py puzzles/easy/big.block.4 puzzles/easy/big.block.4.goal'
        output = subprocess.check_output(command, shell=True)
        output_str = output.decode("utf-8")
        output_str = output_str.strip()
        self.assertEqual('0 0 0 0\n0 2 0 2\n2 0 2 0\n2 3 2 3\n1 1 1 3\n1 0 1 2\n2 0 1 0\n2 2 2 0\n1 2 2 2\n2 2 2 3', output_str)

    def test_big_search_1(self):
        command = 'python3 sliding.py puzzles/easy/big.search.1 puzzles/easy/big.search.1.goal'
        output = subprocess.check_output(command, shell=True)
        output_str = output.decode("utf-8")
        output_str = output_str.strip()
        self.assertEqual('0 1 0 1\n0 2 0 2\n1 0 1 0\n1 1 1 1\n1 2 1 2\n2 0 2 0\n2 1 2 1\n0 1 0 0\n0 2 0 1\n1 2 0 2\n2 2 1 2',
                         output_str)

    def test_big_search_2(self):
        command = 'python3 sliding.py puzzles/easy/big.search.2 puzzles/easy/big.search.2.goal'
        output = subprocess.check_output(command, shell=True)
        output_str = output.decode("utf-8")
        output_str = output_str.strip()
        self.assertEqual('0 1 0 1\n0 2 0 2\n1 0 1 0\n1 1 1 1\n1 2 1 2\n2 0 2 0\n2 1 2 1\n1 2 2 2\n0 2 1 2\n0 1 0 2\n0 0 0 1', output_str)

    def test_big_tray_2(self):
        command = 'python3 sliding.py puzzles/easy/big.tray.2 puzzles/easy/big.tray.2.goal'
        output = subprocess.check_output(command, shell=True)
        output_str = output.decode("utf-8")
        output_str = output_str.strip()
        self.assertEqual('0 0 99 0', output_str)

    def test_check_diff_blocks(self):
        command = 'python3 sliding.py puzzles/easy/check.diff.blocks puzzles/easy/check.diff.blocks.goal'
        output = subprocess.check_output(command, shell=True)
        output_str = output.decode("utf-8")
        output_str = output_str.strip()
        self.assertEqual('0 0 1 0\n0 2 0 0\n1 0 1 1\n1 1 0 1', output_str)

    def test_easy(self):
        command = 'python3 sliding.py puzzles/easy/easy puzzles/easy/easy.goal'
        output = subprocess.check_output(command, shell=True)
        output_str = output.decode("utf-8")
        output_str = output_str.strip()
        self.assertEqual('0 1 1 1', output_str)


if __name__ == '__main__':
    unittest.main()
