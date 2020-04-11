import os
basedir = os.path.abspath(os.path.dirname(__file__))
TESTDB = 'testing.db'
TESTDB_PATH = os.path.join(basedir, TESTDB)

class Config(object):
    """
    Configuration for database
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'backend.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False

class TestConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'testing.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    TESTING = True
    DEBUG = True