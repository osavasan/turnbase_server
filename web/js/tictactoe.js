var playerInfo = null;
var player_id = null;
var room_id = null;
var game_id = "tictactoe";
var consumed_index = [];
/*
    the URL of the WAMP Router (Crossbar.io)
*/
var wsuri;
if (document.location.origin == "file://") {
    wsuri = "ws://127.0.0.1:8080/ws";
} else {
    wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" + document.location.host + "/ws";
}

/*
    the WAMP connection to the Router
*/
var connection = new autobahn.Connection({
    url: wsuri,
    realm: "realm1"
});

/*
    fired when connection is established and session attached
*/
connection.onopen = function(session, details) {
    console.log("Connected");
    put_player_info("Connected");

    // join a match
    put_player_info("Joining to match...");
    session.call("com.developerbob.join_match",[],{game_id:"tictactoe",room_type:"standard",match_criteria:"none"}).then(
        function (result) {
            put_player_info("Joined");
            console.log("player info", result);
            playerInfo = result;
            player_id = playerInfo.player_id
            room_id = playerInfo.room_id
            player_order_id = playerInfo.player_order_id
            if (playerInfo.player_order_id==1) {
                playerInfo.player = "X";
            } else {
                playerInfo.player = "O";
            }
            put_player_info("You playing: " + playerInfo.player);
            $('#player_id').innerHTML = "ID" + playerInfo.player_id;
            put_log("Room ID:" + playerInfo.room_id);
            put_log("Player ID:" + playerInfo.player_id);
            put_log("Player Order ID:" + playerInfo.player_order_id);
            // subscribe to a topic to receive turns info
            session.subscribe("com.developerbob.turn_made." + playerInfo.room_id, on_turn).then(
                function (sub) {
                    put_log("subscribed 'com.developerbob.turn_made."+ playerInfo.room_id  +"'");
                    console.log("subscribed 'com.developerbob.turn_made."+ playerInfo.room_id  +"'");
                },
                function (err) {
                    console.log("failed to subscribe to 'com.developerbob.turn_made."+ playerInfo.room_id +"'", err);
                }
            );

        },
        function (err) {
            console.log("error", err);
            put_player_info("Can not join a match:" + JSON.stringify(err) + ". Reload the page to try again.");
        }
    );

 };

/*
    fired when connection was lost (or could not be established)
*/
connection.onclose = function(reason, details) {
    console.log("Connection lost: " + reason);
    put_player_info("Connection lost: " + reason);
    playerInfo = null;
}

/*
    now actually open the connection
*/
connection.open();

/*
    show message to player
*/
function put_player_info(text) {
    $("#player")[0].innerHTML = text;
    $("#log").append("<br>" + text );
}

function put_log(text) {
    $('#log').append("<br>"+text);
}

/*
    Turn handler
*/
function on_turn(args) {
    kwargs = args[0]
    var current_turn = kwargs["current_turn"]
    var player_order_id = kwargs["sender_order_id"];
    var index = kwargs["message"];
    var player = (player_order_id==1)? "X":"O";

    console.log("on_turn", "player", player, "index", index);

    // apply turn
    $("#board td[data-index=" + index + "]")[0].innerHTML = player;
    consumed_index.push(index);

    if (is_finished) {
        // close the connection anyway
        connection.close();

        // check win and show result
        var message = "DRAW!"
        if (is_win) {
            message = "You LOOSE!";
            if (playerInfo.player == player) {
                message = "You WIN!";
            }
        }
        put_player_info(message + " Reload the page to join again.");
    }
}

 $(document).ready(function() {

    put_player_info("Connecting to " + wsuri + "...");

    // cell click handler
    $("#board td").click(function(e) {

       // you can not do turn until connected
       if (playerInfo == null) {
          put_player_info("not joined yet");
          return;
       }

       // get cell index
       var index = $(this)[0].dataset.index;
       index = +index;
       if (consumed_index.indexOf(index)!==-1) {
            console.log("Cell is used!");
            return;
       }

       // make turn sending player info and turn info
       connection.session.call("com.developerbob.make_turn", [room_id,player_id, index, playerInfo.player]).then(
          function (result) {
            var status = result["status"];
            var message = result["message"];
            console.log("turn made", "Status=", status, " , Message =", message);
            if (status=="error") {
                put_player_info(message)
            }
          },
          function (err) {
             console.log("error", err);
          }
       );

    });
    
 });