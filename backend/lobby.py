from backend import app, models, conn, logger
from backend.models import RATING_MAX, RATING_MIN
from backend.matchmaker import Matchmaker
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
        while is_online(player_id):
            for room_id in rooms(include_players=False, offset=offset, single_room_id=single_room_id):
                if cls.match_quality(single_room_id, room_id) < fitness and time.time() - start > 30:
                    offset += offset * 0.5
                    fitness *= 0.75
                    continue
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
            players = [get_room(room)['player_ids']] + [get_room(match_room_id)['player_ids']]
            return variance([models.Player.get_by_id(player).rating for player in players])/((RATING_MAX - avg)*(avg - RATING_MIN))
        return 1.0 - ((2/3)*diff_rating(match_room_id, room_id) + (1/3)*var_rating(match_room_id, room_id))
    
    @classmethod
    def match(cls, room1_id: int, room2_id: int):
        append_rooms(room1_id, room2_id) #Register room online


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
    return len(get_room(room)['player_ids'])

def append_rooms(room1_id: int, room2_id: int):
    data1 = json.loads(conn.hget('room',room1_id))
    data2 = json.loads(conn.hget('room',room2_id))
    assert data1['lobby_id'] == data2['lobby_id']
    data1['player_ids'] += data2['player_ids']
    conn.hdel('room', room2_id)
    conn.hset('room', room1_id, json.dumps(data1))

def rating(room_id: int):
    data = json.loads(conn.hget('room', room_id))
    player_ids = data['player_ids']
    rating = mean([models.Player.get_by_id(player_id).rating for player_id in player_ids])
    return rating

def rooms(include_players=True, offset=None, single_room_id=None) -> Iterator:
    '''
    Get all online rooms
    '''
    assert (offset is None and single_room_id is None) or all([offset, single_room_id])
    assert offset is None or 0 <= offset <= 1
    offset = offset or float('inf')
    for room in conn.hkeys('room'):
        if single_room_id is not None:
            if abs(rating(single_room_id) - rating(room)) > offset*(RATING_MAX - RATING_MIN):
                continue
        players = conn.smembers(room)
        if include_players:
            yield room, players
        else:
            yield room

def new_ID():
    global __ID_count
    __ID_count += 1
    return __ID_count

def create_room(player_ids: Union[int, List] , lobby_id: int):
    if isinstance(player_ids, int):
        player_ids = [player_ids]
    room_id = new_ID()
    data = {
        'id' : room_id,
        'lobby_id' : lobby_id,
        'player_ids' : player_ids
    }
    conn.hset('room', room_id, json.dumps(data))
    return get_room(room_id, include_player_info=True)

def get_room(room_id, include_player_info=False, include_rating=True):
    room_info = json.loads(conn.hget('room',room_id))
    players = [models.Player.get_by_id(player_id) for player_id in room_info['player_ids']]
    if include_player_info:
        room_info['players'] = [player.representation for player in players]
        del room_info['player_ids']
    if include_rating:
        room_info['rating'] = mean([player.rating for player in players])
    return room_info

def leave_room(player_id: int):
    room_id = conn.hget('inmatch', player_id)
    if room_id is None:
        return
    conn.hdel('inmatch', player_id)
    # conn.srem('room:{}'.format(room_id), player_id)
    data = json.loads(conn.hget('room',room_id))
    if player_id in data['player_id']:
        data['player_ids'].remove(player_id)
    if len(data['player_ids']) == 0:
        conn.hdel('room', room_id)
    else:
        conn.hset('room', room_id, json.dumps(data))
    logger.info(DEBUG, 'Room id {} now with players {}'.format(room_id, data['player_ids']))

def save_room(room_id: int):
    data = json.loads(conn.hget('room',room_id))
    player_ids = data['player_ids']
    lobby_id = data['lobby_id']
    players = [models.Player.get_by_id(player_id) for player_id in player_ids]
    room, status = models.Room.create(players=players, lobby_id=lobby_id)

def connect(player_id: int, sid: int):
    sid_key = 'session:{}'.format(sid)
    if conn.exists(sid_key) or conn.sismember('online', player_id):
        return False
    else:
        conn.set(sid_key, player_id)
        conn.sadd('online', player_id)
    is_online = conn.sismember('online', player_id)
    if is_online:
        logger.log(DEBUG, 'Player {} now online'.format(player_id))
        return True
    else:
        logger.log(DEBUG, 'Error happenned when connecting Player {}'.format(player_id))
    return False

def is_online(player_id):
    return conn.sismember('online', player_id)

def disconnect(sid: int):
    player_id = conn.get('session:{}'.format(sid))
    if player_id is None:
        return
    else:
        player_id = int(player_id)
    leave_room(player_id)
    conn.srem('online', player_id)
    conn.delete('session:{}'.format(sid))
    logger.info('Player {} now offline'.format(player_id))