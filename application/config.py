class Config(object):
    SITE = {
        'brand': 'Web Application Template'
    }


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True


class DevelopmentConfig(Config):
    DEBUG = True


config_map = {
    'production' : ProductionConfig,
    'testing' : TestingConfig,
    'development' : DevelopmentConfig,
}
