from sqlalchemy_serializer import SerializerMixin
from include.db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm


class CourierType(SqlAlchemyBase, SerializerMixin):
    """Класс таблицы с регионами"""
    __tablename__ = 'courier_type'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    weight = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
