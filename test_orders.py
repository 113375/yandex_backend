import unittest
from app import main
import requests

order_id1 = 100
order_id2 = 101


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
                    "order_id": order_id1,
                    "weight": 0.23,
                    "region": 12,
                    "delivery_hours": ["09:00-18:00"]
                }
            ]
        }
        result = requests.post("http://localhost:8080/orders", json=data).json()
        self.assertEqual(result, {
            "couriers": [{"id": order_id1}]
        })

    def test_empty(self):
        """Проверяет реакцию на пустой json"""
        result = requests.post("http://localhost:8080/orders").json()
        self.assertEqual(result, {'error': 'Empty request'})

    def test_validation_error(self):
        data = {
            "data": [
                {
                    "order_id": order_id1,
                    "weight": 0.23,
                    "delivery_hours": ["09:00-18:00"]
                }
            ]
        }
        result = requests.post("http://localhost:8080/orders", json=data).json()
        self.assertEqual(result, {
            'validation_error': {'orders': [{'id': 100}]}
        })

    def test_existing_id(self):
        data = {
            "data": [
                {
                    "order_id": order_id1,
                    "weight": 0.23,
                    "region": 12,
                    "delivery_hours": ["09:00-18:00"]
                }
            ]
        }
        result = requests.post("http://localhost:8080/orders", json=data).json()
        self.assertEqual(result, {'error': 'already existing id'})


