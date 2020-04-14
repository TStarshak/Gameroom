from backend import db
import datetime
import math
from statistics import mean
from typing import Union
from flask_login import UserMixin
from werkzeug.security import safe_str_cmp
import warnings

RATING_MAX = 1000
RATING_MIN = 0
RATING_DEFAULT = (RATING_MAX + RATING_MIN)/2

class ModelMixin(object):
    """
    Mixins for main functional tables
    """
    @classmethod
    def create(cls, **kw):
        obj = cls(**kw)
        db.session.add(obj)
        return cls._commit_changes(obj, fail_msg="Failed to create object")
    
    @classmethod
    def _commit_changes(cls, obj, fail_msg):
        try:
            db.session.commit()
            return obj, None
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            return None, fail_msg


    @classmethod
    def get_by_id(cls, id_):
        return cls.query.get_or_404(id_)

    def representation(self):
        raise NotImplementedError



class Player (db.Model, ModelMixin, UserMixin):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(40))
    email = db.Column(db.String(40))
    toxic = db.Column(db.Integer, default=RATING_DEFAULT)
    skill = db.Column(db.Integer, default=RATING_DEFAULT)
    num_evals = db.Column(db.Integer, default=1)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))

    def verify_password(self, password):
        return safe_str_cmp(password, self.password)

    @classmethod
    def update_rating(cls, id: int, toxic_rates: int, skill_rates: int):
        player = cls.get_by_id(id)
        player.toxic += toxic_rates
        player.skill += skill_rates
        player.num_evals += 1
        db.session.commit()

    @property
    def rating(self) -> float:
        player = self.get_by_id(self.id)
        normalized_rating = (player.skill - player.toxic)/(player.skill) # should be between -1 and 1
        return round(min(max(((normalized_rating + 1)/2)*(RATING_MAX - RATING_MIN), RATING_MIN), RATING_MAX), 2) # rounding and bounding
    
    @property
    def representation(self):
        return {
            "id" : self.id,
            "username" : self.username,
            "email" : self.email,
            "rating" : self.rating,
            "num_evals" : self.num_evals
        }
    


class Room(db.Model, ModelMixin):

    __tablename__ = 'room'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())
    lobby_id = db.Column(db.Integer, db.ForeignKey('lobby.id'))
    players = db.relationship('Player', backref='joined_room', lazy='dynamic')

    @property
    def representation(self):
        return {
            "id" : self.id,
            "timestamp" : self.timestamp,
            "lobby_id" : self.lobby_id,
            "players" : [player.representation for player in self.players],
            "rating" : self.rating
        }

    
    def append(self, player: Union[int, Player]):
        warnings.warn("Experimental")
        if type(player) is int:
            player = Player.get_by_id(player)
        if len(self.players) < Lobby.get_by_id(self.lobby_id).cap:
            self.players.append(player)
            _, status = self._commit_changes(self, "Failed to modify room")
            if status is None:
                return True
        return False
    
    def add(self, room: Union[int, "Room"]):
        warnings.warn("Experimental")
        if type(room) is int:
            room = self.get_by_id(room)
        lobby = Lobby.get_by_id(self.lobby_id)
        cap = lobby.cap
        if self.lobby_id == room.lobby_id and len(self.players) + len(room.players) < cap:
            self.players += room.players
            Room.query.delete(room)
            _, status = self._commit_changes(self, "Failed to modify room")
            if status is None:
                return True
        return False

    @property
    def rating(self):
        return mean([player.rating for player in self.players])

class Lobby (db.Model, ModelMixin):
    __tablename__ = 'lobby'
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String(40))
    timestamp =  db.Column(db.DateTime, default=datetime.datetime.now())
    short_description = db.Column(db.String(40))
    cap = db.Column(db.Integer)
    rooms = db.relationship('Room', backref='game_lobby', lazy='dynamic')

    @property
    def representation(self):
        return {
            "id" : self.id,
            "game" : self.game,
            "timestamp" : self.timestamp,
            "desc" : self.short_description,
            "cap" : self.cap
        }