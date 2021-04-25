import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Inquiry(SqlAlchemyBase):
    __tablename__ = 'inquiry'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('user.id'), nullable=True)
    name_school = sqlalchemy.Column(
        sqlalchemy.String, nullable=True)
    schort_name_school = sqlalchemy.Column(
        sqlalchemy.String, nullable=True)

    # categories = orm.relation("Category", secondary="association", backref="news")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
