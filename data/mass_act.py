import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Action__mass(SqlAlchemyBase, UserMixin):
    __tablename__ = 'action__mass'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    mass_el = sqlalchemy.Column(sqlalchemy.JSON, nullable=True)
