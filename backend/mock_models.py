from typing import List
from datetime import date, datetime
from statistics import mean
from Rating import *

RATING_MAX = 1000
RATING_MIN = 0
RATING_DEFAULT = (RATING_MAX + RATING_MIN)/2
PLAYERS_CAP = 4
'''
These are mock classes for proof of concept before any database setup is involved
'''

class Player:
    _mem = {}
    
    def __init__(self, id: int, rating, username, password):
        self.id = id
        self.rating = Rating(rating, rating, 1)
        self.username = username
        self.password = password
        self._mem[id] = self

    def __repr__(self):
        return str(self.__dict__)

class Room:
    _mem = {}
    def __init__(self, id, timestamp, type_, players: List[int]=[], cap=PLAYERS_CAP, rating=None):
        self.id = id
        self.timestamp = timestamp
        self.type_ = type_
        self.cap = cap
        self.players = players
        self.rating = Rating( mean(map(lambda player_id: Player._mem[player_id].rating, players)), mean(map(lambda player_id: Player._mem[player_id].rating, players)), cap)
        self._mem[id] = self
   
    def append(room):
        totalPlayers = room.players + self.players
        appendedRoom = null
        if len(totalPlayers) < self.cap:
            appendedRoom = Room(self.room_id, self.timestamp, type_=self.type, players=totalPlayers)
        return appendedRoom        
        
    @property
    def size(self):
        return len(self.players)

    def __iadd__(self, other):
        assert other.__class__ == Player.__class__
        temp = (self.rating.getRating() * self.size + other.rating.getRating())/(self.size + 1)
        self.rating.updateRating(temp, temp, self.size + 1)                        
        self.players.append(other)

    def __repr__(self):
        return str(self.__dict__)

class Lobby:

    _mem = {}

    def __init__(self, id: int, game: str, rooms: List[Room]=[]):
        self.id = id
        self.game = game
        self.rooms = rooms
        self._mem[id] = self

    def append(self, room: Room):
        self.rooms.append(room)

    def __hash__(self):
        return hash(self.id)

    # def add_room(self, room: Room):
    #     self.rooms.append(room)

def obj_to_dict(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    return obj.__dict__



