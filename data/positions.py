import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Positions(SqlAlchemyBase, UserMixin):
    __tablename__ = 'positions'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    structure = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    weight = sqlalchemy.Column(
        sqlalchemy.Integer, nullable=True)  # вес продукта
    kategory = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
