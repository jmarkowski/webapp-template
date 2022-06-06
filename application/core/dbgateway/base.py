from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from .database import TableBase


class DbGateway():
    """Gateway interface to the data in the database."""

    def __init__(self, db_session):
        assert db_session

        # Connect all database gateways here
        pass

    @staticmethod
    def open_session(db_uri='sqlite:///sqlite3.db',
            scopefunc=None,
            echo_raw_sql=False):
        """Get a database session with an optional scoping function to ensure that
        sessions are created and removed within a request/response cycle.

        'db_uri' format:
            postgresql://[user[:password]@][netloc][:port][/dbname]
            sqlite:///path/to/data.sqlite
        """
        if db_uri.startswith('sqlite'):
            # If it's a memory-based database, specify a StaticPool to only support
            # a single connection.
            #
            # See https://stackoverflow.com/questions/21766960/operationalerror-no-such-table-in-flask-with-sqlalchemy
            poolclass = StaticPool if ':memory:' in db_uri else None

            engine = create_engine(db_uri,
                                   connect_args={'check_same_thread': False},
                                   echo=echo_raw_sql,
                                   poolclass=poolclass)
        else:
            engine = create_engine(db_uri, echo=echo_raw_sql)

        session_factory = sessionmaker(
            autocommit=False,
            autoflush=True,
            bind=engine,
        )

        # Create all the necessary tables, if they haven't already been created.
        with engine.begin() as conn:
            TableBase.metadata.create_all(bind=conn)

        return scoped_session(session_factory, scopefunc=scopefunc)

    @staticmethod
    def close_session(db_session):
        db_session.remove()
