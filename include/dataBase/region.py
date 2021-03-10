from sqlalchemy_serializer import SerializerMixin
from include.db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm


class Region(SqlAlchemyBase, SerializerMixin):
    """Класс таблицы с районами"""
    __tablename__ = 'region'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)


    table_for_courier = sqlalchemy.Table(
        'courier_region',
        SqlAlchemyBase.metadata,
        sqlalchemy.Column('courier', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('courier.courier_id')),
        sqlalchemy.Column('region', sqlalchemy.Integer,
                          sqlalchemy.ForeignKey('region.id'))
    )