from abc import ABC, abstractmethod


class AbstractInvitationDataGateway(ABC):
    """This class specifies the data interface methods required by the
    interactor to accomplish its tasks.
    """

    @classmethod
    @abstractmethod
    def add_email(cls, email):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_email(cls, email):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_email_list(cls):
        raise NotImplementedError


class InvitationInteractor(object):
    """This class contains operations required for tracking a list of invited
    users.
    """

    def __init__(self, gateway):
        assert isinstance(gateway, AbstractInvitationDataGateway)
        self.gateway = gateway

    def add_email_to_invite_list(self, email):
        self.gateway.add_email(email)

    def is_email_already_invited(self, email):
        return True if self.gateway.get_email(email) else False

    def get_invite_list(self):
        email_lst = self.gateway.get_email_list()

        return email_lst
