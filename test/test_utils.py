import pytest
from backend.mock_models import obj_to_dict, Player, RATING_MIN, RATING_MAX
import random

def test_hide_password():
    player = Player(1, random.randint(RATING_MIN, RATING_MAX),
                    username='Randomplayer{}'.format(1),
                    password="rando{}".format(1))
    assert 'password' not in obj_to_dict(player)
