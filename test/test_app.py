import os
import tempfile

import pytest
import json
from flask_sqlalchemy import SQLAlchemy

from backend import app as _app, db as _db, models, socketio
from backend.models import Room, Player, RATING_MAX, RATING_MIN
from config import TestConfig, TESTDB, TESTDB_PATH
import datetime
import random
import logging
from worker import conn
from redis import ConnectionError

logger = logging.getLogger()

# PLAYERS_TO_GEN = 5

# mock_players = {}

def is_redis_available(conn):
    try:
        conn.ping()
        return True
    except ConnectionError:
        return False

# pytestmark = pytest.mark.skipif(not is_redis_available(conn), reason="redis instance is not available")

def test_player_json(client):
    """Test with single player."""
    response = client.get(
        '/api/player/1'
    )
    print(response.get_data(as_text=True))
    assert response.status_code == 200
    player = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert RATING_MIN <= player['rating']
    assert player['id'] == 1
    assert player['username'] == 'Randomplayer1'


def test_login(client):
    
    response = client.post(
        '/api/auth/login',
         data=json.dumps({'username': 'Randomplayer1', 'password': 'Rand1'}),
        content_type='application/json'
    )

    data = json.loads(response.get_data(as_text=True))
    print(data)
    assert response.status_code == 200

@pytest.mark.skipif(not is_redis_available(conn), reason="redis instance is not available")
def test_room_create(client):
    """Create a new room with single participant"""
    response = client.post(
        '/api/room/create',
        data=json.dumps({'players': [2],
                         'lobby' : 1}),
        content_type='application/json'
    )
    print(response.get_data(as_text=True))
    room = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert RATING_MIN <= room['rating'] <= RATING_MAX
    assert [player['id'] for player in room['players']] == [2]

@pytest.mark.skipif(not is_redis_available(conn), reason="redis instance is not available")
def test_room_existed(client):
    """Create a new room with single participant already in a match"""
    response = client.post(
        '/api/room/create',
        data=json.dumps({'players': [2],
                         'lobby' : 1}),
        content_type='application/json'
    )
    response = client.post(
        '/api/room/create',
        data=json.dumps({'players': [2],
                         'lobby' : 1}),
        content_type='application/json'
    )
    status = json.loads(response.get_data(as_text=True))
    print(status)

    assert status['status'] == 'Player 2 is already in a match'

@pytest.mark.skipif(not is_redis_available(conn), reason="redis instance is not available")
def test_room_json(client):
    """Test with a blank database."""
    response = client.get(
        '/api/room/1',
    )
    print(response.get_data(as_text=True))
    room = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert RATING_MIN <= room['rating'] <= RATING_MAX
    assert room['id'] == 1
    assert [player['id'] for player in room['players']] == [2]

def test_players_list(client):
    """List all current player"""
    response = client.get(
        '/api/player/list',
    )

    data = json.loads(response.get_data(as_text=True))
    print(data)
    assert response.status_code == 200
    assert [player['id'] for player in data] == [1, 2, 3, 4, 5]
    for player in data:
        assert RATING_MIN <= player['rating'] <= RATING_MAX
    


def test_rating_update(client):
    """Match a current player to one room"""
    response = client.post(
        '/api/player/1/update-rating',
        data=json.dumps({'toxic': 1, 'skill': 1}),
        content_type='application/json'
    )

    player = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert player['id'] == 1
    assert RATING_MIN <= player['rating'] <= RATING_MAX
    assert player['num_evals'] == 2

def test_player_create(client):
    response = client.post(
        '/api/player/create',
         data=json.dumps({'username': 'Randomplayer9', 'password': 'Rand9', 'email': 'Rando9@somewhere.somehow'}),
        content_type='application/json'
    )
    print(response.get_data(as_text=True))
    assert response.status_code == 200
    player = json.loads(response.get_data(as_text=True))
    assert player['username'] == 'Randomplayer9'
    assert player['email'] == 'Rando9@somewhere.somehow'
    
def test_player_create_int(client):
    response = client.post(
        '/api/player/create',
         data=json.dumps({'username': 22, 'password': 22, 'email': 22}),
        content_type='application/json'
    )
    print(response.get_data(as_text=True))
    assert response.status_code == 200
    player = json.loads(response.get_data(as_text=True))
    assert player['username'] == '22'
    assert player['email'] == '22'
