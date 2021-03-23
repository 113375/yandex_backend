from include.dataBase.region import Region
from include.dataBase.courier_hours import CourierHours
from include.dataBase.order_hours import OrderHours
import datetime
"""Файл с функциями"""

def check_time(courier_times, order_times):
    """Проверяет время и ищет совпадения"""
    for time_order in order_times:
        start, finish = time_order.begin, time_order.end
        for time_courier in courier_times:
            courier_start, courier_end = time_courier.begin, time_courier.end
            if (start <= courier_start <= finish) or (courier_start <= start <= courier_end):
                return True
    return False


def add_region(person, db_sess):
    """Функция для соединения в базе данных курьера с его районами"""
    for region in person['regions']:
        """Добавление района в таблицу с районами, если его там не было до этого"""
        if not db_sess.query(Region).filter(Region.name == region).first():
            db_sess.add(Region(name=region))
            db_sess.commit()


def add_courier_hours(person, db_sess, courier_id):
    """Добавление рабочих часов курьеру"""
    hours = person['working_hours']
    for string in hours:
        begin, end = string.split("-")
        begin = datetime.time(hour=int(begin.split(":")[0]), minute=int(begin.split(":")[1]))
        end = datetime.time(hour=int(end.split(":")[0]), minute=int(end.split(":")[1]))
        db_sess.add(CourierHours(courier_id=courier_id, begin=begin, end=end))


def add_order_hours(order, db_sess, order_id):
    """Добавление рабочих часов курьеру"""
    hours = order['delivery_hours']
    for string in hours:
        begin, end = string.split("-")
        begin = datetime.time(hour=int(begin.split(":")[0]), minute=int(begin.split(":")[1]))
        end = datetime.time(hour=int(end.split(":")[0]), minute=int(end.split(":")[1]))
        db_sess.add(OrderHours(order_id=order_id, begin=begin, end=end))
