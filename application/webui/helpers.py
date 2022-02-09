from flask import current_app

from core.dbgateway import DbGateway
from core.interactor import Interactor


def get_interactor():
    return Interactor(
        config=current_app.config['CONFIG'],
        db_gateway=DbGateway(current_app.db),
        logger=current_app.logger,
    )
