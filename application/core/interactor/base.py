import logging

from core.config import Config
from core.dbgateway import DbGateway


class Interactor():
    """Interface to the application use cases."""

    def __init__(self,
            config: Config,
            db_gateway: DbGateway,
            logger: logging.Logger,
        ):

        # Connect all interactors here
        pass
