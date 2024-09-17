from typing import List, Optional, Tuple, Any

import psycopg2


class DBManager:
    def __init__(self, dbname: str, user: str, password: str, host: str = "localhost"):
        self.conn = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host
        )
        self.cursor = self.conn.cursor()

    def insert_company(self, company_id: int, company_name: str) -> None:
        query = """
        INSERT INTO companies (hh_id, name) 
        VALUES (%s, %s)
        ON CONFLICT (hh_id) DO NOTHING;
        """
        self.cursor.execute(query, (company_id, company_name))
        self.conn.commit()

    def insert_vacancy(
            self,
            company_id: int,
            title: str,
            salary_min: Optional[int],
            salary_max: Optional[int],
            salary_currency: str,
            url: str,
    ) -> None:
        """
        Вставляет новую вакансию в базу данных, если она ещё не существует.

        :param company_id: Уникальный идентификатор компании.
        :param title: Название вакансии.
        :param salary_min: Минимальная зарплата для вакансии (может быть None).
        :param salary_max: Максимальная зарплата для вакансии (может быть None).
        :param salary_currency: Валюта зарплаты.
        :param url: URL вакансии.
        """
        # Проверка существования компании
        self.cursor.execute("SELECT id FROM companies WHERE hh_id = %s;", (company_id,))
        company = self.cursor.fetchone()
        if company is None:
            print(f"Компания с ID {company_id} не существует. Пропускаем вакансию.")
            return

        query = """
        INSERT INTO vacancies (company_id, title, salary_min, salary_max, salary_currency, url)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (url) DO NOTHING;
        """
        print(
            f"Inserting vacancy: company_id={company_id}, title={title}, salary_min={salary_min}, salary_max={salary_max}, salary_currency={salary_currency}, url={url}")
        self.cursor.execute(
            query, (company[0], title, salary_min, salary_max, salary_currency, url)
        )
        self.conn.commit()

    def get_companies_and_vacancies_count(self) -> list[tuple[Any, ...]]:
        query = """
            SELECT c.name, COUNT(v.id) AS vacancy_count
            FROM companies c
            LEFT JOIN vacancies v ON c.id = v.company_id
            GROUP BY c.name
        """
        self.cursor.execute(query)
        return (
            self.cursor.fetchall()
        )  # Убедитесь, что возвращаемый тип совпадает с аннотацией

    def get_all_vacancies(
        self,
    ) -> List[Tuple[str, str, Optional[int], Optional[int], str]]:
        query = """
            SELECT c.name AS company_name, v.title, v.salary_min, v.salary_max, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return [(row[0], row[1], row[2], row[3], row[4]) for row in result]

    def get_avg_salary(self) -> Optional[float]:
        """
        Рассчитывает среднюю зарплату по всем вакансиям.

        :return: Средняя зарплата в виде числа с плавающей запятой, или None, если зарплат нет.
        """
        query = """
            SELECT AVG((salary_min + salary_max) / 2.0) AS avg_salary
            FROM vacancies
            WHERE salary_min IS NOT NULL AND salary_max IS NOT NULL
        """
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_vacancies_with_higher_salary(
        self,
    ) -> List[Tuple[str, str, Optional[int], Optional[int], str]]:
        avg_salary = self.get_avg_salary()
        if avg_salary is None:
            return []

        query = """
            SELECT c.name AS company_name, v.title, v.salary_min, v.salary_max, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            WHERE (v.salary_min + v.salary_max) / 2.0 > %s
        """
        self.cursor.execute(query, (avg_salary,))
        result = self.cursor.fetchall()
        return [(row[0], row[1], row[2], row[3], row[4]) for row in result]

    def get_vacancies_with_keyword(
        self, keyword: str
    ) -> List[Tuple[str, str, Optional[int], Optional[int], str]]:
        query = """
            SELECT c.name AS company_name, v.title, v.salary_min, v.salary_max, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            WHERE v.title ILIKE %s
        """
        self.cursor.execute(query, (f"%{keyword}%",))
        result = self.cursor.fetchall()
        return [(row[0], row[1], row[2], row[3], row[4]) for row in result]

    def close(self) -> None:
        """
        Закрывает курсор и соединение с базой данных.
        """
        self.cursor.close()
        self.conn.close()
