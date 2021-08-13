import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

from random import choice
from string import ascii_letters

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'user'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    adress = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    dob = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(
        sqlalchemy.String, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    back_id = sqlalchemy.Column(
        sqlalchemy.Integer, nullable=True)
    email_check = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    personal_code = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    scores = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    scores_freez = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    roles = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    secret_key_cokies = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    auth_mail = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    created_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f'<User> {self.id} {self.name} {self.email}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def set_personal_code(self):
        self.personal_code = ''.join(choice(ascii_letters) for i in range(6))
