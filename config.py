import os

class Config:

    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://moringa:james@localhost/pitches'


class ProdConfig(Config):
    DEBUG = False
    

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://moringa:james@localhost/pitches'

    DEBUG = True
    

config_options = {
'development':DevConfig,
'production':ProdConfig
}

