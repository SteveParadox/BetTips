# importing libraries
import os


# app configuration
class Config:

    ENV = 'prod'

    if ENV == 'dev':
        SECRET_KEY = "43rtgtrf04o0gkomrg0gmr0gtgmg0trgo"
        SQLALCHEMY_DATABASE_URI = 'sqlite:///store.db'
        SQLALCHEMY_TRACK_MODIFICATIONS = False

    else:
        SECRET_KEY = "795849f0d2328258710ae9c71cb795849f0d2328258710ae9c71cb4b5ea4b5ea"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SQLALCHEMY_DATABASE_URI = ""
