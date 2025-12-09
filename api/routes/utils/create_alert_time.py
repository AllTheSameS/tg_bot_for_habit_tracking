from zoneinfo import ZoneInfo
from typing import Any
import datetime
import pytz


def create_alert_time(alert_time_str, user_timezone) -> datetime.datetime.time:
    try:
        alert_time: Any = datetime.datetime.strptime(alert_time_str, "%H:%M").time()

        user_tz: ZoneInfo = ZoneInfo(user_timezone)
        user_now: datetime = datetime.datetime.now(user_tz)
        user_datetime: Any = user_now.replace(
                hour=alert_time.hour,
                minute=alert_time.minute,
                second=0,
                microsecond=0
            )
        return user_datetime.astimezone(pytz.UTC).time()
    except Exception as e:
        raise ValueError(str(e))