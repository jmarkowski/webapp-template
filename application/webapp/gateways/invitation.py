from flask import current_app

from core.database import InvitationData
from core.invitation import AbstractInvitationGateway


class InvitationGateway(AbstractInvitationGateway):

    @classmethod
    def add_email(cls, email):
        assert isinstance(email, str)

        new_invitation = InvitationData()
        new_invitation.email = email.lower()

        current_app.db.add(new_invitation)
        current_app.db.commit()

    @classmethod
    def get_email(cls, email):
        assert isinstance(email, str)

        q = current_app.db.query(InvitationData)

        return q.filter_by(email=email.lower()).first()

    @classmethod
    def get_email_list(cls):
        q = current_app.db.query(InvitationData)

        return [record.email for record in q.all()]
