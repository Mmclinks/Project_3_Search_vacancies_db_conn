from typing import List


def output_companies_and_vacancies_count(result: List) -> None:
    for element in result:
        print(f"Название компании: {element[0]}, количество вакансий: {element[1]}")


def output_all_vacancies(result: List) -> None:
    for element in result:
        print(f"Название компании: {element[0]}, вакансия: {element[1]},  зарплата: от {element[2]},  "
              f"до {element[3]},  ссылка на вакансию: {element[4]}")


def output_vacancies_with_higher_salary(result: List) -> None:
    for element in result:
        print(f"Название компании: {element[0]}, вакансия: {element[1]},  зарплата: от {element[2]},  "
              f"до {element[3]},  ссылка на вакансию: {element[4]}")


def output_vacancies_with_keyword(result: List) -> None:
    for element in result:
        print(f"Название компании: {element[0]}, вакансия: {element[1]},  зарплата: от {element[2]},  "
              f"до {element[3]},  ссылка на вакансию: {element[4]}")
