import flask
from flask import request, jsonify, make_response
from include import db_session
from include.dataBase.courier import Courier

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


# @blueprint.route('/couriers', methods=['POST'])
# def add_courier():
#     """Добавление курьера"""
#     if not request.json:
#         """В случае отсутствия параметров"""
#         return make_response(jsonify({'error': 'Empty request'}), 400)
#     db_sess = db_session.create_session()
#     bad = []
#     good = []  # для правильно заполненных курьеров
#     for person in request.json['data']:
#         """Проверка на наличие всех ключей"""
#         if not all(key in request.json for key in
#                    ['courier_id', 'courier_type', 'regions', 'working_hours']):
#
#             try:
#                 """Добавление курьера в базу данных"""
#                 courier = Courier(courier_id=person['courier_id'],
#                                   courier_type=person['courier_type'],
#                                   regions=";".join(map(str, person['regions'])),
#                                   working_hours=";".join(person['working_hours'])
#                                   )
#                 db_sess.add(courier)
#                 db_sess.commit()
#                 good.append({"id": person['courier_id']})
#             except Exception as e:
#                 """В случае непредвиденной ошибки"""
#                 bad.append({"id": person['courier_id']})
#         else:
#             """При неудачном запросе"""
#             bad.append({"id": person['courier_id']})
#
#     if bad:
#         """При наличии неудачных запросов"""
#
#         return make_response(jsonify({
#             f"validation_error": {
#                 "couriers": bad
#             }}), 400)
#     return make_response(jsonify({
#         "couriers": good
#     }), "201 Created")
#
#
