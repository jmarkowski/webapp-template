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

    def add_email(self, email):
        self.email = email

        current_app.db.add(self)
        current_app.db.commit()

    def get_email(self, email):
        return current_app.db.query(InvitationGateway).filter_by(email=email).first()

    def get_email_list(self):
        rows = current_app.db.query(InvitationGateway).all()

        return [r.email for r in rows]
