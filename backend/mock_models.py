from typing import List

RATING_MAX = 1000
RATING_MIN = 0
RATING_DEFAULT = (RATING_MAX + RATING_MIN)/2
PLAYERS_CAP = 4
'''
These are mock classes for proof of concept before any database setup is involved
'''

class Player:

    def __init__(self, id: int, rating, username, password):
        self.id = id
        self.rating = rating
        self.username = username
        self.password = password

    def __repr__(self):
        return str(self.__dict__)

class Room:
    def __init__(self, id, timestamp, type_, rating, players: List[int]=[], cap=PLAYERS_CAP):
        self.id = id
        self.timestamp = timestamp
        self.type_ = type_
        self.cap = cap
        self.players = players
        self.rating = rating

    @property
    def size(self):
        return len(self.players)

    def __iadd__(self, other):
        assert other.__class__ == Player.__class__
        rating = (self.rating * self.size + other.rating)/(self.size + 1)
        self.players.append(other)

    def __repr__(self):
        return str(self.__dict__)

class Lobby:

    def __init__(self, id: int, game: str, rooms: List[Room]=[]):
        self.id = id
        self.game = game
        self.rooms = rooms

    def append(self, room: Room):
        self.rooms.append(room)

    def __hash__(self):
        return hash(self.id)

    def add_room(self, room: Room):
        self.rooms.append(room)
    