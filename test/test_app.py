import os
import tempfile

import pytest
import json

from backend import app
from backend.mock_models import Room, Player, RATING_MAX, RATING_MIN
import datetime
import random


def populate():
    player_ids = [1, 2, 3, 4, 5]
    for player_id in player_ids:
        Player(player_id, random.randint(RATING_MIN, RATING_MAX),
               username='Randomplayer{}'.format(player_id),
               password="rando{}".format(player_id))
    Room(1, datetime.datetime.now(), type_=1, players=[1, 3, 5])


@pytest.fixture(scope="session", autouse=True)
def configure(request):
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest
    file after command line options have been parsed.
    """
    populate()


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_player_json(client):
    """Test with single player."""
    response = client.get(
        '/api/player/1'
    )

    player = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert RATING_MIN <= player['rating']['toxic']
    assert RATING_MIN <= player['rating']['skill']
    assert player['id'] == 1
    assert player['username'] == 'Randomplayer1'


def test_room_json(client):
    """Test with a blank database."""
    response = client.get(
        '/api/room/1',
    )

    room = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert RATING_MIN <= room['rating']
    assert room['id'] == 1
    assert room['players'] == [1, 3, 5]


def test_room_create(client):
    """Create a new room with single participant"""
    response = client.post(
        '/api/room/create',
        data=json.dumps({'players': [2]}),
        content_type='application/json'
    )

    room = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert RATING_MIN <= room['rating']
    assert room['players'] == [2]


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
        assert RATING_MIN <= player['rating']['toxic']
        assert RATING_MIN <= player['rating']['toxic']


def test_players_match(client):
    """Match a current player to one room"""
    response = client.post(
        '/api/server/match',
        data=json.dumps({'player': 4}),
        content_type='application/json'
    )

    room = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert 4 in room['players']
    assert RATING_MIN <= room['rating']


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
    assert RATING_MIN <= player['rating']['toxic']
    assert RATING_MIN <= player['rating']['toxic']
    assert player['rating']['numEvals'] == 2
