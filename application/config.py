from os import getenv

from core.config import Config


class DefaultConfig(Config):
    SITE = {
        'brand': 'Web Application Brand'
    }

    # Connection URI format:
    #   postgresql://[user[:password]@][netloc][:port][/dbname]
    #   sqlite:///path/to/data.sqlite
    DB_URI = 'sqlite:///:memory:' # Use RAM database as default.

    # In a production setting, this key will be overwritten by what is in
    # 'secrets/settings.py'
    SECRET_KEY = 'overwrite-this-key-for-production'

    # Flask settings

    # Browsers will not allow JavaScript access to cookies marked as “HTTP only”
    # for security.
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    @classmethod
    def check_config_conditions(cls):
        # Check the configuration for any possible show-stopping settings, and
        # provide helpful assertion messages if needed.
        assert getattr(cls, 'SECRET_KEY', None), \
            'SECRET_KEY is not defined'


class ProductionConfig(DefaultConfig):
    # This is an instance-specific parameter and should be defined in
    # 'secrets/settings.py'
    SECRET_SETTINGS = './secrets/settings.py'


class TestingConfig(DefaultConfig):
    DB_URI = 'sqlite:///:memory:'
    TESTING = True


class DevelopmentConfig(DefaultConfig):
    DB_URI = 'postgresql://{user}:{password}@{server}:5432/{database}' \
             .format(user=getenv('POSTGRES_USER'),
                     password=getenv('POSTGRES_PASSWORD'),
                     database=getenv('POSTGRES_DB'),
                     server=getenv('SQL_DATABASE_SERVER_NAME'))
    DEBUG = True


config_map = {
    'production' : ProductionConfig,
    'testing' : TestingConfig,
    'development' : DevelopmentConfig,
}


def create_config(config_strategy=getenv('CONFIG_STRATEGY'), override_settings=None):
    """Return an instance of the Config object."""

    cfg = config_map[config_strategy](override_settings=override_settings)
    setattr(cfg, 'CONFIG_STRATEGY', config_strategy)

    return cfg
