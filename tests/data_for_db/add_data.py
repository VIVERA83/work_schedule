from logging import Logger
import psycopg2
import csv
from dotenv import load_dotenv

from core.logger import setup_logging
from core.settings import PostgresSettings

PATH_TO_CSV = str
TABLE_NAME = str


class ExportData:
    """Класс для добавления данных в БД."""

    def __init__(self, pg_settings: PostgresSettings, logger: Logger = Logger):
        """Конструктор класса.

        :param pg_settings: Настройки подключения к БД
        :param logger: Логгер
        """
        self.logger = logger
        self.pg_settings = pg_settings
        self.conn = psycopg2.connect(
            f"dbname={pg_settings.postgres_db} "
            f"user={pg_settings.postgres_user} "
            f"password={pg_settings.postgres_password.get_secret_value()} "
            f"host={pg_settings.postgres_host} "
            f"port={pg_settings.postgres_port}"
        )

    def add_data_to_db_table(self, path_to_csv: str, table_name: str):
        """Функция для добавления данных из csv файла в таблицу БД.

        :param path_to_csv: Путь к csv файлу
        :param table_name: Название таблицы в БД
        :return:
        """
        cur = self.conn.cursor()
        with open(path_to_csv, "r") as f:
            reader = csv.reader(f)
            columns = next(reader)
            count_columns = ",".join(["%s"] * len(columns))
            columns = ",".join(columns)
            for row in reader:
                cur.execute(
                    f"INSERT INTO {self.pg_settings.postgres_schema}.{table_name} ({columns}) VALUES ({count_columns})",
                    row,
                )

        self.conn.commit()

    def add_data_to_db(self, files: list[tuple[PATH_TO_CSV, TABLE_NAME]]):
        """Функция для добавления данных из csv файла в таблицы БД.

        :param files: Список кортежей из пути к файлу и названия таблицы
        :return:
        """

        for path, table in files:
            try:
                self.add_data_to_db_table(path, table)
                self.logger.info(f"Данные из файла {path} добавлены в таблицу {table}")
            except Exception as e:
                self.conn.rollback()
                self.logger.error(
                    f"Ошибка при добавлении данных в таблицу {table} из файла {path}"
                )
                self.logger.error(e)

    def close(self):
        """Закрытие подключения к БД."""

        self.logger.info("Закрытие подключения к БД")
        self.conn.close()


if __name__ == "__main__":
    load_dotenv()
    data = [
        ("data/schedule_types.csv", "schedule_types"),
        ("data/car.csv", "car"),
        ("data/driver.csv", "driver"),
        ("data/crew.csv", "crew"),
        ("data/crew_cars.csv", "crew_cars"),
        ("data/crew_drivers.csv", "crew_drivers"),
        ("data/work_schedule_history.csv", "work_schedule_history"),
        ("data/car_schedule_history.csv", "car_schedule_history"),
    ]
    export_data = ExportData(PostgresSettings(), setup_logging())  # noqa
    export_data.add_data_to_db(data)
