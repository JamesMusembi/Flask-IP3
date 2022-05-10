import os

class Config:

    DATABASE_URI = 'sqlite:///site.db'


class ProdConfig(Config):
    DEBUG = False


class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}

