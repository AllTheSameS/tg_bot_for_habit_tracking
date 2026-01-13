from zoneinfo import ZoneInfo
from datetime import datetime, time


def create_alert_time(alert_time_str: str | None, user_timezone: str) -> datetime:
    """Создает datetime в UTC из строки времени и часового пояса пользователя."""
    try:
        if alert_time_str is None:
            return None
        alert_time: time = datetime.strptime(alert_time_str[:5], "%H:%M").time()
        user_tz = ZoneInfo(user_timezone)
        user_now: datetime = datetime.now(user_tz)

        user_datetime: datetime = datetime.combine(
            user_now.date(),
            alert_time,
            tzinfo=user_tz
        )
        return user_datetime.astimezone(ZoneInfo("UTC")).time()
    except ValueError as e:
        raise ValueError(f"Invalid time format: {alert_time_str}. Expected 'HH:MM'")
    except Exception as e:
        raise ValueError(f"Error creating alert time: {str(e)}")