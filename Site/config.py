# importing libraries
import os


# app configuration
class Config:

    ENV = 'dev'

    if ENV == 'dev':
        SECRET_KEY = "43rtgtrf04o0gkomrg0gmr0gtgmg0trgo"
        SQLALCHEMY_DATABASE_URI = 'sqlite:///store.db'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        MAIL_SERVER = 'smtp.googlemail.com'
        MAIL_PORT = 465
        MAIL_USE_TLS = False
        MAIL_USE_SSL = True
        MAIL_USERNAME = 'vond499y@gmail.com'
        MAIL_PASSWORD = 'saintvirus11'
        MAIL_DEFAULT_SENDER = 'from@example.com'

    else:
        SECRET_KEY = "795849f0d2328258710ae9c71cb795849f0d2328258710ae9c71cb4b5ea4b5ea"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SQLALCHEMY_DATABASE_URI = "postgres://ubroabdhsiwxxn:1edd0690d626c9b0fa720fcce44e5a15afa5a11d12e69c1f586bc7bcd9f5d723@ec2-34-252-251-16.eu-west-1.compute.amazonaws.com:5432/df8bvf9f9npn3o"
        MAIL_SERVER = 'smtp.googlemail.com'
        MAIL_PORT = 465
        MAIL_USE_TLS = False
        MAIL_USE_SSL = True
        MAIL_USERNAME = 'vond499y@gmail.com'
        MAIL_PASSWORD = 'saintvirus11'
        MAIL_DEFAULT_SENDER = 'from@example.com'
