import os
from src.vacancy import Vacancy
from src.api_connector import HeadHunterAPI
from src.data_saver import JSONVacancyStorage


def main() -> None:
    """Основная функция взаимодействия с пользователем"""
    api = HeadHunterAPI()
    path = os.path.join(os.path.dirname(__file__), "data", "vacancies.json")
    storage = JSONVacancyStorage(path)

    region = input("Введите населенный пункт (город, регион и т.п.): ").strip()
    region_id = api.get_area_id(region)

    if not region_id:
        print("Регион не найден. Используется значение по умолчанию (Россия).")
        region_id = 113  # Россия по умолчанию

    while True:
        print("\nМеню:")
        print("1. Поиск вакансий")
        print("2. Получить топ N вакансий по зарплате")
        print("3. Получить вакансии по ключевому слову в описании")
        print("4. Выход")
        choice = input("\nВыберите действие: ").strip()

        if choice == "1":
            query = input("Введите название вакансии: ").strip()
            if not query:
                print("Ошибка: запрос не может быть пустым")
                continue

            vacancies = api.get_vacancies(query, region_id)
            if not vacancies:
                print("По вашему запросу вакансий не найдено.")
                continue

            for item in vacancies:
                salary = item.get("salary", {})
                salary_from = salary.get("from")
                salary_to = salary.get("to")
                requirement = item.get("snippet", {}).get("requirement", "")

                try:
                    vacancy = Vacancy(
                        name=item["name"],
                        area=item["area"]["name"],
                        url=item["alternate_url"],
                        salary_from=salary_from,
                        salary_to=salary_to,
                        description=requirement,
                    )
                    print(vacancy)
                    storage.add_vacancy(vacancy)
                except ValueError as e:
                    print(f"Ошибка обработки вакансии: {e}")

        elif choice == "2":
            top_amount = input("Введите количество вакансий для топа: ").strip()
            if not top_amount.isdigit():
                print("Ошибка: введите целое число")
                continue

            top_amount = int(top_amount)
            if top_amount <= 0:
                print("Ошибка: количество должно быть положительным числом")
                continue

            all_vacancies = storage.get_vacancies("")
            if not all_vacancies:
                print("Нет сохраненных вакансий.")
                continue

            # Сортировка по максимальной зарплате
            sorted_vacancies = sorted(
                all_vacancies,
                key=lambda v: max(
                    v.salary_to if v.salary_to is not None else 0,
                    v.salary_from if v.salary_from is not None else 0,
                ),
                reverse=True,
            )

            # Выводим ровно top_amount вакансий
            for i, vacancy in enumerate(sorted_vacancies[:top_amount], 1):
                print(f"\nВакансия #{i}")
                print(vacancy)

        elif choice == "3":
            keyword = input("Введите ключевое слово для поиска в описании: ").strip()
            if not keyword:
                print("Ошибка: ключевое слово не может быть пустым")
                continue

            vacancies = storage.get_vacancies(keyword)
            if not vacancies:
                print("Вакансий с таким ключевым словом не найдено.")
                continue

            print(f"\nНайдено вакансий: {len(vacancies)}")
            for i, vacancy in enumerate(vacancies, 1):
                print(f"\nВакансия #{i}")
                print(vacancy)

        elif choice == "4":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 4.")


if __name__ == "__main__":
    main()
