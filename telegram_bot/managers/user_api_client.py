import httpx
from typing import Dict
from settings import settings


class UserAPIClient:
    def __init__(self):
        self.base_url: str = settings.base_url

    async def get_user(self, headers: Dict) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.get(
                f"{settings.base_url}/user_info",
                headers=headers,
            )
        return response

    async def update_user(self, data: Dict, headers: Dict) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.patch(
                f"{self.base_url}/me",
                json=data,
                headers=headers,
            )
        return response

    async def auth(self, data: Dict) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.post(
                f"{settings.base_url}/login",
                data=data,
            )
        return response

    async def registration(self, data: Dict) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.post(
                f"{settings.base_url}/registration",
                json=data,
            )
        return response


user_api_client: UserAPIClient = UserAPIClient()