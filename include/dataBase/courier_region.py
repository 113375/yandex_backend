from sqlalchemy_serializer import SerializerMixin
from include.db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm


class CourierRegion(SqlAlchemyBase, SerializerMixin):
    """Класс, объединяющий район и курьера(многие ко многим)"""
    __tablename__ = 'courier_region'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    courier_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("courier.courier_id"), nullable=False)
    region_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("region.id"), nullable=False)