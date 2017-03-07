import uuid


class GameRoom(object):
    """
    Game Room Class
    """

    game_key = "tictactoe"
    room_size = 2
    remaining_slot = 2
    current_turn = 1
    current_player = 1

    def __init__(self):
        self.room_id = uuid.uuid4().__str__()
        self.players = {}
        self.remaining_slot = self.room_size
        self.player_order_id = 0
        self.current_turn = 1

    def add_player(self, player_id):
        self.player_order_id += 1
        self.players[player_id] = self.player_order_id
        self.remaining_slot -= 1
        player_info = {
            "room_id": self.room_id,
            "player_order_id": self.player_order_id,
            "player_id" : player_id,
        }
        return player_info

    def make_turn(self, *args):
        param_room_id = args[0]
        param_player_id = args[1]
        message = args[2]
        if param_room_id != self.room_id:
            return {"status": "error", "message": "Invalid room"}
        if self.remaining_slot > 0:
            return {"status": "error", "message": "Waiting " + self.remaining_slot.__str__() + " player(s)"}
        player_order_id = self.players[param_player_id]
        if player_order_id != self.current_player:
            return {"status": "error", "message": "Invalid turn"}
        self.current_turn += 1
        self.current_player += 1
        if self.current_player > self.room_size:
            self.current_player = 1
        turn = {
            "status": "ok",
            "current_turn": self.current_turn,
            "current_player": self.current_player,
            "message": message,
            "sender_order_id": player_order_id
        }
        return turn


