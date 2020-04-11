import pytest
from backend import app as _app, db as _db, socketio, models
import tempfile
import json
import os
from config import TESTDB, TESTDB_PATH, TestConfig
from worker import conn
from redis import ConnectionError


"""
Must have redis instance running before this test is invoked
"""
def is_redis_available(conn):
    try:
        conn.ping()
        return True
    except ConnectionError:
        return False

pytestmark = pytest.mark.skipif(not is_redis_available(conn), reason="redis instance is not available")


PLAYERS_TO_GEN = 5
mock_players = {}

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
        os.unlink(TESTDB_PATH)
    _db.init_app(app)
    _db.create_all()
    configure(app, _db, request)
    print(_db.engine.table_names())
    request.addfinalizer(teardown)
    return _db

def configure(app, db, request):
    with app.test_client() as client:
        global mock_players
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
        mock_players = {i + 1 : player.representation for i, player in enumerate(models.Player.query.all())}
        models.Lobby.create(game='DOTA 2', 
                            short_description='Some MMORPG game', 
                            cap=8)

@pytest.fixture
def client(db, app, request):
    # db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    # app.config['TESTING'] = True
    # with app.socket_client() as client:
    #     yield client
    print(models.Player.query.all())
    with app.test_client() as client:
        return client

# @pytest.fixture
# def mock_players(db, app, request):
#     # db_fd, app.config['DATABASE'] = tempfile.mkstemp()
#     # app.config['TESTING'] = True
#     # with app.socket_client() as client:
#     #     yield client
#     return mock_players

def test_connection(app, client):
    namespace = '/api/sockets/connection'
    socket_client = socketio.test_client(app, flask_test_client=client)
    socket_client_attack = socketio.test_client(app, flask_test_client=client)
    socket_client.connect(namespace=namespace, query_string='player=1')
    socket_client_attack.connect(namespace=namespace, query_string='player=1')
    assert socket_client.is_connected(namespace)
    # assert not socket_client_attack.is_connected(namespace)
    print(socket_client_attack.get_received(namespace))
    received = socket_client.get_received(namespace)
    assert len(received) == 1
    assert received[0]['args'][0]['status'] == 'Connected'
    socket_client.disconnect(namespace=namespace)
    socket_client_attack.disconnect(namespace=namespace)
    assert not socket_client.is_connected(namespace)



