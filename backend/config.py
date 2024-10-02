"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Set Flask config variables."""
    # General Config
    ENVIRONMENT = environ.get("ENVIRONMENT")
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_DEBUG = environ.get("FLASK_DEBUG")
    SECRET_KEY = environ.get("SECRET_KEY")

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    """Development config."""
    ENVIRONMENT = 'development'
    FLASK_DEBUG = True

    # Database
    POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD")
    POSTGRES_HOST = environ.get("POSTGRES_HOST")
    POSTGRES_DB = environ.get("POSTGRES_DB")
    POSTGRES_USER = environ.get("POSTGRES_USER")
    POSTGRES_PORT = environ.get("POSTGRES_PORT")

    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@'
        f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    )


class TestConfig(Config):
    """Test config."""
    ENVIRONMENT = 'testing'
    FLASK_DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db.sqlite3'


if environ.get("ENVIRONMENT") == 'testing':
    class BaseConfig(TestConfig):
        pass
else:
    class BaseConfig(DevConfig):
        pass
