from utils.utils import create_db, create_table, insert_data
from classe.db_manager import DBManager
from utils.output_functions import (output_all_vacancies, output_vacancies_with_keyword,
                                    output_companies_and_vacancies_count, output_vacancies_with_higher_salary)


def main() -> None:
    """Основная функция, диалог с пользователем"""
    db_name = "vacancies_db"

    create_db(db_name)
    create_table(db_name)
    insert_data(db_name)

    db_manager = DBManager(db_name)

    print("Привет!\nЭто программа для работы с вакансиями сайта HH.RU\nВыбери, что ты хочешь сделать:")
    print("""1. Посмотреть топ-10 компаний и количество вакансий у них.
2. Посмотреть список 50 вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
3. Получить среднюю зарплату по вакансиям.
4. Посмотреть список всех вакансий, у которых зарплата выше средней по всем вакансиям.
5. Посмотреть список всех вакансий, в названии которых содержится ключевое слово.
0. Увидеть все результаты""")

    result1 = db_manager.get_companies_and_vacancies_count()
    result2 = db_manager.get_all_vacancies()
    result3 = db_manager.get_avg_salary()
    result4 = db_manager.get_vacancies_with_higher_salary()

    while True:
        user_answer = input("Сделай выбор: ")

        if user_answer == "1":
            output_companies_and_vacancies_count(result1)
            break
        elif user_answer == "2":
            output_all_vacancies(result2)
            break
        elif user_answer == "3":
            print(f"Средняя зарплата по вакансиям: {result3}")
            break
        elif user_answer == "4":
            output_vacancies_with_higher_salary(result4)
            break
        elif user_answer == "5":
            keyword = input("Введите запрос для поиска: ")
            result5 = db_manager.get_vacancies_with_keyword(keyword)
            if result5:
                output_vacancies_with_keyword(result5)
            else:
                print(f"По запросу '{keyword}' ничего не найдено.")
            break
        elif user_answer == "0":
            output_companies_and_vacancies_count(result1)
            output_all_vacancies(result2)
            print(f"Средняя зарплата по вакансиям: {result3}")
            output_vacancies_with_higher_salary(result4)
            keyword = input("Введите запрос для поиска: ")
            result5 = db_manager.get_vacancies_with_keyword(keyword)
            if result5:
                output_vacancies_with_keyword(result5)
            else:
                print(f"По запросу '{keyword}' ничего не найдено.")
            break
        else:
            print("Неудачная попытка. Попробуй ещё раз.")


main()
