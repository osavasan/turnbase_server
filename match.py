import uuid

class Match(object):

    def __init__(self, game_class):
        """
        Ctor

        :param game_class: game class to instantiate
        :return:
        """

        self.id = uuid.uuid4()
        self.game = game_class()

    def join_player(self):
        """
        Join a player
        """

        try:
            player , player_id = self.game.get_player()
        except IndexError:
            raise Exception("Can not join")

        player_info = {
            "id": self.id.__str__(),
            "player": player,
            "player_id" : player_id
        }

        return player_info

    def make_turn(self, match_id, *args):
        """
        Return tuple of (is_finished, is_win) booleans
        """

        if isinstance(match_id, (str, unicode)):
            match_id = uuid.UUID(match_id)
        if match_id != self.id:
            raise Exception("You must join this match first", self.id)

        result = self.game.make_turn(*args)

        return result
