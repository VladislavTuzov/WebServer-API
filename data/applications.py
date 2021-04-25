# import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Applications(SqlAlchemyBase):
    __tablename__ = 'applications'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    apprentice = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    patronymic = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(
        sqlalchemy.String, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    school = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    short_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    dob = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # categories = orm.relation("Category", secondary="association", backref="news")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
