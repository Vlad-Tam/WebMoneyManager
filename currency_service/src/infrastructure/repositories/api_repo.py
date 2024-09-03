from datetime import date

import aiohttp

from currency_service.src.infrastructure.config.api_config import APIConfig


class APIRepository:
    api_config = APIConfig()

    @staticmethod
    async def fetch_data(url: str, params: dict):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                data = await response.json()
                return data

    async def get_current_exchange_rates(self) -> dict:
        url = self.api_config.get_api_path() + "latest.json"
        params = {"app_id": self.api_config.get_api_token()}
        response = await self.fetch_data(url, params=params)
        return dict(response)

    async def get_exchange_rates_history(self, request_date: date) -> dict:
        str_date = request_date.strftime('%Y-%m-%d')
        url = f"{self.api_config.get_api_path()}historical/{str_date}.json"
        params = {"app_id": self.api_config.get_api_token()}
        response = await self.fetch_data(url, params=params)
        return dict(response)
