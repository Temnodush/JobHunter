import json
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Any

from src.vacancy import Vacancy


class AbstractVacancyStorage(ABC):
    """Абстрактный класс для работы с хранилищами вакансий"""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансии в хранилище"""
        pass

    @abstractmethod
    def get_vacancies(self, criterion: str) -> List[Vacancy]:
        """Получение вакансий по критерию"""
        pass

    @abstractmethod
    def remove_vacancy(self, vacancy_url: str) -> None:
        """Удаление вакансии из хранилища"""
        pass


class JSONVacancyStorage(AbstractVacancyStorage):
    """Класс для работы с JSON-хранилищем вакансий"""

    def __init__(self, filename: str) -> None:
        self.__filename = filename
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    def __load_vacancies(self) -> List[Dict[str, Any]]:
        """Приватный метод загрузки вакансий из файла"""
        if not os.path.exists(self.__filename):
            return []

        try:
            with open(self.__filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []

    def __save_vacancies(self, data: List[Dict[str, Any]]) -> None:
        """Приватный метод сохранения вакансий в файл"""
        with open(self.__filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансии с проверкой на дубликаты"""
        vacancies = self.__load_vacancies()
        vacancy_dict = vacancy.to_dict()

        # Проверка на дубликаты по URL
        if not any(v["url"] == vacancy.url for v in vacancies):
            vacancies.append(vacancy_dict)
            self.__save_vacancies(vacancies)

    def get_vacancies(self, criterion: str) -> List[Vacancy]:
        """Получение вакансий по ключевому слову в описании"""
        vacancies_data = self.__load_vacancies()
        result = []

        for item in vacancies_data:
            try:
                vacancy = Vacancy(
                    name=item["name"],
                    area=item["area"],
                    url=item["url"],
                    salary_from=item["salary_from"],
                    salary_to=item["salary_to"],
                    description=item["description"],
                )

                if not criterion or criterion.lower() in vacancy.description.lower():
                    result.append(vacancy)
            except (KeyError, ValueError):
                continue

        return result

    def remove_vacancy(self, vacancy_url: str) -> None:
        """Удаление вакансии по URL"""
        vacancies = self.__load_vacancies()
        updated = [v for v in vacancies if v["url"] != vacancy_url]
        self.__save_vacancies(updated)
