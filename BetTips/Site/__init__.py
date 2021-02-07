# importing libraries
import datetime
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from .config import Config


# framework initialization
app = Flask(__name__)

app.config.from_object(Config)

# database Iniitialization
db = SQLAlchemy()

def create_app(config_class=Config):

# initializing required modules to app
    db.init_app(app)


# Creating blueprint configuration for app
    from .editor.routes import edit


# registering packages to blueprint
    app.register_blueprint(edit)


    return app
