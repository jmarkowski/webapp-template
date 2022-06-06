import logging

from core.config import Config
from core.dbgateway import DbGateway
from .invitation import InvitationInteractor


class Interactor():
    """Interface to the application use cases."""

    def __init__(self,
            config: Config,
            db_gateway: DbGateway,
            logger: logging.Logger,
        ):

        self.invitation = InvitationInteractor(
            config,
            db_gateway.invitation,
            logger,
        )
