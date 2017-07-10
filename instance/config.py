import os
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_db'
    DEBUG = True

class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}

config_name = os.getenv('APP_SETTINGS') # config_name = "development"
app = FlaskAPI(__name__, instance_relative_config=True)
app.config.from_object(app_config[config_name])
# app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize sql-alchemy
db = SQLAlchemy()
#app = FlaskAPI()

db.init_app(app)