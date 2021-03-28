from include.dataBase.order import Order
from include.dataBase.region import Region
from include.dataBase.courier_hours import CourierHours
from include.dataBase.order_hours import OrderHours
from include.dataBase.batch import Batch
from include.dataBase.courier_type import CourierType
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


def return_weight(orders):
    sum_ = 0
    for order in orders:
        sum_ += order.weight
    return sum_


def change_orders(batch, del_list, db_sess):
    """Повторялся кусок кода, лучше его будет сюда вставить"""
    for order in del_list:
        order.batch = None

    orders = db_sess.query(Order).filter(Order.batch == batch.id).filter(Order.completed == 0).all()
    batch.all_weight = return_weight(orders)


def update_orders_after_changing_weight(db_sess, courier):
    """Изменяет заказы курьера после изменения грузоподъемности """
    batch = db_sess.query(Batch).filter(Batch.courier_id == courier.courier_id).filter(
        Batch.finish_time == None).first()
    if not batch:
        return
    orders = db_sess.query(Order).filter(Order.batch == batch.id).filter(Order.completed == 0).all()
    if not orders:
        return
    weight = db_sess.query(CourierType).filter(CourierType.id == courier.courier_type).first().max_weight
    weight_current = batch.all_weight
    if weight_current > weight:
        del_list = []  # список заказов, которых надо убрать
        i = 1
        orders = list(sorted(orders, key=lambda order: order.weight))
        while weight_current > weight and i - 1 != len(orders):
            del_list.append(orders[len(orders) - i])
            weight_current -= del_list[-1].weight
            i += 1
        change_orders(batch, del_list, db_sess)


def update_orders_after_changing_regions(db_sess, courier):
    """Обновляем посылки последней партии, чтобы все подходило по районам"""
    batch = db_sess.query(Batch).filter(Batch.courier_id == courier.courier_id).filter(
        Batch.finish_time == None).first()
    if not batch:
        return
    orders = db_sess.query(Order).filter(Order.batch == batch.id).filter(Order.completed == 0).all()
    if not orders:
        return
    regions = [i.id for i in courier.regions]

    del_list = []  # Список районов, которых надо будет убрать
    for order in orders:
        if order.region_id not in regions:
            del_list.append(order)

    change_orders(batch, del_list, db_sess)


def update_orders_after_changing_working_times_of_courier(db_sess, courier):
    """Обновляем посылки последней партии после изменения времени работы курьера"""
    batch = db_sess.query(Batch).filter(Batch.courier_id == courier.courier_id).filter(
        Batch.finish_time == None).first()
    if not batch:
        return
    orders = db_sess.query(Order).filter(Order.batch == batch.id).filter(Order.completed == 0).all()
    if not orders:
        return
    del_list = []
    courier_times = db_sess.query(CourierHours).filter(CourierHours.courier_id == courier.courier_id).all()

    for order in orders:
        order_times = db_sess.query(OrderHours).filter(OrderHours.order_id == order.id).all()

        if not check_time(courier_times, order_times):
            del_list.append(order)

    change_orders(batch, del_list, db_sess)