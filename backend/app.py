from flask import Flask, request, jsonify
import json
from .mock_models import *
import random
import datetime
app = Flask(__name__)


@app.route("/api/player/create", methods=["POST"])
def create_player():
        player_id = random.randint(1, 100)
        player = Player(player_id, random.randint(RATING_MIN, RATING_MAX), 
                username='Randomplayer{}'.format(player_id), password="rando{}".format(player_id))
        return json.dumps(player, default=obj_to_dict)

@app.route("/api/player/list", methods=["GET"])
def list_players():
        return json.dumps(list(Player._mem.values()), default=obj_to_dict)

@app.route("/api/room/create", methods=["POST"])
def create_room():
        players = request.get_json().get('players')
        print(players)
        room_id = random.randint(1, 100)
        room = Room(room_id, datetime.datetime.now(), type_=room_id, players=players)
        return json.dumps(room, default=obj_to_dict)

@app.route("/api/room/<room_id>", method=["GET"])
def room_info(room_id):
        return json.dumps(Room._mem[room_id])

@app.route("/api/player/<player_id>", method=["GET"])
def room_info(player_id):
        return json.dumps(Player._mem[player_id])
