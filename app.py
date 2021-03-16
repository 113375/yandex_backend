from flask import Flask
from waitress import serve

from api import blueprint
from include import db_session
from include.dataBase.courier_type import CourierType

app = Flask(__name__)


def add_types():
    """Автоматическое добавление типов курьера"""
    db_sess = db_session.create_session()
    data = {"foot": 10, "bike": 15, "car": 50}
    if not db_sess.query(CourierType).first():
        for i in data.keys():
            if not CourierType(name=i, max_weight=data[i]) in db_sess:
                db_sess.add(CourierType(name=i, max_weight=data[i]))
                db_sess.commit()


@app.route("/")
def index():
    return "<p>проверка</p>"


def main():
    db_session.global_init("db/data.db")
    app.register_blueprint(blueprint)
    add_types()
    # app.run(port=8080)
    serve(app, port=8080)


if __name__ == '__main__':
    main()
