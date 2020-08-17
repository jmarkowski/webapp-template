from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session


Base = declarative_base()


def create_tables(engine):
    Base.metadata.create_all(bind=engine)


def get_db_interface(db_uri='sqlite:///sqlite3.db', scopefunc=None):
    """Get a database session with an optional scoping function to ensure that
    sessions are created and removed within a request/response cycle.

    'db_uri' format:
        postgresql://[user[:password]@][netloc][:port][/dbname]
        sqlite:///path/to/data.sqlite
    """
    engine = create_engine(db_uri, connect_args={'check_same_thread': False})

    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    session = scoped_session(session_factory, scopefunc=scopefunc)

    return session, engine
