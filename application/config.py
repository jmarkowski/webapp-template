import os

from core.config import Config


class DefaultConfig(Config):
    INFO = {
        'product': 'Web Application Template'
    }

    # Directories
    STATIC_DIR = os.path.realpath('./static')
    TEMPLATE_DIR = os.path.realpath('./template')

    # Connection URI format:
    #   postgresql://[user[:password]@][netloc][:port][/dbname]
    #   sqlite:///path/to/data.sqlite
    DB_URI = 'postgresql://{user}:{password}@{server}:5432/{database}' \
             .format(user=os.getenv('POSTGRES_USER'),
                     password=os.getenv('POSTGRES_PASSWORD'),
                     database=os.getenv('POSTGRES_DB'),
                     server=os.getenv('SQL_DATABASE_SERVER_NAME'))

    # In a production setting, this key will be overwritten by what is in
    # 'secrets/settings.py'
    SECRET_KEY = 'overwrite-this-key-for-production'

    # Flask settings

    # Browsers will not allow JavaScript access to cookies marked as “HTTP only”
    # for security.
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    PAGE_PLUGIN = {
        'analytics': '<!-- No analytics plugin -->'
    }

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
    DB_URI = 'sqlite:///:memory:' # Use RAM database
    TESTING = True


class DevelopmentConfig(DefaultConfig):
    DEBUG = True


config_map = {
    'production' : ProductionConfig,
    'testing' : TestingConfig,
    'development' : DevelopmentConfig,
}


def create_config(config_strategy=os.getenv('CONFIG_STRATEGY'),
        override_settings=None):
    """Return an instance of the Config object."""

    cfg = config_map[config_strategy](override_settings=override_settings)
    setattr(cfg, 'CONFIG_STRATEGY', config_strategy)

    # Config inception...
    # The basic reason for this is because Flask unfortunately has its own
    # required configuration setup, but I want to keep both the Flask
    # configuration and the application configuration under one roof.
    # So, we get around this issue by accessing a reference to the
    # application configuration (if needed) with, for example,
    # current_app.config['CONFIG'].
    setattr(cfg, 'CONFIG', cfg)

    return cfg
