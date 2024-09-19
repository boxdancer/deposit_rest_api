from datetime import datetime
import calendar


def get_next_dates(date_str, periods):
    # Преобразуем строку в объект даты
    date = datetime.strptime(date_str, "%d.%m.%Y")

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
    # print(get_next_dates("13.12.2023", 3))
    test = get_next_dates('31.01.1932', 25)
    print(test)

