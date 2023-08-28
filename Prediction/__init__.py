# importing libraries
import datetime
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from .config import Config, CACHE_CONFIG
from Prediction.config import Config, CACHE_CONFIG, CSP,
from flask_caching import Cache
import redis
from Prediction.celery_config import celery_init_app
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


sentry_sdk.init(
    dsn="https://e88b83cc342e53d0a941d023c78f9db8@o4505729268449280.ingest.sentry.io/4505729296236544",
    integrations=[
        FlaskIntegration(),
    ],

    traces_sample_rate=1.0,
    profiles_sample_rate=1.0

)

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
    celery=celery_init_app(app)
    celery.conf.update(
        task_serializer='json',
        result_serializer='json',
        accept_content=['json'],
        timezone='UTC',
        enable_utc=True,
    )
    

# Creating blueprint configuration for app
    from .Analysis.routes import analysis


# registering packages to blueprint
    app.register_blueprint(analysis)
    app.register_blueprint(edit)


    return app, celery
