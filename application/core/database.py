from sqlalchemy import Column, Integer, String

from util.sqlalchemy import Model


class InvitationData(Model):
    __tablename__ = "invitations"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    email = Column(
        String(80),
        unique=True,
        index=True,
    )

    def __repr__(self):
        return '<Invitation {}>'.format(self.email)
