import unittest
from app import main
import requests


class TestAddCouriers(unittest.TestCase):
    """Тесты добавления нового курьера в базу данных"""

    def test_right(self):
        """Проверяет, правильно ли обрабатывается верный запрос"""
        print("Все тесты надо проходить с полностью пустой базой данных, либо следить, чтобы id в бд не повторялись")
        data = {
            "data": [
                {
                    "courier_id": 1,
                    "courier_type": "foot",
                    "regions": [1, 12, 22],
                    "working_hours": ["11:35-14:05", "09:00-11:00"]
                },
                {
                    "courier_id": 2,
                    "courier_type": "bike",
                    "regions": [22],
                    "working_hours": ["09:00-18:00"]
                }
            ]
        }
        result = requests.post("http://localhost:8080/couriers", json=data).json()
        self.assertEqual(result, {
            "couriers": [{"id": 1}, {"id": 2}]
        })

    def test_empty(self):
        """Проверяет реакцию на пустой json"""
        result = requests.post("http://localhost:8080/couriers").json()
        self.assertEqual(result, {'error': 'Empty request'})

    def test_existing_id(self):
        """Проверяем обработку уже существующего id"""
        data = {"data": [{
            "courier_id": 2,
            "courier_type": "bike",
            "regions": [22],
            "working_hours": ["09:00-18:00"]
        }]}
        result = requests.post("http://localhost:8080/couriers", json=data).json()
        self.assertEqual(result, {'error': 'already existing id'})

    def test_validation_error1(self):
        data = {
            "data": [
                {
                    "courier_id": 10,
                    "regions": [1, 12, 22],
                    "working_hours": ["11:35-14:05", "09:00-11:00"]
                }
            ]
        }
        result = requests.post("http://localhost:8080/couriers", json=data).json()
        self.assertEqual(result, {'validation_error': {
            'couriers': [{'id': 10}]}
        })
