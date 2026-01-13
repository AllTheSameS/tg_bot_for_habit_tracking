import httpx
from typing import Dict
from settings import settings


class HabitAPIClient:
    def __init__(self):
        self.base_url: str = settings.base_url

    async def get_all_habits(self, headers: Dict) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.get(
                f"{self.base_url}/habit/all",
                headers=headers,
            )
            return response

    async def get_habit_by_title(self, title: str, headers: Dict) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.get(
                f"{self.base_url}/habit/title/{title}",
                headers=headers,
            )
            return response

    async def create(self, data: Dict, headers: Dict) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.post(
                f"{settings.base_url}/habit/create",
                json=data,
                headers=headers,
            )
            return response

    async def update_habit(self, title: str, data: Dict, headers: Dict) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.patch(
                f"{self.base_url}/habit/update/{title}",
                json=data,
                headers=headers,
            )
            return response

    async def perform_habit(self, title: str, headers: Dict) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.patch(
                f"{settings.base_url}/habit/perform/{title}",
                headers=headers,
            )
            return response

    async def delete_habit(self, title: str, headers: Dict) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.delete(
                f"{settings.base_url}/habit/remove/{title}",
                headers=headers,
            )
            return response


habit_api_client = HabitAPIClient()