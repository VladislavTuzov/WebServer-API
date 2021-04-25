import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Student(SqlAlchemyBase):
    __tablename__ = 'student'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    school_id = sqlalchemy.Column(sqlalchemy.Integer)
    klass_id = sqlalchemy.Column(sqlalchemy.Integer)
    name_klass = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    appraisals_url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    events_url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # categories = orm.relation("Category", secondary="association", backref="news")
