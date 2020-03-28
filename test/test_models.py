import pytest
from backend.mock_models import *
from backend.Rating import Rating
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
        room = Room(id=1, timestamp=datetime.datetime.now(),
                    type_=1, players=[1, 2, 3])
        assert room.id == 1
        assert room.players == [1, 2, 3]
        assert room.cap == PLAYERS_CAP

    def test_append(self):
        """
        Appending test
        """
        room = Room(id=1, timestamp=datetime.datetime.now(),
                    type_=1, players=[1, 2, 3])
        room.append(
            Room(id=2, timestamp=datetime.datetime.now(), type_=2, players=[4]))
        room.append(Room(id=3, timestamp=datetime.datetime.now(),
                         type_=3, players=[4]))  # Must be skipped
        assert room.players == [1, 2, 3, 4]

    def test_size(self):
        """
        Size test
        """
        players = [1, 2, 3]
        room = Room(id=1, timestamp=datetime.datetime.now(),
                    type_=1, players=players)
        assert len(players) == room.size

    def test_size_change(self):
        """
        Size add test
        """
        players = [1, 2, 3]
        additional = [4, 5]
        room = Room(id=1, timestamp=datetime.datetime.now(),
                    type_=1, players=[1, 2, 3], cap=5)
        room.append(Room(id=2, timestamp=datetime.datetime.now(),
                         type_=2, players=additional))
        assert len(players) + len(additional) == room.size
