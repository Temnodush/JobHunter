import unittest
import os
import json
import tempfile

from src.vacancy import Vacancy
from src.data_saver import JSONVacancyStorage


class TestJSONVacancyStorage(unittest.TestCase):
    def setUp(self):
        # Создаем временный файл
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.storage = JSONVacancyStorage(self.temp_file.name)

        # Тестовая вакансия
        self.vacancy = Vacancy(
            name="Python Developer",
            area="Москва",
            url="https://hh.ru/vacancy/123",
            salary_from=100000,
            salary_to=150000,
            description="Разработка на Python"
        )

    def tearDown(self):
        # Удаляем временный файл после тестов
        os.unlink(self.temp_file.name)

    def test_add_vacancy(self):
        """Тест добавления вакансии"""
        # Первое добавление
        self.storage.add_vacancy(self.vacancy)

        with open(self.temp_file.name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["name"], "Python Developer")

        # Попытка добавить дубликат
        self.storage.add_vacancy(self.vacancy)
        with open(self.temp_file.name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertEqual(len(data), 1)  # Дубликат не добавлен

    def test_get_vacancies(self):
        """Тест получения вакансий по критерию"""
        # Добавляем тестовые данные
        self.storage.add_vacancy(self.vacancy)

        # Вакансия с другим описанием
        other_vacancy = Vacancy(
            name="Java Developer",
            area="Москва",
            url="https://hh.ru/vacancy/124",
            salary_from=120000,
            salary_to=180000,
            description="Разработка на Java"
        )
        self.storage.add_vacancy(other_vacancy)

        # Поиск по ключевому слову
        python_vacancies = self.storage.get_vacancies("Python")
        self.assertEqual(len(python_vacancies), 1)
        self.assertEqual(python_vacancies[0].name, "Python Developer")

        # Поиск без ключевого слова
        all_vacancies = self.storage.get_vacancies("")
        self.assertEqual(len(all_vacancies), 2)

    def test_remove_vacancy(self):
        """Тест удаления вакансии"""
        # Добавляем тестовые данные
        self.storage.add_vacancy(self.vacancy)

        # Удаляем вакансию
        self.storage.remove_vacancy("https://hh.ru/vacancy/123")

        with open(self.temp_file.name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertEqual(len(data), 0)

        # Попытка удалить несуществующую вакансию
        self.storage.remove_vacancy("https://hh.ru/vacancy/999")
        with open(self.temp_file.name, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertEqual(len(data), 0)  # Файл остался пустым


if __name__ == "__main__":
    unittest.main()
