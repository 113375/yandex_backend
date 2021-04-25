import unittest
import requests

testing_id1 = 100  # Если не проходят тесты,
# то возможно из-за повторяющихся id, а изменить их можно в этих двух переменных
testing_id2 = 101


class TestAddCouriers(unittest.TestCase):
    """Тесты добавления нового курьера в базу данных
        Перед началом тестирования надо запустить программу
    """

    def test_right(self):
        """Проверяет, правильно ли обрабатывается верный запрос"""
        print("Все тесты надо проходить с полностью пустой базой данных, либо следить, чтобы id в бд не повторялись")
        data = {
            "data": [
                {
                    "courier_id": testing_id1,
                    "courier_type": "foot",
                    "regions": [1, 12, 22],
                    "working_hours": ["11:35-14:05", "09:00-11:00"]
                },
                {
                    "courier_id": testing_id2,
                    "courier_type": "bike",
                    "regions": [22],
                    "working_hours": ["09:00-18:00"]
                }
            ]
        }
        result = requests.post("http://localhost:8080/couriers", json=data).json()
        self.assertEqual(result, {
            "couriers": [{"id": testing_id1}, {"id": testing_id2}]
        })

    def test_empty(self):
        """Проверяет реакцию на пустой json"""
        result = requests.post("http://localhost:8080/couriers").json()
        self.assertEqual(result, {'error': 'Empty request'})

    def test_existing_id(self):
        """Проверяем обработку уже существующего id"""
        data = {"data": [{
            "courier_id": testing_id2,
            "courier_type": "bike",
            "regions": [22],
            "working_hours": ["09:00-18:00"]
        }]}
        result = requests.post("http://localhost:8080/couriers", json=data).json()
        self.assertEqual(result, {'error': 'already existing id'})

    def test_validation_error1(self):
        """Проверяет правильность данных и присутствуют ли все поля"""
        data = {
            "data": [
                {
                    "courier_id": testing_id2,
                    "regions": [1, 12, 22],
                    "working_hours": ["11:35-14:05", "09:00-11:00"]
                }
            ]
        }
        result = requests.post("http://localhost:8080/couriers", json=data).json()
        self.assertEqual(result, {'validation_error': {
            'couriers': [{'id': testing_id2}]}
        })

    def test_patch_courier(self):

        """Тут должно все корректно измениться"""
        data = {
            "regions": [11, 33, 2]
        }
        result = requests.patch(f"http://localhost:8080/couriers/{testing_id1}", json=data).json()
        self.assertEqual(result, {'courier_id': '100', 'courier_type': 'foot', 'regions': ['11', '33', '2'],
                                  'working_hours': ['11:35-14:5', '9:0-11:0']})

    def test_patch_wrong(self):
        """Несуществующий id"""
        data = {
            "regions": [11, 33, 2]
        }
        result = requests.patch(f"http://localhost:8080/couriers/{testing_id1 - 10}", json=data).json()
        self.assertEqual(result, {'error': 'Non-existent courier'})
