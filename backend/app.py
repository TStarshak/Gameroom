from flask import Flask, request, jsonify
import json
from .mock_models import *
import random
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

