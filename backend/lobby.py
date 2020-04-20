from backend import app, models, conn, logger
from backend.models import RATING_MAX, RATING_MIN
##from backend.matchmaker import Matchmaker
from typing import Iterator, Union, List
from logging import DEBUG
from statistics import variance, mean
import time
import json

'''
Module to implement joining and leaving logic
'''

__ID_count = 0

# Trying in memory first
online_players = set() # set of player ids
online_rooms = dict() # dictionaries that map from room to List[player_ids]

class Matchmaker:
    '''
    Class to match make a gameroom based on a request
    '''
    

    @classmethod
    def matchmake(cls, single_room_id, fitness=0.75, offset=0.1):
        # Pseudocode
        # start = time.time()
        # while request.is_alive(): 
        #     for room in rooms(request, offset):
        #         if match_quality(request, room) < fitness:
        #             if time.time - start > 30:
        #                 offset <- offset + offset * 0.5
        #                 fitness <- fitness * 0.75
        #             continue
        #         else:
        #             match(request, room)
        #             break
        start = time.time()
        player_id = get_room(single_room_id)['player_ids'][0]
        while is_online(player_id) and size(single_room_id) == 1:
            for room_id in rooms(offset=offset, single_room_id=single_room_id):
                if cls.match_quality(single_room_id, room_id) < fitness and time.time() - start > 30:
                    offset += offset * 0.5
                    fitness *= 0.75
                else:
                    cls.match(room_id, single_room_id)
                    return get_room(room_id, include_player_info=True)

    # @staticmethod
    # def rooms(request: Request, offset: int):
    #     if request.lobby_id in _games:
    #         for room in _games[request.lobby_id]:
    #             if abs(room.rating.getRating() - request.player.rating.getRating()) <= offset:
    #                 yield room

    @classmethod
    def match_quality(cls, match_room_id: int, room_id: int) -> float:

        def diff_rating(match_room_id, room):
            return abs(rating(match_room_id) - rating(room))/(RATING_MAX - RATING_MIN)  
        def var_rating(match_room_id, room):
            avg = (rating(room) * size(room) + rating(match_room_id))/(size(room) + size(match_room_id))
            players = get_room(room)['player_ids'] + get_room(match_room_id)['player_ids']
            logger.debug(players)
            return variance([models.Player.get_by_id(player).rating for player in players])/((RATING_MAX - avg)*(avg - RATING_MIN))
        return 1.0 - ((2/3)*diff_rating(match_room_id, room_id) + (1/3)*var_rating(match_room_id, room_id))
    
    @classmethod
    def match(cls, room1_id: int, room2_id: int):
        append_rooms(room1_id, room2_id) #Register room online

"""
General redis instance handles

Our main data structurs

inmatch -> hashmap of player_id -> room_id where it tells which map the player is in
online -> set of all online players
room -> hashmap of room_id -> room representation json
    {
        "id" : room id
        "lobby_id": lobby_id
        "player_ids": player_ids
    }
session -> key val pairs that contains session hash to player_id to ensure single connection from socketio
"""

def join_room(player_id: int, room_id: int):
    conn.hset('inmatch', player_id, room_id)
    # conn.sadd('room:{}'.format(room_id), player_id)
    data = json.loads(conn.hget('room', room_id))
    data['player_ids'].append(player_id)
    conn.hset('room', room_id, json.dumps(data))
    logger.info(DEBUG, 'Room id {} now with players {}'.format(room_id, conn.smembers(room_id)))

def is_in_match(player_id: int):
    return conn.hexists('inmatch', player_id)

def size(room):
    return len(get_room(room)['player_ids']) if get_room(room) else 0

def append_rooms(room1_id: int, room2_id: int):
    data1 = json.loads(conn.hget('room',room1_id))
    data2 = json.loads(conn.hget('room',room2_id))
    assert data1['lobby_id'] == data2['lobby_id']
    data1['player_ids'] += data2['player_ids']
    conn.hdel('room', room2_id)
    for player_id in data2['player_ids']:
        conn.hdel('inmatch', player_id)
    conn.hset('room', room1_id, json.dumps(data1))

def rating(room_id: int):
    data = json.loads(conn.hget('room', room_id))
    player_ids = data['player_ids']
    rating = mean([models.Player.get_by_id(player_id).rating for player_id in player_ids])
    return rating

