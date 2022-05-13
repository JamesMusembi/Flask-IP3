from distutils.debug import DEBUG
import os

class Config:

    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://moringa:james@localhost/pitches'


# class ProdConfig(Config):
    # DEBUG = False

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:james@localhost/pitches'
    DEBUG = False
    

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

