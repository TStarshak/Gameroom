import pytest
from backend.mock_models import *
import datetime

class TestRoom:

    def populate():
        player_ids = [1, 2, 3, 4, 5]
        for player_id in player_ids:
            Player(player_id, random.randint(RATING_MIN, RATING_MAX),
                username='Randomplayer{}'.format(player_id),
                password="rando{}".format(player_id))

    def test_creation(self):
        """
        Creation test
        """
        room = Room(id=1, timestamp=datetime.datetime.now(), type_=1, players=[1, 2, 3])
        assert room.id == 1
        assert room.players == [1, 2, 3]
        assert room.cap == PLAYERS_CAP

    def test_append(self):
        """
        Appending test
        """
        room = Room(id=1, timestamp=datetime.datetime.now(), type_=1, players=[1, 2, 3])
        room.append(Room(id=2, timestamp=datetime.datetime.now(), type_=2, players=[4]))
        room.append(Room(id=3, timestamp=datetime.datetime.now(), type_=3, players=[4])) # Must be skipped
        assert room.players == [1, 2, 3, 4]


    def test_add(self):
        """
        Adding test
        """
        room = Room(id=1, timestamp=datetime.datetime.now(), type_=1, players=[1, 2, 3])
        room += Player._mem[4]
        print(room)
        assert room.players == [1, 2, 3, 4]