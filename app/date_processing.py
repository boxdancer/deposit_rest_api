import calendar
import re
from datetime import datetime


def validate_date_string(date_string: str) -> bool:
    # регулярка для проверки формата передаваемой даты
    pattern = r"^\d{2}\.\d{2}\.\d{4}$"
    if re.match(pattern, date_string):
        date_string = date_string.split('.')
        if len(date_string) == 3 and (1 <= int(date_string[0]) <= 31) and (1 <= int(date_string[1]) <= 12) and (
                1000 <= int(date_string[2]) <= 9999):
            return True
    return False


def get_next_dates(date: datetime, periods: int) -> list[str]:
    # Список для хранения результатов
    dates = [date]

    for i in range(1, periods):
        year = date.year
        month = date.month + i

        # Если месяц больше 12, увеличиваем год и уменьшаем месяц
        while month > 12:
            month -= 12
            year += 1

        # Получаем последний день месяца
        last_day_of_month = calendar.monthrange(year, month)[1]

        # Если в месяце нет исходного дня, берём последний день месяца
        day = min(date.day, last_day_of_month)

        # Создаем новую дату
        new_date = datetime(year, month, day)
        dates.append(new_date)

    # Преобразуем даты обратно в строку и возвращаем список
    return [d.strftime("%d.%m.%Y") for d in dates]


if __name__ == '__main__':
    # Пример использования
    test = get_next_dates(datetime(2022, 1, 31), 6)
    print(test)
