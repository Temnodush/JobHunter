import unittest
from src.vacancy import Vacancy


class TestVacancy(unittest.TestCase):
    def setUp(self):
        self.valid_vacancy = Vacancy(
            name="Python Developer",
            area="Москва",
            url="https://hh.ru/vacancy/123",
            salary_from=100000,
            salary_to=150000,
            description="Разработка на Python",
        )

    def test_creation_valid(self):
        """Тест создания вакансии с валидными данными"""
        self.assertEqual(self.valid_vacancy.name, "Python Developer")
        self.assertEqual(self.valid_vacancy.area, "Москва")
        self.assertEqual(self.valid_vacancy.url, "https://hh.ru/vacancy/123")
        self.assertEqual(self.valid_vacancy.salary_from, 100000)
        self.assertEqual(self.valid_vacancy.salary_to, 150000)
        self.assertEqual(self.valid_vacancy.description, "Разработка на Python")

    def test_validation_errors(self):
        """Тест валидации некорректных данных"""
        with self.assertRaises(ValueError):
            # Отсутствует название
            Vacancy("", "Москва", "https://hh.ru", 100000, 150000, "Описание")

        with self.assertRaises(ValueError):
            # Отсутствует ссылка
            Vacancy("Python", "Москва", "", 100000, 150000, "Описание")

        with self.assertRaises(ValueError):
            # Некорректный тип зарплаты
            Vacancy("Python", "Москва", "https://hh.ru", "100000", 150000, "Описание")

    def test_comparison_methods(self):
        """Тест методов сравнения вакансий"""
        lower_salary = Vacancy(
            "Junior Python",
            "Москва",
            "https://hh.ru/124",
            50000,
            80000,
            "Младший разработчик",
        )
        higher_salary = Vacancy(
            "Senior Python",
            "Москва",
            "https://hh.ru/125",
            200000,
            250000,
            "Старший разработчик",
        )

        # Проверка операторов сравнения
        self.assertTrue(lower_salary < self.valid_vacancy)
        self.assertTrue(higher_salary > self.valid_vacancy)
        self.assertTrue(self.valid_vacancy <= higher_salary)
        self.assertTrue(higher_salary >= self.valid_vacancy)
        self.assertEqual(self.valid_vacancy, self.valid_vacancy)

    def test_to_dict(self):
        """Тест преобразования в словарь"""
        vacancy_dict = self.valid_vacancy.to_dict()
        self.assertEqual(vacancy_dict["name"], "Python Developer")
        self.assertEqual(vacancy_dict["area"], "Москва")
        self.assertEqual(vacancy_dict["url"], "https://hh.ru/vacancy/123")
        self.assertEqual(vacancy_dict["salary_from"], 100000)
        self.assertEqual(vacancy_dict["salary_to"], 150000)
        self.assertEqual(vacancy_dict["description"], "Разработка на Python")

    def test_str_representation(self):
        """Тест строкового представления"""
        vacancy_str = str(self.valid_vacancy)

        # Проверяем основные компоненты вывода
        self.assertIn("Вакансия: Python Developer", vacancy_str)
        self.assertIn("Регион: Москва", vacancy_str)
        self.assertIn("Зарплата: от 100000 до 150000", vacancy_str)
        self.assertIn("Ссылка: https://hh.ru/vacancy/123", vacancy_str)

        # Проверяем описание (первые 100 символов + ...)
        self.assertIn("Описание: Разработка на Python", vacancy_str)

        # Проверяем полный формат вывода
        expected_output = (
            "Вакансия: Python Developer\n"
            "Регион: Москва\n"
            "Зарплата: от 100000 до 150000\n"
            "Описание: Разработка на Python\n"
            "Ссылка: https://hh.ru/vacancy/123\n"
        )
        self.assertEqual(vacancy_str, expected_output)


if __name__ == "__main__":
    unittest.main()
