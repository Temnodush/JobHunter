from typing import Optional, Dict, Any


class Vacancy:
    """Класс для представления и работы с вакансиями"""

    __slots__ = ("name", "area", "url", "salary_from", "salary_to", "description")

    def __init__(
            self,
            name: str,
            area: str,
            url: str,
            salary_from: Optional[int],
            salary_to: Optional[int],
            description: str
    ) -> None:
        self.name = name
        self.area = area
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.description = description or ""
        self._validate()

    def _validate(self) -> None:
        """Приватный метод валидации данных вакансии"""
        if not self.name or not self.url:
            raise ValueError("Название и ссылка на вакансию обязательны")

        if self.salary_from is not None and not isinstance(self.salary_from, int):
            raise ValueError("Зарплата 'от' должна быть целым числом")

        if self.salary_to is not None and not isinstance(self.salary_to, int):
            raise ValueError("Зарплата 'до' должна быть целым числом")

    def __str__(self) -> str:
        salary_info = []
        if self.salary_from is not None:
            salary_info.append(f"от {self.salary_from}")
        if self.salary_to is not None:
            salary_info.append(f"до {self.salary_to}")

        salary_str = "Зарплата: " + " ".join(salary_info) if salary_info else "Зарплата не указана"

        return (
            f"Вакансия: {self.name}\n"
            f"Регион: {self.area}\n"
            f"{salary_str}\n"
            f"Описание: {self.description[:100]}{'...' if len(self.description) > 100 else ''}\n"
            f"Ссылка: {self.url}\n"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return False
        return self.url == other.url

    def __lt__(self, other: "Vacancy") -> bool:
        self_max = self.salary_to or self.salary_from or 0
        other_max = other.salary_to or other.salary_from or 0
        return self_max < other_max

    def __le__(self, other: "Vacancy") -> bool:
        return self < other or self == other

    def __gt__(self, other: "Vacancy") -> bool:
        return not self <= other

    def __ge__(self, other: "Vacancy") -> bool:
        return not self < other

    def to_dict(self) -> Dict[str, Any]:
        """Возвращает словарь с данными вакансии"""
        return {
            "name": self.name,
            "area": self.area,
            "url": self.url,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "description": self.description
        }