import psycopg2
from psycopg2 import errors


def create_database(
    dbname: str, user: str, password: str, host: str = "localhost"
) -> None:
    """
    Создаёт базу данных с указанным именем, если она ещё не существует.

    :param dbname: Имя базы данных, которую нужно создать.
    :param user: Имя пользователя для подключения к базе данных.
    :param password: Пароль для подключения к базе данных.
    :param host: Хост, на котором работает сервер базы данных (по умолчанию 'localhost').
    """
    conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host)
    conn.autocommit = True
    cursor = conn.cursor()

    try:
        cursor.execute(f"CREATE DATABASE {dbname}")
    except errors.DuplicateDatabase:
        # База данных уже существует
        pass

    conn.close()


def create_tables(
    dbname: str, user: str, password: str, host: str = "localhost"
) -> None:
    """
    Создаёт таблицы в указанной базе данных, если они ещё не существуют.

    :param dbname: Имя базы данных, в которой нужно создать таблицы.
    :param user: Имя пользователя для подключения к базе данных.
    :param password: Пароль для подключения к базе данных.
    :param host: Хост, на котором работает сервер базы данных (по умолчанию 'localhost').
    """
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)

    cursor = conn.cursor()

    create_companies_table = """
    CREATE TABLE IF NOT EXISTS companies (
        id SERIAL PRIMARY KEY,
        hh_id INTEGER UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL
    );
    """

    create_vacancies_table = """
    CREATE TABLE IF NOT EXISTS vacancies (
        id SERIAL PRIMARY KEY,
        company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
        title VARCHAR(255) NOT NULL,
        salary_min INTEGER,
        salary_max INTEGER,
        salary_currency VARCHAR(10),
        url TEXT NOT NULL
    );
    """

    cursor.execute(create_companies_table)
    cursor.execute(create_vacancies_table)

    conn.commit()
    cursor.close()
    conn.close()
