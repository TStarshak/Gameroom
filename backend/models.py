from backend import db

class Player (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40))
    password = db.Column(db.String(40))
    rating = db.Column(db.Float)

class Lobby (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lobby_id = db.Column(db.String(40))
    timestamp = db.Column(db.Integer)
    type_ = db.Column(db.String(40))
    rating = db.Column(db.Integer)
    external = db.Column(db.String(5))