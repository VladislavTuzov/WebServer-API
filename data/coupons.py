import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase

# vievs: new_user, special_offer, special_offer_vip
# ctstus: activ, inactive

# все супоны длинной до 3 включительно знаков являются служебными и используются для сотрудников
# все остальные купоны от 6 и более знаков для клиентов


class Coupon(SqlAlchemyBase, UserMixin):
    __tablename__ = 'coupons'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    coupon = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    view = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    discount = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    status = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    id_klient = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
