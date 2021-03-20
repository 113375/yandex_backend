from sqlalchemy_serializer import SerializerMixin
from include.db_session import SqlAlchemyBase
import sqlalchemy
from include.dataBase.region import Region
from sqlalchemy import orm


class Courier(SqlAlchemyBase, SerializerMixin):
    """Класс таблицы 'курьер' в базе данных"""
    __tablename__ = 'courier'

    courier_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   primary_key=True, autoincrement=True)

    courier_type = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("courier_type.id"), nullable=False)
    rating = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    earnings = sqlalchemy.Column(sqlalchemy.Float, nullable=True)

    regions = orm.relation("Region",
                           secondary="courier_region",
                           backref="courier")

    orders = orm.relation("Order",
                          secondary="courier_order",
                          backref="order")

    courier = sqlalchemy.Table(
        'courier_delivery',
        SqlAlchemyBase.metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
        sqlalchemy.Column('courier_id', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('courier.courier_id')),
        sqlalchemy.Column("begin", sqlalchemy.DateTime, nullable=False),
        sqlalchemy.Column("end", sqlalchemy.DateTime, nullable=True),
        sqlalchemy.Column("finished", sqlalchemy.Boolean, default=False)
    )
