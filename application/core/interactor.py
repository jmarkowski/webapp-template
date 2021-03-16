from abc import ABC, abstractmethod
import logging


class AbstractInvitationDataGateway(ABC):
    """This class specifies the data interface methods required by the
    interactor to accomplish its tasks.
    """

    @abstractmethod
    def add_email(self, email):
        raise NotImplementedError

    @abstractmethod
    def get_email(self, email):
        raise NotImplementedError

    @abstractmethod
    def get_email_list(self):
        raise NotImplementedError


class InvitationInteractor(object):
    """This class contains operations required for tracking a list of invited
    users.
    """

    def __init__(self, gateway, logger):
        assert isinstance(gateway, AbstractInvitationDataGateway)
        assert isinstance(logger, logging.Logger)

        self.gateway = gateway
        self.logger = logger

    def add_email_to_invite_list(self, email):
        self.gateway.add_email(email)

    def is_email_already_invited(self, email):
        return True if self.gateway.get_email(email) else False

    def get_invite_list(self):
        email_lst = self.gateway.get_email_list()

        self.logger.info('Fetching invite list ...')

        return email_lst
