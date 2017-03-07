class IncorrectTurn(Exception):
    pass


class TicTacToe(object):
    """
    Classic TicTacToe game
    """

    WINNING_POSITIONS = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    )

    def __init__(self):
        self.board = [None] * 9
        self.current_player = "X"
        self.finished = False
        self.players = ["X", "O"]
        self.last_player_id = 0
        self.game_session = 0

    def get_player(self):
        self.last_player_id += 1
        return self.players.pop(), self.last_player_id

    def make_turn(self, player, position):
        """
        Returns (is_finished, is_win) booleans tuple

        :param player: "X" or "O"
        :param position:
        0 1 2
        3 4 5
        6 7 8
        :return:
        """
        if self.finished:
            raise IncorrectTurn("The game is over")

        if player not in ("X", "O"):
            raise TypeError()

        if player != self.current_player:
            raise IncorrectTurn("Current player {}".format(self.current_player))

        cell = self.board[position]
        if cell is not None:
            raise IncorrectTurn("The cell {} is already filled".format(position))

        self.board[position] = player
        self.current_player = "X" if self.current_player == "O" else "O"

        is_win = self.is_win()
        self.finished = self.is_filled() or is_win

        return self.finished, is_win

    def is_win(self):
        """
        Returns True if winning position occured
        :return:
        """
        for wp in TicTacToe.WINNING_POSITIONS:
            if self.board[wp[0]] == self.board[wp[1]] == self.board[wp[2]] is not None:
                return True
        return False

    def is_filled(self):
        """
        Returns True when all cell are filled
        :return:
        """
        return all((c is not None for c in self.board))
