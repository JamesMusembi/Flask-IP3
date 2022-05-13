import os

class Config:

    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://moringa:james@localhost/pitches'


class ProdConfig(Config):

    SQLALCHEMY_DATABASE_URI ='postgresql://mxhwjrztvelttj:f78c638ad02dbae50ef11ca5e8acab88b2bdc1a3ae0e1fa274ff3186213aa009@ec2-107-22-238-112.compute-1.amazonaws.com:5432/de50v5u7j3bip6'
    DEBUG = False
    

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://moringa:james@localhost/pitches'

    DEBUG = True
    

config_options = {
'development':DevConfig,
'production':ProdConfig
}

