from typing import Any, Dict, List

from api_handler import fetch_companies, fetch_vacancies
from db_manager import DBManager
from file_handler import create_database, create_tables


def populate_db(db_manager: DBManager) -> None:
    """
    Заполняет базу данных данными о компаниях и вакансиях.

    :param db_manager: Экземпляр класса DBManager для взаимодействия с базой данных.
    """
    # URL для получения данных о работодателях
    companies_url = "https://api.hh.ru/employers"
    vacancies_url = "https://api.hh.ru/vacancies"

    # Получение данных о работодателях
    companies_data: List[Dict[str, Any]] = fetch_companies(
        companies_url, params={"per_page": 10}
    )

    # Подготовка словаря для хранения вакансий
    vacancies_data: Dict[int, List[Dict[str, Any]]] = {}

    for company in companies_data:
        company_id = company["id"]
        print(f"Fetching vacancies for company ID: {company_id}")
        vacancies: List[Dict[str, Any]] = fetch_vacancies(company_id, vacancies_url)
        vacancies_data[company_id] = vacancies

    # Заполнение базы данных
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
        db_manager.insert_company(company_id, company_name)

    for company_id, vacancies in vacancies_data.items():
        for vacancy in vacancies:
            title = vacancy.get("name")
            salary_min = vacancy.get("salary", {}).get("from")
            salary_max = vacancy.get("salary", {}).get("to")
            salary_currency = vacancy.get("salary", {}).get("currency")
            url = vacancy.get("alternate_url")
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


def main() -> None:
    """
    Основная функция, которая создаёт базу данных, заполняет её данными и отображает информацию.
    """
    dbname = "postgres"
    user = "postgres"
    password = "4Ka7dGnm"

    # Создание базы данных и таблиц
    create_database(dbname, user, password)
    create_tables(dbname, user, password)

    db_manager = DBManager(dbname=dbname, user=user, password=password)

    try:
        populate_db(db_manager)
        user_interface(db_manager)
    finally:
        db_manager.close()


if __name__ == "__main__":
    main()
