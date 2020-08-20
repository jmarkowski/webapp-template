from flask import current_app
from sqlalchemy import Column, Integer, String

from util.sqlalchemy import Base
from core.invitation import AbstractGateway


class InvitationGateway(Base):
    __tablename__ = "invite_list"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(80), unique=True, index=True)

    def add_email(self, email):
        self.email = email

        current_app.session.add(self)
        current_app.session.commit()

    def get_email(self, email):
        return current_app.session.query(InvitationGateway).filter_by(email=email).first()

    def get_email_list(self):
        rows = current_app.session.query(InvitationGateway).all()

        return [r.email for r in rows]
