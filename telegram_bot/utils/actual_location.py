from telegram_bot.managers.user_api_client import user_api_client
from typing import Dict
from timezonefinder import TimezoneFinder


async def actual_location(latitude, longitude, header) -> str:
    try:
        tf = TimezoneFinder()
        user_timezone: str | None = tf.timezone_at(lat=latitude, lng=longitude)

        if user_timezone:
            response_data: Dict | None = await user_api_client.update_user(
                data={"timezone": str(user_timezone)},
                headers=header,
            )
            if response_data:
                return response_data.json()
            else:
                return "❌ Произошла ошибка при определении часового пояса. Повторите попытку позже."
    except Exception:
        return "❌ Произошла ошибка при определении часового пояса"
