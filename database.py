import datetime as dt
import typing as t
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from config import engine


""" Функционал подключения к БД """


class Singleton(type):
    _instances: t.Dict[t.Type, t.Dict[str, object]] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = {}
        key = str(args) + str(kwargs)
        if key not in cls._instances[cls]:
            cls._instances[cls][key] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls][key]


class CConnection(metaclass=Singleton):
    def __init__(self, custom_engine=None):
        self.custom_engine = custom_engine
        self.engine = create_engine(
            engine if not self.custom_engine else self.custom_engine
        )
        self.refresh_time = dt.datetime.now() + dt.timedelta(seconds=10)
        self.session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.session()


@contextmanager
def session_scope(connection: CConnection) -> Session:
    session = connection.get_session()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        session.close()
