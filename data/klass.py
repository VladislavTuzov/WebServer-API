# import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Klass(SqlAlchemyBase):
    __tablename__ = 'klass'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name_klass = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    schedule_url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    shool_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    # categories = orm.relation("Category", secondary="association", backref="news")
