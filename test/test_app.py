import os
import tempfile

import pytest
import json

from backend.app import app
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


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


def test_filled_db(client):
    """Start with a blank database."""
    populate()
    response = client.get(
        '/api/player/1',
        data=json.dumps({'id': 1, 'rating': 500, 'username': 'Randomplayer1'}),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert RATING_MIN <= data['rating']['toxic'] <= RATING_MAX
    assert RATING_MIN <= data['rating']['skill'] <= RATING_MAX
    assert data['id'] == 1
    assert data['username'] == 'Randomplayer1'
