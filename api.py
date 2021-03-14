import flask
from flask import request, jsonify, make_response
from include import db_session
from include.dataBase.courier import Courier
from include.dataBase.courier_type import CourierType
# from include.dataBase.courier_region import CourierRegion
from include.dataBase.region import Region
from include.dataBase.courier_hours import CourierHours
import datetime

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


def add_courier_regions(person, db_sess, courier_id):
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
        db_sess.commit()


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

                courier_type = db_sess.query(CourierType).filter(CourierType.name == person['courier_type']).first().id

                db_sess.add(Courier(courier_id=person['courier_id'],
                                    courier_type=courier_type,
                                    rating=0,
                                    earnings=0))  # добавляем курьера в базу данных
                add_courier_regions(person, db_sess, person['courier_id'])

                courier = db_sess.query(Courier).filter(Courier.courier_id == person['courier_id']).first()
                courier.regions = person['regions']


                add_courier_hours(person, db_sess, person['courier_id'])
                db_sess.commit()
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
    return make_response(jsonify({
        "couriers": good
    }), "201 Created")


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
            db_sess.commit()
        # if 'regions' in data:
        #     courier.regions = data['regions']
        #     db_sess.commit()
        if 'working_hours' in data:
            db_sess.query(CourierHours).filter(CourierHours.courier_id == courier_id).delete()
            add_courier_hours(data, db_sess, courier_id)
            db_sess.commit()


        hours = db_sess.query(CourierHours).filter(CourierHours.courier_id == courier_id).all()
        hours = ["-".join(
            [":".join([str(i.begin.hour), str(i.begin.minute)]), ":".join([str(i.end.hour), str(i.end.minute)])]) for i
            in
            hours]
        return make_response(jsonify({"courier_id": courier_id,
                                      "courier_type": db_sess.query(CourierType).filter(
                                          CourierType.id == courier.courier_type).first().name,
                                      "regions": courier.regions,
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
                   ['courier_id', 'courier_type', 'regions', 'working_hours']):
            pass
