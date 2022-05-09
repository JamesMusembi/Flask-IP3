import os

from flask import Config

class Confif:
    SQLAlchemy_DATABASE_URI=os.getenv('DATABASE_URL')
    DEBUG=os.getenv('DEBUG')