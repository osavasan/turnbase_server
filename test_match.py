import unittest

import match


class GameMock(object):

    def __init__(self):
        self.players = ["A"]

    def get_player(self):
        return self.players.pop()


class MatchTestCase(unittest.TestCase):

    def test(self):
        m = match.Match(GameMock)

        self.assertIsInstance(m.game, GameMock)

        player_info = m.join_player()
        self.assertEqual(player_info["player"], "A")
        self.assertEqual(player_info["id"], m.id.__str__())

        with self.assertRaises(Exception) as ar:
            m.join_player()
        self.assertEqual(ar.exception.message, "Can not join")

        with self.assertRaises(Exception) as ar:
            m.make_turn("00000000-0000-0000-0000-000000000000", "a", "b", "c")
        self.assertEqual(ar.exception.args, ("You must join this match first", m.id))

if __name__ == '__main__':
    unittest.main()
