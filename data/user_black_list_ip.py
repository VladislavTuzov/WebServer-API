import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Black_ip(SqlAlchemyBase, UserMixin):
    __tablename__ = 'black_ip'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    ip = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cause = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    time_ban = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
