import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'user'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    apprentice = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    patronymic = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(
        sqlalchemy.String, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo = sqlalchemy.Column(sqlalchemy.String)
    # добавить nullable=True
    school = sqlalchemy.Column(sqlalchemy.String)
    # добавить nullable=True
    dob = sqlalchemy.Column(sqlalchemy.String)
    # events_url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # добавить nullable=True
    roles = sqlalchemy.Column(sqlalchemy.String)  # добавить nullable=True
    created_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now)

    # news = orm.relation("News", back_populates='user')

    def __repr__(self):
        return f'<User> {self.id} {self.name} {self.email}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
