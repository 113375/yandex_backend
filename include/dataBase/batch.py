from sqlalchemy_serializer import SerializerMixin
from include.db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm


class Batch(SqlAlchemyBase, SerializerMixin):
    """Класс партии заказов"""
    __tablename__ = 'batch'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    courier_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("courier.courier_id"), nullable=False)
    assign_time = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    finish_time = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    all_weight = sqlalchemy.Column(sqlalchemy.Float, default=0)
