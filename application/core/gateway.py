from .database import InvitationData
from .invitation import AbstractInvitationDataGateway


class InvitationDataGateway(AbstractInvitationDataGateway):

    db = None

    def __init__(self, db_session):
        assert db_session
        InvitationDataGateway.db = db_session

    @classmethod
    def add_email(cls, email):
        assert isinstance(email, str)

        new_invitation = InvitationData()
        new_invitation.email = email.lower()

        cls.db.add(new_invitation)
        cls.db.commit()

    @classmethod
    def get_email(cls, email):
        assert isinstance(email, str)

        q = cls.db.query(InvitationData)

        return q.filter_by(email=email.lower()).first()

    @classmethod
    def get_email_list(cls):
        q = cls.db.query(InvitationData)

        return [record.email for record in q.all()]
