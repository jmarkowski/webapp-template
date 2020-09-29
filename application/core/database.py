from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker



Model = declarative_base()


def init_db_session(db_uri='sqlite:///sqlite3.db',
        scopefunc=None,
        echo_raw_sql=False):
    """Get a database session with an optional scoping function to ensure that
    sessions are created and removed within a request/response cycle.

    'db_uri' format:
        postgresql://[user[:password]@][netloc][:port][/dbname]
        sqlite:///path/to/data.sqlite
    """
    if db_uri.startswith('sqlite'):
        engine = create_engine(db_uri,
                               connect_args={'check_same_thread': False},
                               echo=echo_raw_sql)
    else:
        engine = create_engine(db_uri, echo=echo_raw_sql)

    session_factory = sessionmaker(autocommit=False,
                                   autoflush=False,
                                   bind=engine)

    # Create all the necessary tables
    Model.metadata.create_all(bind=engine)

    return scoped_session(session_factory, scopefunc=scopefunc)


def deinit_db_session(session):
    session.close()


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
