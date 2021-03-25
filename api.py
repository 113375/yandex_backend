import flask
from flask import request, jsonify, make_response

from func import add_region, add_courier_hours, check_time, add_order_hours
from include import db_session
from include.dataBase.courier import Courier
from include.dataBase.courier_type import CourierType
from include.dataBase.region import Region
from include.dataBase.courier_hours import CourierHours
from include.dataBase.order_hours import OrderHours
from include.dataBase.order import Order
from include.dataBase.batch import Batch
import datetime

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/couriers', methods=['POST'])
def add_courier():
    """Добавление курьера"""
    if not request.json:
        """В случае отсутствия параметров"""
        return make_response(jsonify({'error': 'Empty request'}), 400)
    db_sess = db_session.create_session()
    bad = []
    good = []  # для правильно заполненных курьеров
    for person in request.json['data']:
        """Проверка на наличие всех ключей"""
        if not all(key in request.json for key in
                   ['courier_id', 'courier_type', 'regions', 'working_hours']):
            try:
                """Добавление курьера в базу данных"""
                if db_sess.query(Courier).filter(Courier.courier_id == person['courier_id']).first():
                    """Если id уже существует"""
                    return make_response(jsonify({'error': 'already existing id'}), 400)

                courier_type = db_sess.query(CourierType).filter(CourierType.name == person['courier_type']).first().id

                db_sess.add(Courier(courier_id=person['courier_id'],
                                    courier_type=courier_type,
                                    rating=0,
                                    earnings=0))  # добавляем курьера в базу данных
                add_region(person, db_sess)

                """__________Добавление районов в базу данных_________"""

                courier = db_sess.query(Courier).filter(Courier.courier_id == person['courier_id']).first()
                for i in person['regions']:
                    region = db_sess.query(Region).filter(Region.name == i).first()

                    courier.regions.append(region)

                add_courier_hours(person, db_sess, person['courier_id'])
                good.append({"id": person['courier_id']})
            except Exception as e:
                """В случае непредвиденной ошибки"""
                bad.append({"id": person['courier_id']})

        else:
            """При неудачном запросе"""
            bad.append({"id": person['courier_id']})

    if bad:
        """При наличии неудачных запросов"""

        return make_response(jsonify({
            f"validation_error": {
                "couriers": bad
            }}), 400)
    db_sess.commit()
    return make_response(jsonify({
        "couriers": good
    }), 201)


@blueprint.route('/couriers/<courier_id>', methods=['PATCH'])
def change_courier(courier_id):
    """Обновление информации о курьере"""
    if not request.json:
        """В случае отсутствия параметров"""
        return make_response(jsonify({'error': 'Empty request'}), 400)

    data = request.json
    db_sess = db_session.create_session()
    if not db_sess.query(Courier).filter(Courier.courier_id == courier_id).first():
        """В случае отсутствия курьера с таким id"""
        return make_response(jsonify({'error': 'Non-existent courier'}), 400)

    if any(key in data for key in ['courier_type', 'regions', 'working_hours']):

        courier = db_sess.query(Courier).filter(Courier.courier_id == courier_id).first()
        if 'courier_type' in data:
            courier.courier_type = db_sess.query(CourierType).filter(
                CourierType.name == data['courier_type']).first().id
        if 'regions' in data:
            regions = courier.regions.copy()
            for j in regions:
                """Удалям старые районы"""
                courier.regions.remove(j)

            for i in data['regions']:
                """Заменяем на новые"""
                add_region(data, db_sess)
                region = db_sess.query(Region).filter(Region.name == i).first()
                courier.regions.append(region)
        if 'working_hours' in data:
            db_sess.query(CourierHours).filter(CourierHours.courier_id == courier_id).delete()
            add_courier_hours(data, db_sess, courier_id)

        hours = db_sess.query(CourierHours).filter(CourierHours.courier_id == courier_id).all()
        hours = ["-".join(
            [":".join([str(i.begin.hour), str(i.begin.minute)]), ":".join([str(i.end.hour),
                                                                           str(i.end.minute)])]) for i in hours]
        db_sess.commit()
        return make_response(jsonify({"courier_id": courier_id,
                                      "courier_type": db_sess.query(CourierType).filter(
                                          CourierType.id == courier.courier_type).first().name,
                                      "regions": [i.name for i in courier.regions],
                                      "working_hours": hours}), 200)
    else:
        return make_response(jsonify({'error': 'Empty request'}), 400)


