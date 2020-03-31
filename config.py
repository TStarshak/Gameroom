import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """
    Configuration for database
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'backend.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False