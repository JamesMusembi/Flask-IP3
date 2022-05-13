from distutils.debug import DEBUG
import os

class Config:

    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://moringa:james@localhost/pitches'


# class ProdConfig(Config):
    # DEBUG = False

# class ProdConfig(Config):
#     SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:james@localhost/pitches'
#     DEBUG = False

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    if SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://','postgresql://',1)    

# class DevConfig(Config):
#     SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://moringa:james@localhost/pitches'

#     DEBUG = True
    
class DevConfig(Config):
   '''
   Development  configuration child class
   Args:
       Config: The parent configuration class with General configuration settings
   '''
   SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://moringa:james@localhost/pitches'
DEBUG = True
 

config_options = {
'development':DevConfig,
'production':ProdConfig
}

