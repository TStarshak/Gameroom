from flask_script import Manager
import random
import datetime
from backend.mock_models import Room, Player, RATING_MAX, RATING_MIN
from backend import app

manager = Manager(app)


@manager.command
def populate():
    player_ids = [1, 2, 3, 4, 5]
    for player_id in player_ids:
        Player(player_id, random.randint(RATING_MIN, RATING_MAX),
               username='Randomplayer{}'.format(player_id),
               password="rando{}".format(player_id))
    Room(1, datetime.datetime.now(), type_=1, players=[1, 3, 5])
    app.run(debug=True)

@manager.command
def run():
    app.run(debug=True)

if __name__ == "__main__":
    manager.run()
