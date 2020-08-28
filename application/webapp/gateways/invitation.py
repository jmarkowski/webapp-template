from flask import current_app
from sqlalchemy import Column, Integer, String

from util.sqlalchemy import Base
from core.invitation import AbstractInvitationGateway


class MetaInvitationGateway(type(Base), type(AbstractInvitationGateway)):
    """This metaclass inherits from the two metaclasses that InvitationGateway
    is based on to prevent a metaclass conflict.
    """
    pass


class InvitationGateway(Base, AbstractInvitationGateway,
        metaclass=MetaInvitationGateway):
    __tablename__ = "invite_list"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(80), unique=True, index=True)

    @classmethod
    def add_email(cls, email):
        assert(isinstance(email, str))

        new_invitation = cls()
        new_invitation.email = email.lower()

        current_app.db.add(new_invitation)
        current_app.db.commit()

    @classmethod
    def get_email(cls, email):
        assert(isinstance(email, str))

        return current_app.db.query(cls).filter_by(email=email.lower()).first()

    @classmethod
    def get_email_list(cls):
        rows = current_app.db.query(cls).all()

        return [r.email for r in rows]
