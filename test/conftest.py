import os
import tempfile

import pytest
import json
from flask_sqlalchemy import SQLAlchemy

from backend import app as _app, db as _db, models, socketio
from backend.mock_models import Room, Player, RATING_MAX, RATING_MIN
from config import TestConfig, TESTDB, TESTDB_PATH
import datetime
import random
import logging
from worker import conn

logger = logging.getLogger()

PLAYERS_TO_GEN = 5

# mock_players = {}
# def populate():
#     player_ids = [1, 2, 3, 4, 5]
#     for player_id in player_ids:
#         Player(player_id, random.randint(RATING_MIN, RATING_MAX),
#                username='Randomplayer{}'.format(player_id),
#                password="rando{}".format(player_id))
#     Room(1, datetime.datetime.now(), type_=1, players=[1, 3, 5])


# @pytest.fixture(scope="session", autouse=True)
# def configure(request):
#     """
#     Allows plugins and conftest files to perform initial configuration.
#     This hook is called for every plugin and initial conftest
#     file after command line options have been parsed.
#     """
#     populate()
    
@pytest.fixture(scope='session')
def app(request):
    _app.config.from_object(TestConfig)
    ctx = _app.app_context()
    ctx.push()
    def teardown():
        ctx.pop()
    request.addfinalizer(teardown)
    return _app

@pytest.fixture(scope='session')
def db(app, request):
    if os.path.exists(TESTDB_PATH):
        os.unlink(TESTDB_PATH)
    def teardown():
        _db.drop_all()
        conn.shutdown(nosave=True)
        os.unlink(TESTDB_PATH)
    _db.init_app(app)
    _db.create_all()
    configure(app, _db, request)
    print(_db.engine.table_names())
    request.addfinalizer(teardown)
    return _db

def configure(app, db, request):
    with app.test_client() as client:
        for i in range(1, PLAYERS_TO_GEN+1):
            models.Player.create(username='Randomplayer{}'.format(i), 
                                 email='Rando{}@somewhere.somehow'.format(i), 
                                 password='Rand{}'.format(i))
            # response = client.post(
            #     '/api/player/create',
            #     data=json.dumps({'username' : 'Randomplayer{}'.format(i),
            #                     'email' : 'Rando{}@somewhere.somehow'.format(i),
            #                     'password': 'Rand{}'.format(i)}),
            #     content_type='application/json'
            # )
        models.Lobby.create(game='DOTA 2', 
                            short_description='Some MMORPG game', 
                            cap=8)

@pytest.fixture
def client(db, app, request):
    # db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    # app.config['TESTING'] = True
    # with app.test_client() as client:
    #     yield client
    # print(models.Player.query.all())
    with app.test_client() as client:
        return client

@pytest.fixture()
def mock_players(db, app, request):
    return {player.id : player for player in models.Player.query.all()}

