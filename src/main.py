import configparser
import os
from typing import Any, Dict, List

from src.api_handler import fetch_companies, fetch_vacancies
from src.db_manager import DBManager
from src.file_handler import create_database, create_tables


def populate_db(db_manager: DBManager) -> None:
    """
    Загружает данные о компаниях и вакансиях с API hh.ru и сохраняет их в базу данных.

    Аргументы:
        db_manager (DBManager): Экземпляр класса для управления базой данных.

    Описание:
        1. Извлекает данные о компаниях с API hh.ru с помощью функции `fetch_companies`,
        ограничивая результат 10 компаниями.
        2. Для каждой компании запрашивает список вакансий, связанных с ней, с помощью функции `fetch_vacancies`.
        3. Все вакансии группируются по ID компании и сохраняются в словаре `vacancies_data`.
        4. Затем данные о компаниях и их вакансиях передаются в функцию `load_data_to_db`,
        которая сохраняет их в базе данных.

    Исключения:
        В случае ошибок при запросах к API или работе с базой данных функция поднимет соответствующие исключения.
    """
    companies_url = "https://api.hh.ru/employers"
    vacancies_url = "https://api.hh.ru/vacancies"

    companies_data: List[Dict[str, Any]] = fetch_companies(
        companies_url, params={"per_page": 10}
    )
    vacancies_data: Dict[int, List[Dict[str, Any]]] = {}

    for company in companies_data:
        company_id = company["id"]
        print(f"Fetching vacancies for company ID: {company_id}")
        vacancies: List[Dict[str, Any]] = fetch_vacancies(company_id, vacancies_url)
        vacancies_data[company_id] = vacancies

    load_data_to_db(db_manager, companies_data, vacancies_data)


def load_data_to_db(
    db_manager: DBManager,
    companies_data: List[Dict[str, Any]],
    vacancies_data: Dict[int, List[Dict[str, Any]]],
) -> None:
    """
    Загружает данные о компаниях и вакансиях в базу данных.

    :param db_manager: Экземпляр класса DBManager для взаимодействия с базой данных.
    :param companies_data: Список словарей с данными о компаниях.
    :param vacancies_data: Словарь с данными о вакансиях, где ключ - ID компании.
    """
    for company in companies_data:
        company_id = company["id"]
        company_name = company["name"]
        db_manager.insert_or_update_company(company_id, company_name)

    for company_id, vacancies in vacancies_data.items():
        for vacancy in vacancies:
            title = vacancy.get("name", "")
            salary_min = vacancy.get("salary", {}).get("from")
            salary_max = vacancy.get("salary", {}).get("to")
            salary_currency = vacancy.get("salary", {}).get("currency", "")
            url = vacancy.get("alternate_url", "")
            db_manager.insert_vacancy(
                company_id, title, salary_min, salary_max, salary_currency, url
            )


def user_interface(db_manager: DBManager) -> None:
    """
    Отображает информацию о компаниях, вакансиях и средней зарплате.

    :param db_manager: Экземпляр класса DBManager для взаимодействия с базой данных.
    """
    print("Companies and Vacancy Count:")
    print(db_manager.get_companies_and_vacancies_count())

    print("\nAll Vacancies:")
    print(db_manager.get_all_vacancies())

    print("\nAverage Salary:")
    print(db_manager.get_avg_salary())

    print("\nVacancies with Higher Salary:")
    print(db_manager.get_vacancies_with_higher_salary())

    keyword = "python"
    print(f"\nVacancies with Keyword '{keyword}':")
    print(db_manager.get_vacancies_with_keyword(keyword))


def get_db_config() -> dict:
    """
    Получает параметры подключения к базе данных из файла config.ini
    :return: словарь с параметрами подключения
    """
    # Получаем абсолютный путь к текущему файлу и строим путь к config.ini
    config_path = os.path.join(os.path.dirname(__file__), "config.ini")

    config = configparser.ConfigParser()
    config.read(config_path)

    db_config = {
        "dbname": config.get("database", "dbname"),
        "user": config.get("database", "user"),
        "password": config.get("database", "password"),
        "host": config.get("database", "host"),
    }

    return db_config


def main() -> None:
    """
    Основная функция, которая создаёт базу данных, заполняет её данными и отображает информацию.
    """
    # Получение данных из конфигурационного файла
    db_config = get_db_config()

    # Создание базы данных и таблиц
    create_database(db_config["dbname"], db_config["user"], db_config["password"])
    create_tables(db_config["dbname"], db_config["user"], db_config["password"])

    # Подключение к базе данных
    db_manager = DBManager(**db_config)

    try:
        populate_db(db_manager)
        user_interface(db_manager)
    finally:
        db_manager.close()


if __name__ == "__main__":
    main()
