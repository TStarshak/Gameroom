from flask import Flask, request, jsonify
import json
from .models import *
import random
import datetime
from backend import app, models, socketio, logger
import flask_socketio as fsio
from flask_socketio import ConnectionRefusedError, leave_room, join_room, close_room, rooms, disconnect
from .lobby import *
import backend.lobby as lobby
from flask_login import current_user, login_user, logout_user, login_required
import functools
from pprint import pformat
from flask_login.config import EXEMPT_METHODS

def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            logger.debug("User have been disconnected due to not matching auth")
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped

# @app.before_request
# def make_session_permanent():
#     '''
#     [Experimental]
#     Disable in case giving unwanted behavior!!!
#     '''
#     session.permanent = True 

@app.route("/api/player/create", methods=["POST"])
def create_player():
    """
    Expected input: {username, password, email}
    """
    # if request.get_json() is None:
    #     player_id = random.randint(1, 100)
    #     player = Player(player_id, random.randint(RATING_MIN, RATING_MAX),
    #                     username='Randomplayer{}'.format(player_id), password="rando{}".format(player_id))
    #     """
    #     # Read data from given json
    #     {
    #         "username" : ""
    #         "password" : ""
    #         "email" : ""
    #     }
    #     -> data
    #     Player.create(**data)
    #     """
    #     return _serialize(player)
    data = request.get_json()
    player, status = models.Player.create(username=data.get("username"), 
                                          password=data.get("password"), 
                                          email=data.get("email"))
    if player is None:
        return json.dumps({"error": status}), 500
    return jsonify(player.representation)


@app.route("/api/player/list", methods=["GET"])
def list_players():
    return jsonify(list(map(lambda player: player.representation, models.Player.query.all())))

@app.route("/api/lobby/list", methods=["GET"])
def list_lobbies():
    return jsonify(list(map(lambda lobby: lobby.representation, models.Lobby.query.all())))

@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    logger.debug(data)
    player = models.Player.query.filter_by(username=username).first()
    # print(player.representation)
    if not player or not player.verify_password(password):
        return jsonify(status="Failed credentials")
    login_user(player)
    logger.debug('Player found on login {}'.format(current_user.username))
    return jsonify(player.representation)

@app.route("/api/auth/logout", methods=["GET", "POST"])
def logout():
    # logger.debug('Current user on logout is {}'.format(current_user.username))
    # logger.debug(current_user.username)
    logout_user()
    return jsonify(status="logged out")

@app.route("/api/room/create", methods=["POST"])
def create_room():
    """
    Expected input:
    {
        'players' : [<player-id>]
        'lobby' : lobby_id
    }
    """
    player_ids = request.get_json().get('players')
    lobby_id = request.get_json().get('lobby')
    # print(lobby_id)
    # print(players)
    # room_id = random.randint(1, 100)
    # room = Room(room_id, datetime.datetime.now(),
    #             type_=room_id, players=players)
    # players = [models.Player.get_by_id(player_id) for player_id in player_ids]
    # print(players)
    # room, status = models.Room.create(players=players, lobby_id=lobby_id)
    if not player_ids or not lobby_id:
        return jsonify(status="Missing or invalid argument")
    for player_id in player_ids:
        if is_in_match(player_id):
            return jsonify(status="Player {} is already in a match".format(player_id))
    return jsonify(lobby.create_room(player_ids, lobby_id))
    # if room is None:
    #     return json.dumps({"error": status}), 500
    # return jsonify(room.representation)

@socketio.on('match', '/connection')
@authenticated_only
def match_player(data):
    player_id = current_user.get_id()
    if 'lobby' not in data:
        raise ConnectionRefusedError('Lobby missing or not exist')
    lobby_id = data['lobby']
    # create new single room with player inside
    # players = [models.Player.get_by_id(player_id)]
    # room, status = models.Room.create(players=players, lobby_id=lobby_id)
    # new_room_id = Matchmaker.match(room.id) # Get a potential room
    # new_room = models.Room.get_by_id(new_room_id) #Get room info
    if is_in_match(player_id):
        socketio.emit('match', {'room': current_player_room(player_id, include_room_info=True),
                                'msg': 'Has not left room'}, namespace='/connection')
        return True
    print('ids ' + str(player_id) + ' ' + str(lobby_id))
    room_info = lobby.create_room(player_id, lobby_id)
    print('old')
    print(room_info['players'])
    new_room_info = lobby.Matchmaker.matchmake(room_info['id'])
    print('new')
    print(new_room_info['players'])
    player = models.Player.get_by_id(player_id)
    # fsio.join_room(new_room_info['id'])
    socketio.emit('match', {'room': new_room_info}, namespace='/connection')
    emit_to_player_room(player_id, data=player.representation, event='new join')
    emit_to_player_room(player_id, data={'message': 'Player {} has joined'.format(current_user.username)})
    #Deregister old room? How?
    # Match: create new room -> matching algo -- matched room w our player not inside --> adding ---> remove old room

