import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
# from sqlalchemy.dialect.postgresql import JSON

from .db_session import SqlAlchemyBase


class Orders(SqlAlchemyBase, UserMixin):
    __tablename__ = 'orders'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name_klient = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    adress = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    phone_number = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    times_orders = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now)
    applied_coupons = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    order_note = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    execution_speed = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    payment_method = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    structure = sqlalchemy.Column(sqlalchemy.JSON, nullable=True)
    back_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    summ = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    status = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    scores = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
