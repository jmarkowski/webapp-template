import os

from webapp import create_app


app = create_app(os.getenv('APP_CONFIG'))
