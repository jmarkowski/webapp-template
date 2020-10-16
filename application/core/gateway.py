from .database import InvitationData
from .interactor import AbstractInvitationDataGateway


class InvitationDataGateway(AbstractInvitationDataGateway):

    def __init__(self, db_session):
        assert db_session
        self.db = db_session

    def add_email(self, email):
        assert isinstance(email, str)

        new_invitation = InvitationData()
        new_invitation.email = email.lower()

        self.db.add(new_invitation)
        self.db.commit()

    def get_email(self, email):
        assert isinstance(email, str)

        q = self.db.query(InvitationData)

        return q.filter_by(email=email.lower()).first()

    def get_email_list(self):
        q = self.db.query(InvitationData)

        return [record.email for record in q.all()]
