from sqlalchemy_serializer import SerializerMixin
from include.db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm


class Order(SqlAlchemyBase, SerializerMixin):
    """Класс заказа"""
    __tablename__ = 'order'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    region_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("region.id"), nullable=False)
    weight = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    completed = sqlalchemy.Column(sqlalchemy.Boolean, default=False)