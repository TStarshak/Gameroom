import pytest
from backend import app as _app, db as _db, socketio, models
import tempfile
import json
import os
from config import TESTDB, TESTDB_PATH, TestConfig
from worker import conn
from redis import ConnectionError
import random
from pprint import pprint
from collections import namedtuple
# from .conftest import mock_players, PLAYERS_TO_GEN, is_redis_available


PLAYERS_TO_GEN = 5
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

@pytest.fixture
def player_clients(app, mock_players):
    namespace = '/connection'
    clients = {}
    socket_clients = {}
    for player in mock_players.values():
        clients[player.id] = app.test_client()
        client = clients[player.id]
        socket_clients[player.id] = socketio.test_client(app, flask_test_client=client)
        login_response = login(player, client)
        socket_clients[player.id].connect(namespace=namespace) # query_string='player={}'.format(player.id))
        response = client.post(
            '/api/room/create',
            data=json.dumps({'players': [player.id],
                            'lobby' : 1}),
            content_type='application/json'
        )
    ClientTuple = namedtuple('ClientTuple', ['socket_clients', 'clients', 'mock_players'])
    yield ClientTuple(socket_clients, clients, mock_players)
    for socket_client, client in zip(socket_clients.values(), clients.values()):
        if socket_client.is_connected(namespace=namespace):
            socket_client.disconnect(namespace=namespace)
        logout(client)
        assert not socket_client.is_connected(namespace)

def login(player, app_client):
    return app_client.post(
            '/api/auth/login',
            data=json.dumps({'username': player.username,
                             'password': player.password}),
            content_type='application/json'
        )

def logout(app_client):
    return app_client.get(
        '/api/auth/logout'
    )

def test_connection(app, client, mock_players):
    namespace = '/connection'
    response = login(mock_players[1], client)
    print(response.get_data(as_text=True))
    socket_client = socketio.test_client(app, flask_test_client=client)
    socket_client_attack = socketio.test_client(app, flask_test_client=app.test_client())
    socket_client.connect(namespace=namespace) # query_string='player=1')
    received = socket_client.get_received(namespace)
    socket_client_attack.connect(namespace=namespace) # query_string='player=1')
    # assert not socket_client_attack.is_connected(namespace)
    print("Connection status returns")
    print(received)
    socket_client.disconnect(namespace=namespace)
    assert len(received) == 1
    assert received[0]['args'][0]['status'] == 'Connected'
    assert not socket_client.is_connected(namespace)
    

def test_players_match(app, player_clients):
    namespace = '/connection'
    clients = player_clients.clients
    socket_clients = player_clients.socket_clients
    player, _ = models.Player.create(username='Randomplayer{}'.format(PLAYERS_TO_GEN+1), 
                                 email='Rando{}@somewhere.somehow'.format(PLAYERS_TO_GEN+1), 
                                 password='Rand{}'.format(PLAYERS_TO_GEN+1))
    client = app.test_client()
    clients[player.id] = client
    response = login(player, client)
    socket_clients[player.id] = socketio.test_client(app, flask_test_client=client)
    player_client = socket_clients[player.id]
    player_client.connect(namespace=namespace) # query_string='player={}'.format(player.id))
    player_client.emit('match', {'player' : player.id, 'lobby': 1}, namespace=namespace)
    received = player_client.get_received(namespace)
    # assert len(received) == 2
    pprint(received)
    assert len(received[1]['args'][0]['room']['players']) > 1

def test_room_list(app, player_clients):
    namespace = '/connection'
    clients = player_clients.clients
    socket_clients = player_clients.socket_clients
    mock_players = player_clients.mock_players
    player = random.choice(list(mock_players.values()))
    client = clients[player.id]
    player_client = socket_clients[player.id]
    response = client.get(
        '/api/room/list',
        data=json.dumps({
            'offset': 0.2
        }),
        content_type='application/json'
    )

    data = json.loads(response.get_data(as_text=True))
    assert 0 <= len(data) # <= len(mock_players)
    pprint('Returned data on list rooms')
    pprint(data)

def test_messaging(app, player_clients):
    namespace = '/connection'
    clients = player_clients.clients
    socket_clients = player_clients.socket_clients
    player, _ = models.Player.create(username='Randomplayer{}'.format(PLAYERS_TO_GEN+2), 
                                 email='Rando{}@somewhere.somehow'.format(PLAYERS_TO_GEN+2), 
                                 password='Rand{}'.format(PLAYERS_TO_GEN+2))
    client = app.test_client()
    clients[player.id] = client
    response = login(player, client)
    socket_clients[player.id] = socketio.test_client(app, flask_test_client=client)
    player_client = socket_clients[player.id]
    player_client.connect(namespace=namespace) # query_string='player={}'.format(player.id))
    player_client.emit('match', {'player' : player.id, 'lobby': 1}, namespace=namespace)
    received = player_client.get_received(namespace)
    players = received[1]['args'][0]['room']['players']
    other_player = None
    while True:
        other_player = random.choice(players)
        if other_player['id'] != player.id:
            break
    other_player_client = socket_clients[other_player['id']]
    # Start sending message
    player_client.emit('message', {'message': 'Hello'}, namespace=namespace)
    received = other_player_client.get_received(namespace)
    assert received[-1]['args']['message'] == 'Hello'
    assert int(received[-1]['args']['sender']) == player.id

@pytest.mark.skip(reason='Endpoint is deprecated')
def test_leaving(app, player_clients):
    namespace = '/connection'
    clients = player_clients.clients
    socket_clients = player_clients.socket_clients
    mock_players = player_clients.mock_players
    player = random.choice(list(mock_players.values()))
    client = clients[player.id]
    # status = client.post(
    #     'api/room/leave'
    # )
    socket_client = socket_clients[player.id]
    socket_client.emit('leave', namespace=namespace)
    received = socket_client.get_received()
    pprint(received)
    response = client.get(
        '/api/room/list',
        data=json.dumps({
            'offset': 1.0
        }),
        content_type='application/json'
    )
    # status = json.loads(status.get_data(as_text=True))
    # assert status['status'] == 'Success'
    rooms = json.loads(response.get_data(as_text=True))
    for room in rooms:
        assert player.id not in [player['id'] for player in room['players']]
    
def test_online_players(app, client, player_clients):
    namespace = '/connection'
    clients = player_clients.clients
    socket_clients = player_clients.socket_clients
    mock_players = player_clients.mock_players
    player, _ = models.Player.create(username='Randomplayer{}'.format(PLAYERS_TO_GEN+3), 
                                 email='Rando{}@somewhere.somehow'.format(PLAYERS_TO_GEN+3), 
                                 password='Rand{}'.format(PLAYERS_TO_GEN+3))
    client = app.test_client()
    clients[player.id] = client
    login(player, client)
    socket_clients[player.id] = socketio.test_client(app, flask_test_client=client)
    player_client = socket_clients[player.id]
    player_client.connect(namespace=namespace) # query_string='player={}'.format(player.id))
    response = client.get(
        '/api/player/online-list'
    )
    players = json.loads(response.get_data(as_text=True))
    assert player.id in [player['id'] for player in players]
    #Disconnect player from online
    player_client.disconnect(namespace=namespace)
    response = client.get(
        '/api/player/online-list'
    )
    players = json.loads(response.get_data(as_text=True))
    assert player.id not in [player['id'] for player in players]

    

    



