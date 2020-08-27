from os import getenv


class Config(object):
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

class ProductionConfig(Config):
    # This is an instance-specific parameter and should be defined in
    # 'secrets/settings.py'
    DB_URI = None


class TestingConfig(Config):
    DB_URI = 'sqlite:///test.db'
    TESTING = True


class DevelopmentConfig(Config):
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
