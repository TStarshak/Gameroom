import time
from collections import deque
from .mock_models import *
from statistics import variance

class Request:
    def __init__(self, player: Player, lobby_id):
        self.player = player
        self.lobby_id = lobby_id
        self.time = time.time()

    @property
    def is_alive(self):
        return time.time() - self.time < 30
    
    
    
class Matchmaker:
    '''
    Class to match make a gameroom based on a request
    '''

    _games = {1: Lobby(1, "CSGO")}
    _player_queue = deque(maxlen=2000)

    @staticmethod
    def matchmake(request: Request, fitness=0.75, offset=0.1):
        # Pseudocode
        # start = time.time()
        # while request.is_alive(): 
        #     for room in rooms(request, offset):
        #         if match_quality(request, room) < fitness:
        #             if time.time - start > 30:
        #                 offset <- offset + offset * 0.5
        #                 fitness <- fitness * 0.75
        #             continue
        #         else:
        #             match(request, room)
        #             break
        start = time.time()
        while request.is_alive:
            for room in rooms(request, offset):
                if match_quality(request, room) < fitness and time.time() - start > 30:
                    offset += offset * 0.5
                    fitness *= 0.75
                    continue
                else:
                    match(request, room)
                    break

    @staticmethod
    def rooms(request: Request, offset: int):
        if request.lobby_id in _games:
            for room in _games[request.lobby_id]:
                if abs(room.rating.getRating() - request.player.rating.getRating()) <= offset:
                    yield room

    @staticmethod
    def match_quality(request: Request, room: Room) -> float:
        def diff_rating(request, room):
            return abs(request.player.rating.getRating() - room.rating)/(RATING_MAX - RATING_MIN)  
        def var_rating(request, room):
            avg = (room.rating * room.size + request.player.rating.getRating())/(room.size + 1)
            return variance(map(lambda player: player.rating.getRating(), room.players))/((RATING_MAX - avg)*(avg - RATING_MIN))
        
        return 1.0 - ((2/3)*diff_rating(request, room) + (1/3)*var_rating(request, room))
    
    @staticmethod
    def match(request, room):
        room += request.player
