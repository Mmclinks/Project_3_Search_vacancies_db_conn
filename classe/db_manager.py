import os
import psycopg2
from dotenv import load_dotenv
from typing import List

load_dotenv()


class DBManager:
    """Класс для подключния к БД, в котором реализованы различные выборки данных"""
    def __init__(self, db_name: str) -> None:
        """Инициализатор класса"""
        self.__db_name = db_name

    def __execute_query(self, query: str) -> List:
        """Метод, в котором выполняется подключение к БД и выполнение передаваемого в метод запроса"""
        conn = psycopg2.connect(dbname=self.__db_name, user=os.getenv("user"), password=os.getenv("password"),
                                host=os.getenv("host"), port=os.getenv("port"))

        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        conn.close()
        return result

    def get_companies_and_vacancies_count(self) -> List:
        """Метод, который получает список всех компаний и количество вакансий у каждой компании."""
        query = '''
        SELECT employer.name, employer.all_vacancies
        FROM employer

        GROUP BY employer.name, employer.all_vacancies
        ORDER BY employer.all_vacancies DESC;
        '''
        return self.__execute_query(query)

    def get_all_vacancies(self) -> List:
        """Метод, который  получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        query = '''
        SELECT employer.name AS company, vacancy.name AS vacancy, 
               vacancy.salary_from, vacancy.salary_to, vacancy.url
        FROM vacancy
        JOIN employer ON vacancy.employer_id = employer.id;
        '''
        return self.__execute_query(query)

    def get_avg_salary(self) -> int:
        """Метод, который получает среднюю зарплату по вакансиям."""
        query = '''
        SELECT AVG((salary_from + salary_to) / 2) AS average_salary
        FROM vacancy
        WHERE salary_from > 0 OR salary_to > 0;
        '''
        result = self.__execute_query(query)
        average_salary = int(round(result[0][0]))
        return average_salary

    def get_vacancies_with_higher_salary(self) -> List:
        """Метод, который получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        query = '''
        SELECT employer.name AS company, vacancy.name AS vacancy, 
               vacancy.salary_from, vacancy.salary_to, vacancy.url
        FROM vacancy
        JOIN employer ON vacancy.employer_id = employer.id
        WHERE (salary_from + salary_to) / 2 > (
            SELECT AVG((salary_from + salary_to) / 2)
            FROM vacancy
            WHERE salary_from > 0 OR salary_to > 0
        );
        '''
        return self.__execute_query(query)


    def get_vacancies_with_keyword(self, keyword: str) -> List:
        """Метод, который получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        query = f'''
        SELECT employer.name AS company, vacancy.name AS vacancy, 
               vacancy.salary_from, vacancy.salary_to, vacancy.url
        FROM vacancy
        JOIN employer ON vacancy.employer_id = employer.id
        WHERE vacancy.name LIKE '%{keyword}%';
        '''
        return self.__execute_query(query)
