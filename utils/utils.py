import os
import psycopg2
from dotenv import load_dotenv
from classe.hh_parser import HHParser

load_dotenv()

conn_params = {
    "host": os.getenv('host'),
    "database": "postgres",
    "user": os.getenv('user'),
    "password": os.getenv('password'),
    "port": os.getenv('port')
}


def create_db(db_name: str) -> None:
    """Функция для создания БД"""
    conn = psycopg2.connect(**conn_params)

    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")

    cur.close()
    conn.close()


def create_table(db_name: str) -> None:
    """Функция для создания таблиц employer и vacancy"""
    conn = psycopg2.connect(dbname=db_name, user=os.getenv("user"), password=os.getenv("password"),
                            host=os.getenv("host"), port=os.getenv("port"))
    with conn:
        with conn.cursor() as cur:
            cur.execute('''CREATE TABLE employer (
            id INT PRIMARY KEY,
            all_vacancies INT,
            name VARCHAR(255))''')

            cur.execute('''CREATE TABLE vacancy (
            id INT PRIMARY KEY,
            name VARCHAR(255),
            salary_from INT,
            salary_to INT,
            url VARCHAR(255),
            employer_id INT REFERENCES employer(id))''')

    conn.close()


def insert_data(db_name: str) -> None:
    """Функция для заполнения таблиц данными, полученными от АПИ"""
    conn = psycopg2.connect(dbname=db_name, user=os.getenv("user"), password=os.getenv("password"),
                            host=os.getenv("host"), port=os.getenv("port"))
    with conn:
        with conn.cursor() as cur:
            hh = HHParser()
            employers = hh.get_employers()
            for employer in employers:
                employer_id = employer['id']
                cur.execute('INSERT INTO employer VALUES (%s, %s, %s)', (employer['id'],
                                                                         employer['open_vacancies'], employer['name']))
                vacancies = hh.get_vacancies(employer_id)
                for vacancy in vacancies:
                    if not vacancy['salary']:
                        salary_from = 0
                        salary_to = 0
                    else:
                        salary_from = vacancy['salary']['from'] if vacancy['salary']['from'] else 0
                        salary_to = vacancy['salary']['to'] if vacancy['salary']['to'] else 0
                    cur.execute('INSERT INTO vacancy VALUES (%s, %s, %s, %s, %s, %s)',
                                (vacancy['id'], vacancy['name'], salary_from, salary_to,
                                 vacancy['alternate_url'], employer_id))

    conn.close()
