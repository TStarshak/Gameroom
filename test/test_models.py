import pytest
from backend.models import *
import datetime
import random
from backend.lobby import *

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
    
class TestPlayer:
    def populate():
        player_ids = [1, 2, 3, 4, 5]
        for player_id in player_ids:
            Player(player_id, random.randint(RATING_MIN, RATING_MAX),
                   username='Randomplayer{}'.format(player_id),
                   password="rando{}".format(player_id))	 
        

    def test_Rating(self):
        player = Player.get_by_id(1)
        assert player.rating == 500
    
    def test_password(self):
        player = Player.get_by_id(1)
        assert player.password == "Rand1"
        assert player.verify_password("Rand1") == True
    
    def test_repr(self):
        player = Player.get_by_id(1)
        print(player.representation)
    
class TestRoom:
    def populate():
        player_ids = [1, 2, 3, 4, 5]
        for player_id in player_ids:
            Player(player_id, random.randint(RATING_MIN, RATING_MAX),
                   username='Randomplayer{}'.format(player_id),
                   password="rando{}".format(player_id))

    def test_append(self):
        room = Room(id = 1, players = [Player.get_by_id(1)])
        assert room.rating == 500
        
    def test_repr(self):
        room = Room(id =2, players = [Player.get_by_id(2)])
        print(room.representation)
        
class TestLobby:
    def test_repr(self):
        lobby = Lobby(id = 1, game = "CSGO")
        print(lobby.representation)
        
        
        
        