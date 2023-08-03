# importing libraries
import datetime
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from .config import Config, CACHE_CONFIG
from flask_caching import Cache
import redis

# framework initialization
app = Flask(__name__)

app.config.from_object(Config)

# database Iniitialization
db = SQLAlchemy()
cache = Cache(config=CACHE_CONFIG)


def create_app(config_class=Config):

# initializing required modules to app
    db.init_app(app)
    cache.init_app(app)
    

# Creating blueprint configuration for app
    from .editor.routes import edit
    from .Analysis.routes import analysis


# registering packages to blueprint
    app.register_blueprint(analysis)


# registering packages to blueprint
    app.register_blueprint(edit)


    return app