@blueprint.route('/orders', methods=['POST'])
def add_orders():
    """Добавление заказа"""
    if not request.json:
        """В случае отсутствия параметров"""
        return make_response(jsonify({'error': 'Empty request'}), 400)
    db_sess = db_session.create_session()
    bad = []
    good = []  # для правильно заполненных посылок
    for order in request.json['data']:
        """Проверка на наличие всех ключей"""
        if not all(key in request.json for key in
                   ['order_id', 'weight', 'region', 'delivery_hours']):
            try:
                """Создание заказа"""
                if not db_sess.query(Region).filter(Region.name == order['region']).first():
                    """Если нет района, то добавляем его """
                    db_sess.add(Region(name=order['region']))
                    db_sess.commit()
                if db_sess.query(Order).filter(Order.id == order['order_id']).first():
                    """Если id уже существует"""
                    return make_response(jsonify({'error': 'already existing id'}), 400)
                db_sess.add(Order(id=order['order_id'],
                                  weight=order['weight'],
                                  region_id=db_sess.query(Region).filter(Region.name == order['region']).first().id,
                                  completed=False
                                  ))
                add_order_hours(order, db_sess, order['order_id'])
                good.append({"id": order['order_id']})
            except Exception as e:
                """При непредвиденной ошибке"""
                bad.append({"id": order['order_id']})

        else:
            """При неудачном запросе"""
            bad.append({"id": order['order_id']})

    if bad:
        """При наличии неудачных запросов"""

        return make_response(jsonify({
            f"validation_error": {
                "orders": bad
            }}), 400)
    db_sess.commit()
    return make_response(jsonify({
        "orders": good
    }), 201)


@blueprint.route('/orders/assign', methods=['POST'])
def assign_orders():
    if not request.json:
        """В случае отсутствия параметров"""
        return make_response(jsonify({'error': 'Empty request'}), 400)

    db_sess = db_session.create_session()
    data = request.json
    if "courier_id" in request.json and not db_sess.query(Courier).filter(
            Courier.courier_id == data['courier_id']).first():
        """Проверка на наличие нужного курьера в базе данных"""
        return make_response(jsonify({'error': 'Non-existent courier'}), 400)

    """Отбираем все незанятые и незавершенные заказы"""

    orders = db_sess.query(Order).filter(Order.completed == 0).filter(Order.batch == None).all()

    """Курьер"""
    courier = db_sess.query(Courier).filter(Courier.courier_id == data['courier_id']).first()

    """Время доставки курьером"""
    courier_times = db_sess.query(CourierHours).filter(CourierHours.courier_id == courier.courier_id).all()

    """все регионы курьера"""
    courier_regions = [i.id for i in courier.regions]  # список id районов доставки этого курьера

    """Максимальные вес всех заказов"""
    max_weight = db_sess.query(CourierType).filter(CourierType.id == courier.courier_type).first().max_weight

    chosen_orders = []
    weight = 0

    if db_sess.query(Batch).filter(Batch.courier_id == courier.courier_id).first():
        weight = db_sess.query(Batch).filter(Batch.courier_id == courier.courier_id).first().all_weight

    for order in orders:
        times = db_sess.query(OrderHours).filter(OrderHours.order_id == order.id).all()
        if check_time(courier_times,
                      times) and order.region_id in courier_regions and weight + order.weight <= max_weight:
            chosen_orders.append(order)
            weight += order.weight

    if not db_sess.query(Batch).filter(Batch.courier_id == courier.courier_id).first():
        db_sess.add(Batch(courier_id=courier.courier_id, assign_time=datetime.datetime.now(), all_weight=weight))
    batch = db_sess.query(Batch).filter(Batch.courier_id == courier.courier_id).first()
    for order in chosen_orders:
        """Добавляем id доставки к заказу"""
        order.batch = batch.id
    db_sess.commit()
    chosen_orders_ids = []
    for order in db_sess.query(Order).filter(Order.batch == batch.id).filter(Order.completed == 0).all():
        chosen_orders_ids.append({"id": order.id})
    if not chosen_orders_ids:
        return make_response(jsonify({
            "orders": chosen_orders_ids,
        }))
    return make_response(jsonify({
        "orders": chosen_orders_ids,
        "assign_time": batch.assign_time
    }))
