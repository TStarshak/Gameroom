import pytest
from backend.models import *
import datetime
import random
import backend.lobby as L1

    
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
        room = Room(id = 1, players = [Player.get_by_id(1), Player.get_by_id(2)])
        assert room.rating == 500
        
    def test_repr(self):
        room = Room(id =2, players = [Player.get_by_id(2)])
        print(room.representation)
        
        
class TestLobby:
    def test_repr(self):
        lobby = Lobby(id = 1, game = "CSGO")
        print(lobby.representation)
        
    def test_join(self):
        room = L1.create_room(lobby_id = 1, player_ids = [1,2])
        L1.join_room(player_id = 3, room_id = room.get('id'))
        assert L1.size(room.get('id')) == 3
    
    def test_append(self):
        room = L1.create_room(lobby_id = 1, player_ids = [1,2])
        room2 = L1.create_room(lobby_id = 1, player_ids = [3,4])
        L1.append_rooms(room1_id = room.get('id'), room2_id = room2.get('id'))
        assert L1.size(room.get('id')) ==4
        