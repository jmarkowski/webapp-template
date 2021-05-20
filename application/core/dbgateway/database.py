import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TypeDecorator

from util.datetime import now_tz_utc


# Construct a base class for the declarative table class definitions below.
# This new base class will be given a metaclass that produces appropriate Table
# objects used by SQLAlchemy.
TableBase = declarative_base()


class TZDateTime(TypeDecorator):
    """
    A DateTime type which can only store timezone aware DateTimes.

    There are two kinds of datetime objects: "naive" and "aware"

    An aware object has sufficient knowledge of applicable algorithmic and
    political time adjustments, such as time zone and daylight saving time
    information, to locate itself relative to other aware objects.

    A naive object does not contain enough information to unambiguously locate
    itself relative to other date/time objects.

    Source:
      https://docs.sqlalchemy.org/en/14/core/custom_types.html#store-timezone-aware-timestamps-as-timezone-naive-utc
    """
    impl = DateTime

    def process_bind_param(self, value, dialect):
        if value is not None:
            if not value.tzinfo:
                raise TypeError('tzinfo is required')
            value = value.astimezone(datetime.timezone.utc).replace(
                tzinfo=None
            )
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = value.replace(tzinfo=datetime.timezone.utc)
        return value

    def __repr__(self):
        return 'TZDateTime()'


class BaseDataMixin():
    """Base mixin for common columns and methods for all data models."""

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    created_on = Column(
        TZDateTime,
        default=now_tz_utc
    )

    updated_on = Column(
        TZDateTime,
        default=now_tz_utc,
        onupdate=now_tz_utc
    )

    def __str__(self):
        fields = self.__table__.c.keys()
        obj_addr = hex(id(self))

        value_lst = []

        for f in fields:
            value_lst.append(f'{f}={getattr(self, f)}')

        value_str = ','.join(value_lst)

        return f'<{obj_addr} {self.__class__.__name__}({value_str})>'


class InvitationData(BaseDataMixin, TableBase):
    __tablename__ = "invitations"

    email = Column(
        String(80),
        unique=True,
        index=True,
    )

    def __repr__(self):
        return '<Invitation {}>'.format(self.email)
