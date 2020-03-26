from backend import db

class Player (db.Model):

    __table_args__ = (
        db.CheckConstraint('rating >= 0 and rating <= 5.0'),
    )

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40))
    password = db.Column(db.String(40))
    email = db.Column(db.String(40))
    rating = db.Column(db.Float, default=2.5)

class Lobby (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lobby_id = db.Column(db.String(40))
    timestamp = db.Column(db.Integer)
    type_ = db.Column(db.String(40))
    cap = db.Column(db.Integer)
    player = db.Column(db.Integer, db.ForeignKey(Player.id))
    rating = db.Column(db.Float)
    external = db.Column(db.String(5))