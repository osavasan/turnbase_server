import unittest

import tictactoe


class MyTestCase(unittest.TestCase):

    def test_basics(self):
        game = tictactoe.TicTacToe()
        self.assertEqual(len(game.board), 9)

    def test_turn_restrictions(self):
        game = tictactoe.TicTacToe()

        # unknown player
        with self.assertRaises(TypeError):
            game.make_turn("Z", 3)

        # correct turn
        game.make_turn("X", 3)
        self.assertEqual(game.board[3], "X")

        # out of turn
        with self.assertRaises(tictactoe.IncorrectTurn) as ar:
            game.make_turn("X", 3)
        self.assertEqual(ar.exception.message, "Current player O")

        # filled cell
        with self.assertRaises(tictactoe.IncorrectTurn) as ar:
            game.make_turn("O", 3)
        self.assertEqual(ar.exception.message, "The cell 3 is already filled")

    def test_wins_and_finish(self):

        game = tictactoe.TicTacToe()

        self.assertFalse(game.is_win())

        game.make_turn("X", 0)
        game.make_turn("O", 4)
        game.make_turn("X", 1)
        is_finished, is_win = game.make_turn("O", 8)

        # X X _
        # _ O _
        # _ _ O

        self.assertFalse(is_finished)
        self.assertFalse(is_win)

        is_finished, is_win = game.make_turn("X", 2)

        # X X X
        # _ O _
        # _ _ O

        self.assertTrue(is_finished)
        self.assertTrue(is_win)

        with self.assertRaises(tictactoe.IncorrectTurn) as ar:
            game.make_turn("O", 3)
        self.assertEqual(ar.exception.message, "The game is over")

if __name__ == '__main__':
    unittest.main()
