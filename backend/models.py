from backend import db
import datetime

RATING_MAX = 1000
RATING_MIN = 0
RATING_DEFAULT = (RATING_MAX + RATING_MIN)/2

class Player (db.Model):
    __tablename__ = 'player'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40))
    password = db.Column(db.String(40))
    email = db.Column(db.String(40))
    toxic = db.Column(db.Integer, default=RATING_DEFAULT)
    skill = db.Column(db.Integer, default=RATING_DEFAULT)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))

class Room(db.Model):

    __tablename__ = 'room'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())
    lobby_id = db.Column(db.Integer, db.ForeignKey('lobby.id'))

class Lobby (db.Model):
    __tablename__ = 'lobby'
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String(40))
    timestamp = db.Column(db.Integer)
    short_description = db.Column(db.String(40))
    cap = db.Column(db.Integer)
