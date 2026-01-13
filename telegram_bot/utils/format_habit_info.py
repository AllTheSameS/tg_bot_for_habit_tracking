from typing import Dict, Any
from telegram_bot.utils.convert_utc_time_to_local import convert_utc_time_to_local

def format_habit_info(habit_data: Dict, user_timezone) -> str:
    """Форматирование информации о привычке."""
    alert_time_str: Any = habit_data["habits_tracking"][0]["alert_time"]
    user_alert_time_display = convert_utc_time_to_local(alert_time_str, user_timezone)
    return (
        f"Название: {habit_data['title']}\n"
        f"Описание: {habit_data['description']}\n"
        f"Время оповещения: {user_alert_time_display}\n"
        f"Осталось дней: {habit_data['habits_tracking'][0]['count']}"
    )