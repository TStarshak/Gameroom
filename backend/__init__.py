#################
#### imports ####
#################

from flask import Flask
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

################
#### config ####
################

app = Flask(__name__)
# bcrypt = Bcrypt(app)
# app.config.from_object(os.environ['APP_SETTINGS'])
# db = SQLAlchemy(app)

# # register our blueprints


# from .models import Player

# login_manager.login_view = "users.login"


# @login_manager.user_loader
# def load_user(user_id):
#     return Player.query.filter(Player.id == int(user_id)).first()