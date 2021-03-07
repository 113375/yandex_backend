from sqlalchemy_serializer import SerializerMixin
from include.db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm


class CourierHours(SqlAlchemyBase, SerializerMixin):
    """Класс, объеденяющий курьера и его рабочик часы(многие ко многим)"""
    __tablename__ = 'courier_hours'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    courier_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("courier.courier_id"))
    begin = sqlalchemy.Column(sqlalchemy.Time, nullable=False)
    end = sqlalchemy.Column(sqlalchemy.Time, nullable=False)
