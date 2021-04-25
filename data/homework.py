import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Homework(SqlAlchemyBase):
    __tablename__ = 'homework'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)

    lesson = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    task = sqlalchemy.Column(sqlalchemy.String, nullable=True)
