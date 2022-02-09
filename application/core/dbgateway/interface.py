from abc import ABC, abstractmethod


class BaseDbGateway():
    def __init__(self, db_session):
        self.db = db_session


class AbstractInvitationDbGateway(BaseDbGateway, ABC):
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