def rooms(offset=None, single_room_id=None, player_id=None) -> Iterator:
    '''
    Get all online rooms in an iterator

    Options: Two optional calls will only be used by the matchmake method
    offset: offset values from given single_room_id and rooms found between 0 and 1 (no diff -> whole range diff)
    single_room_id: id of room to be matched, should contain one single player
    '''
    assert (offset is None and single_room_id is None) or (offset and any([single_room_id, player_id]))
    assert offset is None or 0 <= offset <= 1
    rate = None
    if single_room_id is not None:
        rate = rating(single_room_id)
    elif player_id is not None and is_online(player_id):
        rate = models.Player.get_by_id(player_id).rating
    offset = offset or float('inf')
    for room in conn.hkeys('room'):
        if rate and abs(rate - rating(room)) > offset*(RATING_MAX - RATING_MIN):
            continue
        yield room

def new_ID():
    global __ID_count
    __ID_count += 1
    return __ID_count

def create_room(player_ids: Union[int, List] , lobby_id: int):
    """
    Create and save room
    Returns: dict of new room created
    """
    if not isinstance(player_ids, list):
        player_ids = [int(player_id) for player_id in player_ids]
    room_id = new_ID()
    data = {
        'id' : room_id,
        'lobby_id' : lobby_id,
        'player_ids' : player_ids
    }
    for player_id in player_ids:
        conn.hset('inmatch', player_id, room_id)
    conn.hset('room', room_id, json.dumps(data))
    return get_room(room_id, include_player_info=True)

def get_room(room_id, include_player_info=False, include_rating=True):
    """
    Get dict of room

    Inputs:
    room_id: id of room

    Optionals:
    include_player_info: include json representation of player, and remove player_ids
    include_rating: include room rating
    """
    room_info = json.loads(conn.hget('room',room_id))
    players = [models.Player.get_by_id(player_id) for player_id in room_info['player_ids']]
    if include_player_info:
        room_info['players'] = [player.representation for player in players]
        del room_info['player_ids']
    if include_rating:
        room_info['rating'] = rating(room_id)
    return room_info

def leave_room(player_id: int):
    room_id = conn.hget('inmatch', player_id)
    if room_id is None:
        return
    conn.hdel('inmatch', player_id)
    # conn.srem('room:{}'.format(room_id), player_id)
    logger.debug("{}, {}".format(player_id, conn.hget('room',room_id)))
    data = json.loads(conn.hget('room',room_id))
    if player_id in data['player_ids']:
        data['player_ids'].remove(player_id)
    if len(data['player_ids']) == 0:
        conn.hdel('room', room_id)
    else:
        conn.hset('room', room_id, json.dumps(data))
    logger.log(DEBUG, 'Room id {} now with players {}'.format(room_id, data['player_ids']))

def save_room(room_id: int):
    """
    [In Development]
    Save a room to the database
    This will be integral to the logic of rating post-match
    """
    data = json.loads(conn.hget('room',room_id))
    player_ids = data['player_ids']
    lobby_id = data['lobby_id']
    players = [models.Player.get_by_id(player_id) for player_id in player_ids]
    room, status = models.Room.create(players=players, lobby_id=lobby_id)

def connect_session(player_id: int, sid: int):
    """
    Connect player to online session

    Inputs:

    player_id:
    sid: session id of socket connection
    """

    sid_key = 'session:{}'.format(sid)
    if conn.exists(sid_key) or conn.sismember('online', player_id):
        return False
    else:
        conn.set(sid_key, player_id)
        conn.sadd('online', player_id)
    if is_online(player_id):
        logger.log(DEBUG, 'Player {} now online'.format(player_id))
        return True
    else:
        logger.log(DEBUG, 'Error happenned when connecting Player {}'.format(player_id))
    return False

def is_online(player_id):
    return conn.sismember('online', player_id)

def disconnect_session(sid: int):
    """
    Disconnect player to online session. 
    All information regarding player will be deregistered from rooms and all data structures proposed

    Inputs:

    player_id:
    sid: session id of socket connection
    """
    player_id = conn.get('session:{}'.format(sid))
    if player_id is None:
        return
    else:
        player_id = int(player_id)
    leave_room(player_id)
    conn.srem('online', player_id)
    conn.delete('session:{}'.format(sid))
    logger.info('Player {} now offline'.format(player_id))