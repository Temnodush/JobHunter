import unittest
from unittest.mock import patch, Mock
from src.api_connector import HeadHunterAPI


class TestHeadHunterAPI(unittest.TestCase):
    def setUp(self):
        self.api = HeadHunterAPI()

    @patch('requests.get')
    def test_get_area_id_success(self, mock_get):
        """Тест успешного получения ID региона"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "areas": [
                    {"name": "Москва", "id": 1, "areas": []},
                    {
                        "name": "Россия",
                        "id": 113,
                        "areas": [
                            {"name": "Санкт-Петербург", "id": 2},
                            {"name": "Новосибирск", "id": 4}
                        ]
                    }
                ]
            }
        ]
        mock_get.return_value = mock_response

        # Поиск существующего региона
        self.assertEqual(self.api.get_area_id("Москва"), 1)
        self.assertEqual(self.api.get_area_id("Санкт-Петербург"), 2)

        # Регион не найден
        self.assertIsNone(self.api.get_area_id("Несуществующий город"))

    @patch('requests.get')
    def test_get_area_id_failure(self, mock_get):
        """Тест ошибки при получении ID региона"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        self.assertIsNone(self.api.get_area_id("Москва"))

    @patch('requests.get')
    def test_get_vacancies_success(self, mock_get):
        """Тест успешного получения вакансий"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "name": "Python Developer",
                    "area": {"name": "Москва"},
                    "alternate_url": "https://hh.ru/vacancy/123",
                    "salary": {"from": 100000, "to": 150000},
                    "snippet": {"requirement": "Опыт работы с Python"}
                }
            ]
        }
        mock_get.return_value = mock_response

        vacancies = self.api.get_vacancies("Python", 1)
        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0]["name"], "Python Developer")

    @patch('requests.get')
    def test_get_vacancies_failure(self, mock_get):
        """Тест ошибки при получении вакансий"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        vacancies = self.api.get_vacancies("Python", 1)
        self.assertEqual(len(vacancies), 0)


if __name__ == "__main__":
    unittest.main()