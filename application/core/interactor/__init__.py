import logging

from core.config import Config
from core.dbgateway import DbGateway
from .invitation import InvitationInteractor


class Interactor():
    """Interface to the application use cases."""

    def __init__(self,
            config,
            db_gateway,
            logger,
        ):
        assert isinstance(config, Config)
        assert isinstance(db_gateway, DbGateway)
        assert isinstance(logger, logging.Logger)

        self.invitation = InvitationInteractor(
            config,
            db_gateway.invitation,
            logger,
        )
