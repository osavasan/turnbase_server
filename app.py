from twisted.internet import defer
from twisted.logger import Logger

from autobahn.twisted.wamp import ApplicationSession

import uuid

import GameRoom


class GameSession(ApplicationSession):

    log = Logger()

    rooms = {}

    @defer.inlineCallbacks
    def onJoin(self, details):

        def join_player(*args,**kwargs):
            print("join_player() triggered!")
            game_id = kwargs.get("game_id")
            room_type = kwargs.get("room_type")
            match_criteria = kwargs.get("match_criteria")
            print("game_id:", game_id, " ,room_type=", room_type, " ,match_criteria:", match_criteria)
            player_id = uuid.uuid4().__str__()
            found = False
            player_info = None
            for room_key in self.rooms:
                if (game_id == self.rooms[room_key].game_key) and (self.rooms[room_key].remaining_slot > 0):
                    player_info = self.rooms[room_key].add_player(player_id)
                    found = True
            if not found:
                room = GameRoom.GameRoom()
                room.game_key = game_id
                room.room_type = room_type
                room.match_criteria = match_criteria
                player_info = room.add_player(player_id)
                self.rooms[room.room_id] = room
                print("New room created : "+ room.room_id)
            return player_info

        yield self.register(join_player, "com.developerbob.join_match")
        self.log.info("procedure join_match() registered")

        @defer.inlineCallbacks
        def make_turn(*args, **kwargs):
            """
            Make a turn and broadcast results

            :param room_id:
            :param args:
            :return:
            """
            room_id =  args[0]
            print("make_turn() triggered!")
            turn_result = self.rooms[room_id].make_turn(args[0], args[1], args[2])
            if turn_result["status"] == "ok":
                yield self.publish("com.developerbob.turn_made." + room_id, turn_result)
                defer.returnValue(turn_result)
            else:
                defer.returnValue(turn_result)

        yield self.register(make_turn, "com.developerbob.make_turn")
        self.log.info("procedure make_turn() registered")
