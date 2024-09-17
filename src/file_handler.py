import psycopg2
from psycopg2 import errors


def create_database(
    dbname: str, user: str, password: str, host: str = "localhost"
) -> None:
    """
    Создает базу данных с указанным именем. Если база данных уже существует, пропускает создание.

    :param dbname: Имя базы данных для создания.
    :param user: Имя пользователя для подключения к базе данных PostgreSQL.
    :param password: Пароль пользователя для подключения к базе данных PostgreSQL.
    :param host: Хост базы данных PostgreSQL (по умолчанию "localhost").
    """
    conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host)
    conn.autocommit = True
    cursor = conn.cursor()

    try:
        cursor.execute(f"CREATE DATABASE {dbname}")
    except errors.DuplicateDatabase:
        pass  # База данных уже существует

    conn.close()


def create_tables(
    dbname: str, user: str, password: str, host: str = "localhost"
) -> None:
    """
    Создает таблицы `companies` и `vacancies` в указанной базе данных. Если таблицы уже существуют, они будут удалены
    и созданы заново.

    :param dbname: Имя базы данных, в которой будут созданы таблицы.
    :param user: Имя пользователя для подключения к базе данных PostgreSQL.
    :param password: Пароль пользователя для подключения к базе данных PostgreSQL.
    :param host: Хост базы данных PostgreSQL (по умолчанию "localhost").
    """
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    cursor = conn.cursor()

    # Удаление существующих таблиц
    cursor.execute("DROP TABLE IF EXISTS vacancies;")
    cursor.execute("DROP TABLE IF EXISTS companies;")

    # Создание таблицы компаний
    create_companies_table = """
    CREATE TABLE IF NOT EXISTS companies (
        id SERIAL PRIMARY KEY,
        hh_id INTEGER UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL
    );
    """

    # Создание таблицы вакансий
    create_vacancies_table = """
    CREATE TABLE IF NOT EXISTS vacancies (
        id SERIAL PRIMARY KEY,
        company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
        title VARCHAR(255) NOT NULL,
        salary_min INTEGER,
        salary_max INTEGER,
        salary_currency VARCHAR(10),
        url TEXT NOT NULL UNIQUE
    );
    """

    cursor.execute(create_companies_table)
    cursor.execute(create_vacancies_table)

    conn.commit()
    cursor.close()
    conn.close()
