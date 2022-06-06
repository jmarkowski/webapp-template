from abc import ABC, abstractmethod


class BaseDbGateway():
    def __init__(self, db_session):
        self.db = db_session
