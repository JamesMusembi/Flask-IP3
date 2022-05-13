import os

class Config:

    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://moringa:james@localhost/pitches'


# class ProdConfig(Config):
#     DEBUG = False

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL','')
    # if SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
    # SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', "postgresql://", 1)     
    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://moringa:james@localhost/pitches'
        # sql_alchemy_conn = 'postgresql://moringa:james@host:port/db'
    DEBUG = False

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://moringa:james@localhost/pitches'

    DEBUG = True
    

config_options = {
'development':DevConfig,
'production':ProdConfig
}

