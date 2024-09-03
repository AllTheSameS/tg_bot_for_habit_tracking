async def true_time(time: str | None) -> str | None:
    """Функция преобразования времени
    для корректного вывода пользователю."""

    try:

        time = time[:5]

    except TypeError:
        return None

    else:
        return time
