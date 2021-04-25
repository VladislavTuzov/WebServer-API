# import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class UsersProfile(SqlAlchemyBase):
    __tablename__ = 'users_profile'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_users = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    zipfiles = sqlalchemy.Column(sqlalchemy.LargeBinary)
    # categories = orm.relation("Category", secondary="association", backref="news")
