from backend import db
import datetime

RATING_MAX = 1000
RATING_MIN = 0
RATING_DEFAULT = (RATING_MAX + RATING_MIN)/2

class BaseMixin(object):
    @classmethod
    def create(cls, **kw):
        obj = cls(**kw)
        db.session.add(obj)
        db.session.commit()

class Player (db.Model, BaseMixin):
    __tablename__ = 'player'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40))
    password = db.Column(db.String(40))
    email = db.Column(db.String(40))
    toxic = db.Column(db.Integer, default=RATING_DEFAULT)
    skill = db.Column(db.Integer, default=RATING_DEFAULT)
    num_evals = db.Column(db.Integer, default=1)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))

class Room(db.Model, BaseMixin):

    __tablename__ = 'room'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())
    lobby_id = db.Column(db.Integer, db.ForeignKey('lobby.id'))
    players = db.relationship('Player', backref='joined_room', lazy='dynamic')

class Lobby (db.Model, BaseMixin):
    __tablename__ = 'lobby'
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String(40))
    timestamp = db.Column(db.Integer)
    short_description = db.Column(db.String(40))
    cap = db.Column(db.Integer)
    rooms = db.relationship('Room', backref='game_lobby', lazy='dynamic')