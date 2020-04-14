from flask_script import Manager
import random
import datetime
# from backend.mock_models import Room, Player, RATING_MAX, RATING_MIN
from backend import app, models

manager = Manager(app)

PLAYERS_TO_GEN = 5

@manager.command
def populate():
    # player_ids = [1, 2, 3, 4, 5]
    # for player_id in player_ids:
    #     Player(player_id, random.randint(RATING_MIN, RATING_MAX),
    #            username='Randomplayer{}'.format(player_id),
    #            password="rando{}".format(player_id))
    # Room(1, datetime.datetime.now(), type_=1, players=[1, 3, 5])
    # app.run(debug=True)
    for i in range(1, PLAYERS_TO_GEN+1):
        models.Player.create(username='Randomplayer{}'.format(i), 
                                email='Rando{}@somewhere.somehow'.format(i), 
                                password='Rand{}'.format(i))
        # response = client.post(
        #     '/api/player/create',
        #     data=json.dumps({'username' : 'Randomplayer{}'.format(i),
        #                     'email' : 'Rando{}@somewhere.somehow'.format(i),
        #                     'password': 'Rand{}'.format(i)}),
        #     content_type='application/json'
        # )
        mock_players = {player.id : player.representation for player in models.Player.query.all()}
    models.Lobby.create(game='DOTA 2', 
                        short_description='Some MMORPG game', 
                        cap=8)
    app.run(debug=True)

@manager.command
def run():
    app.run(debug=True)

if __name__ == "__main__":
    manager.run()
