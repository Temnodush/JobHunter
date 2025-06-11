import requests
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class JobPlatformAPI(ABC):
    """Абстрактный класс для работы с API сервисов вакансий"""

    @abstractmethod
    def _connect_to_api(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Приватный метод для подключения к API"""
        pass

    @abstractmethod
    def get_vacancies(self, query: str, area_id: int) -> List[Dict[str, Any]]:
        """Абстрактный метод получения вакансий"""
        pass


class HeadHunterAPI(JobPlatformAPI):
    """Класс для работы с API hh.ru"""

    def __init__(self) -> None:
        self.__base_url = "https://api.hh.ru/vacancies"
        self.__areas_url = "https://api.hh.ru/areas"

    def _connect_to_api(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Приватный метод подключения к API hh.ru с проверкой статуса"""
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise ConnectionError(
                f"Ошибка подключения к API hh.ru. Статус: {response.status_code}"
            )
        return response.json()

    def get_area_id(self, region_name: str) -> Optional[int]:
        """Получение ID региона по названию"""
        try:
            areas_data = self._connect_to_api(self.__areas_url, {})
            for country in areas_data:
                for region in country["areas"]:
                    if region["name"].lower() == region_name.lower():
                        return region["id"]
                    for city in region["areas"]:
                        if city["name"].lower() == region_name.lower():
                            return city["id"]
            return None
        except ConnectionError:
            return None

    def get_vacancies(self, query: str, area_id: int) -> List[Dict[str, Any]]:
        """Получение вакансий по запросу и региону"""
        params = {
            "text": query,
            "area": area_id,
            "per_page": 100,
            "only_with_salary": True
        }
        try:
            data = self._connect_to_api(self.__base_url, params)
            return data.get("items", [])
        except ConnectionError:
            return []
