# import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Director(SqlAlchemyBase):
    __tablename__ = 'director'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_dir = sqlalchemy.Column(
        sqlalchemy.Integer)
    school_id = sqlalchemy.Column(sqlalchemy.Integer)
    # categories = orm.relation("Category", secondary="association", backref="news")
