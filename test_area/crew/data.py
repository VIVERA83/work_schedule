import datetime

from api.worker_schedule.schemes import CrewSchema

crew = {
    "cars": [
        {
            "id": 1,
            "model": "TGL",
            "name": "MAN",
            "number": "О196МР196",
            "schedules": [
                {
                    "is_working": True,
                    "schedule_start_date": datetime.datetime(2025, 1, 1, 0, 0),
                    "weekend_days": 2,
                    "what_day": 1,
                    "work_days": 4,
                }
            ],
        },
        {
            "id": 2,
            "model": "C7H",
            "name": "SITRAK",
            "number": "А012КС198",
            "schedules": [
                {
                    "is_working": True,
                    "schedule_start_date": datetime.datetime(2025, 1, 1, 0, 0),
                    "weekend_days": 2,
                    "what_day": 3,
                    "work_days": 4,
                }
            ],
        },
    ],
    "drivers": [
        {
            "id": 1,
            "name": "Смирнов Василий Викторович",
            "schedules": [
                {
                    "is_working": True,
                    "schedule_start_date": datetime.datetime(2025, 1, 1, 0, 0),
                    "weekend_days": 2,
                    "what_day": 1,
                    "work_days": 4,
                }
            ],
        },
        {
            "id": 2,
            "name": "Петров Инокентий Петрович",
            "schedules": [
                {
                    "is_working": True,
                    "schedule_start_date": datetime.datetime(2025, 1, 1, 0, 0),
                    "weekend_days": 2,
                    "what_day": 3,
                    "work_days": 4,
                }
            ],
        },
        {
            "id": 3,
            "name": "Веселовский Александр Михайлович",
            "schedules": [
                {
                    "is_working": False,
                    "schedule_start_date": datetime.datetime(2025, 1, 1, 0, 0),
                    "weekend_days": 2,
                    "what_day": 1,
                    "work_days": 4,
                }
            ],
        },
    ],
    "id": 1,
}

crew_schema = CrewSchema(**crew)
