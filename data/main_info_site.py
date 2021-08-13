import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class MainInfo(SqlAlchemyBase, UserMixin):
    __tablename__ = 'maininfo'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    logo = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # в синей полосе меню сверху слева
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    phone_number = sqlalchemy.Column(sqlalchemy.String, nullable=True)
