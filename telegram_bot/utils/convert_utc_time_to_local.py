from datetime import datetime
import pytz
from zoneinfo import ZoneInfo


def convert_utc_time_to_local(alert_time: datetime.time, user_timezone_str: str) -> datetime.time:
    """
    Преобразует время из UTC в локальное время пользователя

    Args:
        alert_time_utc: время в UTC
        user_timezone_str: строковый идентификатор часового пояса

    Returns:
        Локальное время пользователя

    Raises:
        ValueError: если часовой пояс не найден
    """
    if alert_time is None:
        return "Не установлено."
    if isinstance(alert_time, str):
        alert_time = datetime.strptime(alert_time, '%H:%M:%S').time()
    utc_datetime = datetime.combine(datetime.today(), alert_time).replace(tzinfo=pytz.utc)
    local_datetime = utc_datetime.astimezone(ZoneInfo(user_timezone_str))
    return local_datetime.time()