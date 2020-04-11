#################
#### imports ####
#################

from flask import Flask
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from config import Config
import os
import logging

logger = logging.getLogger('Global logger')

################
#### config ####
################

basedir = os.path.abspath(os.path.dirname(__file__))

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    return app

from rq import Queue
from rq.job import Job
from worker import conn
from flask_socketio import SocketIO
import redis
# redis_lobby = redis.StrictRedis(charset="utf-8",
#                       decode_responses=True)
app = create_app(Config)
socketio = SocketIO(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'mydatabase.db')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from backend import views, models
# app = Flask(__name__)
# bcrypt = Bcrypt(app)
# app.config.from_object(os.environ['APP_SETTINGS'])
# db = SQLAlchemy(app)

# # register our blueprints


# from .models import Player

# login_manager.login_view = "users.login"


# @login_manager.user_loader
# def load_user(user_id):
#     return Player.query.filter(Player.id == int(user_id)).first()