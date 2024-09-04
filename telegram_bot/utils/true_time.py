async def true_time(time: str | None) -> str | None:
    """Функция преобразования времени
    для корректного вывода пользователю."""

    try:

        time = time[11:-4]

    except TypeError:
        return None

    else:
        return time
