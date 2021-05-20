import logging

from core.config import Config
from core.dbgateway.interface import AbstractInvitationDbGateway


class InvitationInteractor():
    """This class contains operations required for tracking a list of invited
    users.
    """

    def __init__(self, config, gateway, logger):
        assert isinstance(config, Config)
        assert isinstance(gateway, AbstractInvitationDbGateway)
        assert isinstance(logger, logging.Logger)

        self.config = config
        self.gateway = gateway
        self.logger = logger

    def add_email_to_invite_list(self, email):
        self.gateway.add_email(email)

    def is_email_already_invited(self, email):
        return bool(self.gateway.get_email(email))

    def get_invite_list(self):
        email_lst = self.gateway.get_email_list()

        self.logger.info('Fetching invite list ...')

        return email_lst
