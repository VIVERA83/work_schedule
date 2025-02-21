from logging import Logger
import psycopg2
import csv

PATH_TO_CSV = str
TABLE_NAME = str


class ExportData:
    """Класс для добавления данных в БД."""

    def __init__(
        self,
        db_name: str,
        db_user: str,
        db_password: str,
        db_host: str,
        db_port: int,
        db_schema: str = "public",
        logger: Logger = Logger,
    ):
        """Конструктор класса.

        :param db_name: Имя БД
        :param db_user: Имя пользователя БД
        :param db_password: Пароль пользователя БД
        :param db_host: Хост БД
        :param db_port: Порт БД
        :param db_schema: Схема БД
        :param logger: Логгер
        """
        self.logger = logger
        self.db_schema = db_schema
        self.conn = psycopg2.connect(
            f"dbname={db_name} "
            f"user={db_user} "
            f"password={db_password} "
            f"host={db_host} "
            f"port={db_port}"
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
                    f"INSERT INTO {self.db_schema}.{table_name} ({columns}) VALUES ({count_columns})",
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
