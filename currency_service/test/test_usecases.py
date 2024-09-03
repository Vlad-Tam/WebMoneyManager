import datetime
from datetime import date

import pytest

from currency_service.src.domain.entities.exchange_rate import ExchangeRateDTO
from currency_service.src.domain.entities.response import ResponseStatus, ResponseFailure, ResponseSuccess
from currency_service.src.domain.usecases.change_base_currency import ChangeBaseCurrency
from currency_service.src.domain.usecases.get_current_exchange_rate import GetCurrentExchangeRate
from currency_service.src.domain.usecases.get_exchange_rate_history import GetExchangeRateHistory
from currency_service.src.domain.usecases.parse_api_response_to_dto import ParseAPIResponseToDTO


def test_parse_api_response_to_dto():
    parser = ParseAPIResponseToDTO()
    request_data = {
        "base": "USD",
        "rates": {
            "EUR": 0.85,
            "RUB": 75.0,
        }
    }
    request_date = date(2024, 9, 1)
    request = ParseAPIResponseToDTO.Request(data_from_api=request_data, request_date=request_date)
    response = parser.execute(request)
    assert response.exchange_rate_dto.base_currency == "USD"
    assert response.exchange_rate_dto.request_date == request_date
    assert response.exchange_rate_dto.rates == {
        "EUR": 0.85,
        "RUB": 75.0,
    }


def test_execute():
    change_base_currency = ChangeBaseCurrency()
    request_data = {
        "new_base": "EUR",
        "old_values": {
            "USD": 100.0,
            "EUR": 85.0,
            "RUB": 7500.0,
        }
    }
    request = ChangeBaseCurrency.Request(new_base=request_data["new_base"], old_values=request_data["old_values"])
    response = change_base_currency.execute(request)
    expected_new_values = {
        "USD": round(100.0 / 85.0, 4),
        "EUR": round(85.0 / 85.0, 4),
        "RUB": round(7500.0 / 85.0, 4),
    }
    assert response.new_values == expected_new_values


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "use_case_class", [GetCurrentExchangeRate, GetExchangeRateHistory]
)
async def test_get_current_exchange_rate_from_db_success(monkeypatch, use_case_class):
    self_ = use_case_class()

    async def mock_get_exchange_rate_by_date(date):
        return ExchangeRateDTO(
            base_currency='USD',
            request_date=datetime.date(2024, 9, 1),
            rates={
                "BYN": 3.6729,
                "RUB": 70.2681,
                "EUR": 89.467815
            },
            id=1
        )

    async def mock_get_current_exchange_rates():
        return {'rates': {"BYN": 3.6729, "RUB": 70.2681, "EUR": 89.467815}}

    async def mock_insert_exchange_rate(dto):
        pass

    monkeypatch.setattr(self_.db_repository, 'get_exchange_rate_by_date', mock_get_exchange_rate_by_date)
    monkeypatch.setattr(self_.api_repository, 'get_current_exchange_rates', mock_get_current_exchange_rates)
    monkeypatch.setattr(self_.db_repository, 'insert_exchange_rate', mock_insert_exchange_rate)

    if isinstance(self_, GetExchangeRateHistory):
        request = self_.Request(
            base_currency="USD",
            requested_currencies=["BYN", "RUB", "EUR"],
            request_date="2024-09-01"
        )
    else:
        request = self_.Request(
            base_currency="USD",
            requested_currencies=["BYN", "RUB", "EUR"]
        )
    response = await self_.execute(request)

    assert isinstance(response.response, ResponseSuccess)
    assert response.response.data.rates == {"BYN": 3.6729, "RUB": 70.2681, "EUR": 89.467815}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "use_case_class", [GetCurrentExchangeRate, GetExchangeRateHistory]
)
async def test_get_current_exchange_rate_from_api_with_different_base_success(monkeypatch, use_case_class):
    self_ = use_case_class()

    async def mock_get_exchange_rate_by_date(date):
        return None

    async def mock_get_current_exchange_rates():
        return {'base_currency': 'USD', 'rates': {'EUR': 0.85, 'RUB': 75.0}}

    async def mock_insert_exchange_rate(dto):
        return None

    def mock_change_base_currency(req):
        return ChangeBaseCurrency().Response(new_values={'EUR': 1, 'RUB': 2})

    def mock_parse_to_dto(req):
        return ParseAPIResponseToDTO().Response(exchange_rate_dto=ExchangeRateDTO(
            base_currency='USD',
            request_date=datetime.date(2024, 9, 1),
            rates={
                'EUR': 0.85, 'RUB': 75.0
            },
            id=1
        ))

    monkeypatch.setattr(self_.db_repository, 'get_exchange_rate_by_date', mock_get_exchange_rate_by_date)
    monkeypatch.setattr(self_.api_repository, 'get_current_exchange_rates', mock_get_current_exchange_rates)
    monkeypatch.setattr(self_.db_repository, 'insert_exchange_rate', mock_insert_exchange_rate)
    monkeypatch.setattr(self_.currency_base_changer, 'execute', mock_change_base_currency)
    monkeypatch.setattr(self_.api_parser, 'execute', mock_parse_to_dto)

    if isinstance(self_, GetExchangeRateHistory):
        request = self_.Request(
            base_currency="EUR",
            requested_currencies=["RUB", "EUR"],
            request_date="2024-09-01"
        )
    else:
        request = self_.Request(
            base_currency="EUR",
            requested_currencies=["RUB", "EUR"]
        )
    response = await self_.execute(request)
    assert isinstance(response.response, ResponseSuccess)
    assert response.response.data.rates == {'EUR': 1, 'RUB': 2}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "use_case_class", [GetCurrentExchangeRate, GetExchangeRateHistory]
)
async def test_get_current_exchange_rate_currency_not_found(monkeypatch, use_case_class):
    self_ = use_case_class()

    async def mock_get_exchange_rate_by_date(date):
        return ExchangeRateDTO(
            base_currency='USD',
            request_date=datetime.date(2024, 9, 1),
            rates={
                "RUB": 70.2681,
                "EUR": 89.467815
            },
            id=1
        )

    monkeypatch.setattr(self_.db_repository, 'get_exchange_rate_by_date', mock_get_exchange_rate_by_date)

    if isinstance(self_, GetExchangeRateHistory):
        request = self_.Request(
            base_currency="usd",
            requested_currencies=["BYN"],
            request_date="2024-09-01"
        )
    else:
        request = self_.Request(
            base_currency="usd",
            requested_currencies=["BYN"]
        )
    response = await self_.execute(request)

    assert isinstance(response.response, ResponseFailure)
    assert response.response.status_code == ResponseStatus.NOT_FOUND.status_code
    assert "Currency is not found" in response.response.details
