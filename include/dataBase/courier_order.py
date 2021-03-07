from sqlalchemy_serializer import SerializerMixin
from include.db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm


class CourierOrder(SqlAlchemyBase, SerializerMixin):
    """Класс, объединяющий район с заказом"""
    __tablename__ = 'courier_order'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    courier_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("courier.courier_id"), nullable=False)
    order_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("order.id"), nullable=False)
