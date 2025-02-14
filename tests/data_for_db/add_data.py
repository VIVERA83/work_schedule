import logging
from logging import Logger

import psycopg2
import csv
from dotenv import load_dotenv

from core.logger import setup_logging
from core.settings import PostgresSettings

load_dotenv()


def add_data_to_db_table(
    path_to_csv: str, table_name: str, conn: psycopg2.extensions.connection
):
    """
    Функция для добавления данных из csv файла в таблицу БД.

    :param path_to_csv: Путь к csv файлу
    :param table_name: Название таблицы в БД
    :param conn: Подключение к БД
    :return:
    """
    cur = conn.cursor()
    with open(path_to_csv, "r") as f:
        reader = csv.reader(f)
        columns = next(reader)
        count_columns = ",".join(["%s"] * len(columns))
        columns = ",".join(columns)
        for row in reader:
            cur.execute(
                f"INSERT INTO {pg_settings.postgres_schema}.{table_name} ({columns}) VALUES ({count_columns})",
                row,
            )

    conn.commit()


def add_data_to_db(
    conn: psycopg2.extensions.connection,
    files: list[tuple[str, str]],
    logger: logging.Logger = Logger,
):
    """Функция для добавления данных из csv файла в таблицы БД.

    :param conn: Подключение к БД
    :param files: Список кортежей из пути к файлу и названия таблицы
    :param logger: Логгер
    :return:
    """

    for path, table in files:
        try:
            add_data_to_db_table(path, table, conn)
            logger.info(f"Данные из файла {path} добавлены в таблицу {table}")
        except Exception as e:
            connection.rollback()
            logger.error(
                f"Ошибка при добавлении данных в таблицу {table} из файла {path}"
            )
            logger.error(e)


if __name__ == "__main__":
    logger = setup_logging()
    pg_settings = PostgresSettings()  # noqa

    connection = psycopg2.connect(
        f"dbname={pg_settings.postgres_db} "
        f"user={pg_settings.postgres_user} "
        f"password={pg_settings.postgres_password.get_secret_value()} "
        f"host={pg_settings.postgres_host} "
        f"port={pg_settings.postgres_port}"
    )
    data = [
        ("data/schedule_types.csv", "schedule_types"),
        ("data/car.csv", "car"),
        ("data/driver.csv", "driver"),
        ("data/crew.csv", "crew"),
        ("data/crew_cars.csv", "crew_cars"),
        ("data/crew_drivers.csv", "crew_drivers"),
    ]
    add_data_to_db(connection, data, logger)
    connection.close()
