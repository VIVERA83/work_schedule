from dotenv import load_dotenv
from core.logger import setup_logging
from core.settings import PostgresSettings

from test_area.data_for_db.export_data import ExportData

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
    settings = PostgresSettings()  # noqa
    export_data = ExportData(
        settings.postgres_db,
        settings.postgres_user,
        settings.postgres_password.get_secret_value(),
        settings.postgres_host,
        int(settings.postgres_port),
        settings.postgres_schema,
        setup_logging(),
    )
    export_data.add_data_to_db(data)
    export_data.close()