from datetime import date
from unittest.mock import AsyncMock

import pytest

from currency_service.src.infrastructure.repositories.api_repo import APIRepository


@pytest.mark.asyncio
async def test_get_current_exchange_rates(monkeypatch):
    api_repo = APIRepository()

    async def mock_fetch_data(url: str, params: dict):
        return {
            'base_currency': 'USD',
            'rates': {'EUR': 0.85, 'RUB': 75.0}
        }

    monkeypatch.setattr(api_repo, "fetch_data", AsyncMock(side_effect=mock_fetch_data))
    result = await api_repo.get_current_exchange_rates()
    assert result['base_currency'] == 'USD'
    assert result['rates']['EUR'] == 0.85
    assert result['rates']['RUB'] == 75.0


@pytest.mark.asyncio
async def test_get_exchange_rates_history(monkeypatch):
    api_repo = APIRepository()
    request_date = date(2021, 9, 1)

    async def mock_fetch_data(url: str, params: dict):
        return {
            'date': '2024-09-01',
            'base_currency': 'USD',
            'rates': {'EUR': 0.85, 'RUB': 75.0}
        }

    monkeypatch.setattr(api_repo, "fetch_data", AsyncMock(side_effect=mock_fetch_data))
    result = await api_repo.get_exchange_rates_history(request_date)
    assert result['date'] == '2024-09-01'
    assert result['base_currency'] == 'USD'
    assert result['rates']['EUR'] == 0.85
    assert result['rates']['RUB'] == 75.0
