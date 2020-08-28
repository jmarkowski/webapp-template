from abc import ABC, abstractmethod


class AbstractInvitationGateway(ABC):
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

    def __init__(self, gateway):
        self.gateway = gateway()
        self.email = None

    def add_email_to_invite_list(self, email):
        self.gateway.add_email(email)

    def is_email_already_invited(self, email):
        return True if self.gateway.get_email(email) else False

    def get_invite_list(self):
        email_lst = self.gateway.get_email_list()

        return email_lst
