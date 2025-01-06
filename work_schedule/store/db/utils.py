def validate_schedule_data(is_working: bool, what_day: int, work_days: int, weekend_days: int) -> None:
    if is_working and not (work_days >= what_day > 0):
        raise ValueError(f"Неверное значение параметра {what_day=} в диапазоне от 1 до {work_days=}.")
    elif not (weekend_days >= what_day > 0):
        raise ValueError(f"Неверное значение параметра {what_day=} в диапазоне от 1 до {weekend_days=}.")