@app.route("/api/room/list", methods=["GET"])
@login_required
def list_rooms():
    if current_user.is_authenticated:
        offset = request.get_json().get('offset')
        # print(current_user.get_id())
        user = current_user.get_id()
        rooms = [get_room(room, include_player_info=True, include_rating=True) for room in lobby.rooms(offset, player_id=user)]
        logger.debug(pformat(rooms))
        return jsonify(rooms)
    else:
        return False



def _serialize(obj):
    return json.dumps(obj, default=obj_to_dict)


@app.route("/api/room/<int:room_id>", methods=["GET"])
def room_info(room_id):
    return jsonify(get_room(room_id, include_player_info=True))


@app.route("/api/player/<int:player_id>", methods=["GET"])
def player_info(player_id):
    return jsonify(models.Player.get_by_id(player_id).representation)


@app.route("/api/player/<int:player_id>/update-rating", methods=["POST"])
def update_rating(player_id):
    # if request.get_json() is None:
    #     toxic = request.get_json().get('toxic')
    #     skill = request.get_json().get('skill')
    #     player = Player._mem[player_id]
    #     player.rating.updateRating(toxic, skill)
    #     return _serialize(player)
    # else:
    data = request.get_json()
    toxic = data.get('toxic')
    skill = data.get('skill')
    if toxic is None or skill is None:
        return jsonify(status="Missing args")
    models.Player.update_rating(player_id, toxic, skill)
    return jsonify(models.Player.get_by_id(player_id).representation)

@socketio.on('connect', '/connection')
@authenticated_only
def connect_player():
    # player_id = request.args.get('player', type=int)
    # print(player_id)
    # print(request.sid)
    player_id = current_user.get_id()
    sid = request.sid
    if is_online(player_id):
        logger.debug('Player {} already online'.format(player_id))
        raise ConnectionRefusedError('Player is alrady online, attempts to have another session is refused')
    assert models.Player.get_by_id(player_id)
    is_valid = connect_session(player_id, sid)
    socketio.emit('connect_callback', {'status': 'Connected'}, namespace='/connection')

@socketio.on('disconnect', '/connection')
@authenticated_only
def disconnect_player():
    # player_id = request.args.get('player', type=int)
    # assert models.Player.get_by_id(player_id)
    disconnect_session(request.sid)

@socketio.on('message', '/connection')
@authenticated_only
def send_message(data):
    player_id = current_user.get_id()
    if is_in_match(player_id) and 'message' in data:
        message = data.get('message')
        # rooms = fsio.rooms(sid=request.sid)
        # room = rooms[-1]
        emit_to_player_room(player_id, {'message': message, 'sender': player_id, 'username': current_user.username})
    else:
        return False

@app.route('/api/player/online-list', methods=['GET', 'POST'])
def online_players():
    return jsonify([models.Player.get_by_id(player_id).representation for player_id in lobby.online_player_ids()])

# @app.route('/api/room/leave', methods=['GET', 'POST'])
# @login_required
@socketio.on('leave', namespace='/connection')
@authenticated_only
def leave_room():
    logger.debug(current_user.username)
    player_id = int(session_player_id(request.sid))
    if is_in_match(player_id):
        room_id = current_player_room(player_id)
        username = current_user.username
        emit_to_player_room(player_id, {'message': 'Player {} has left'.format(username)})
        lobby.leave_room(player_id)
        # socketio.send('message', 'Player {} has left'.format(player_id), room=room_id)
        if not is_in_match(player_id):
            emit_to_player_room(player_id, {'message': 'Player {} has left'.format(models.Player.get_by_id(player_id).username)})
            return socketio.emit('leave', data={'status':'Success'}, namespace='/connection')
        else:
            return socketio.emit('leave', data={'status':'Failed'}, namespace='/connection')
    else:
        return socketio.emit('leave', data={'status':'In a match'}, namespace='/connection')
        
def emit_to_player_room(player_id, data, event='message'):
    room = current_player_room(player_id, include_room_info=True)
    for player in room['player_ids']:
        socketio.emit(event, data, room=player_session_id(player), namespace='/connection')

