from sqlalchemy_serializer import SerializerMixin
from include.db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm


class OrderHours(SqlAlchemyBase, SerializerMixin):
    """Класс, соеденяющий часы с заказом"""
    __tablename__ = 'order_hours'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    order_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("order.id"), nullable=False)
    begin = sqlalchemy.Column(sqlalchemy.Time, nullable=False)
    end = sqlalchemy.Column(sqlalchemy.Time, nullable=False)