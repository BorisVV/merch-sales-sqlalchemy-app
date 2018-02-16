import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True # TODO: Change this to False.

# SECRET_KEY = 'testkey'
SQLALCHEMY_DATABASE_URI = 'sqlite:///sports.db'
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'sport-team.db')

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_CONNECT_OPTIONS = {}

del os
