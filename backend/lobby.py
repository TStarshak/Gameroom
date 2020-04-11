from backend import app, models, conn, logger
from backend.matchmaker import Matchmaker
from typing import Iterator
from logging import DEBUG

'''
Module to implement joining and leaving logic
'''


# Trying in memory first
online_players = set() # set of player ids
online_rooms = dict() # dictionaries that map from room to List[player_ids]

def join_room(player_id: int, room_id: int):
    conn.hset('inmatch', player_id, room_id)
    conn.sadd('room:{}'.format(room_id), player_id)
    logger.info(DEBUG, 'Room id {} now with players {}'.format(room_id, conn.smembers(room_id)))

def rooms(include_players=True) -> Iterator:
    '''
    Get all online rooms
    '''
    for room in conn.scan_iter(match='room:*'):
        players = conn.smembers(room)
        if include_players:
            yield room, players
        else:
            yield room

def leave_room(player_id: int):
    room_id = conn.hget('inmatch', player_id)
    if room_id is None:
        return
    conn.hdel('inmatch', player_id)
    conn.srem('room:{}'.format(room_id), player_id)
    logger.info(DEBUG, 'Room id {} now with players {}'.format(room_id, conn.smembers(room_id)))

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
    logger.log(DEBUG, 'Player {} now offline'.format(player_id))