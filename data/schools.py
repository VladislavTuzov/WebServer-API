import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Schools(SqlAlchemyBase):
    __tablename__ = 'schools'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name_schools = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # short_name_schools = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    director = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # categories = orm.relation("Category", secondary="association", backref="news")
