import psycopg2
from psycopg2 import errors

def create_database(
    dbname: str, user: str, password: str, host: str = "localhost"
) -> None:
    conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host)
    conn.autocommit = True
    cursor = conn.cursor()

    try:
        cursor.execute(f"CREATE DATABASE {dbname}")
    except errors.DuplicateDatabase:
        pass

    conn.close()

def create_tables(
    dbname: str, user: str, password: str, host: str = "localhost"
) -> None:
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS vacancies;")
    cursor.execute("DROP TABLE IF EXISTS companies;")

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
        url TEXT NOT NULL UNIQUE
    );
    """

    cursor.execute(create_companies_table)
    cursor.execute(create_vacancies_table)

    conn.commit()
    cursor.close()
    conn.close()
