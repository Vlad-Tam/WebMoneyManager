import pytest
from httpx import AsyncClient

from currency_service.src.domain.entities.response import ResponseFailure, ResponseSuccess, ResponseStatus
from currency_service.src.domain.usecases.get_current_exchange_rate import GetCurrentExchangeRate
from currency_service.src.domain.usecases.get_exchange_rate_history import GetExchangeRateHistory


@pytest.mark.parametrize(
    "base_currency, requested_currencies, expected_response", [
        ("EUR", ["EUR", "RUB"], {"data": {"EUR": 1, "RUB": 0.85}, "status": 200}),
        ("EUR", ["RUB"], {"data": {"RUB": 0.85}, "status": 200}),
        ("VALIDATE_CHECK", ["EUR"], {"detail": "Invalid request"}),
        ("INV", ["EUR"], {"detail": "Invalid base currency"}),
    ]
)
async def test_get_exchange_rates_api(
        ac: AsyncClient,
        monkeypatch,
        base_currency,
        requested_currencies,
        expected_response
):

    async def mock_execute(self_, request):
        if request.base_currency == "INV":
            return GetCurrentExchangeRate.Response(
                ResponseFailure(
                    status=ResponseStatus.NOT_FOUND,
                    details="Invalid base currency"
                )
            )
        return GetCurrentExchangeRate.Response(
            ResponseSuccess(
                status=ResponseStatus.SUCCESS,
                data={currency: (1.0 if currency == request.base_currency else 0.85) for currency in
                      request.requested_currencies
                      }
                )
        )

    monkeypatch.setattr(GetCurrentExchangeRate, "execute", mock_execute)

    response = await ac.get("/exchange_rates", params={
        "base_currency": base_currency,
        "requested_currencies": requested_currencies
    })

    assert response.json() == expected_response


@pytest.mark.parametrize(
    "base_currency, requested_currencies, expected_response", [
        ("EUR", ["EUR", "RUB"], {"data": {"EUR": 1, "RUB": 0.85}, "status": 200}),
        ("EUR", ["RUB"], {"data": {"RUB": 0.85}, "status": 200}),
        ("VALIDATE_CHECK", ["EUR"], {"detail": "Invalid request"}),
        ("INV", ["EUR"], {"detail": "Invalid base currency"}),
    ]
)
async def test_get_history_api(
        ac: AsyncClient,
        monkeypatch,
        base_currency,
        requested_currencies,
        expected_response
):

    async def mock_execute(self_, request):
        if request.base_currency == "INV":
            return GetExchangeRateHistory.Response(
                ResponseFailure(
                    status=ResponseStatus.NOT_FOUND,
                    details="Invalid base currency"
                )
            )
        return GetExchangeRateHistory.Response(
            ResponseSuccess(
                status=ResponseStatus.SUCCESS,
                data={currency: (1.0 if currency == request.base_currency else 0.85) for currency in
                      request.requested_currencies
                      }
                )
        )

    monkeypatch.setattr(GetExchangeRateHistory, "execute", mock_execute)

    response = await ac.get("/history", params={
        "base_currency": base_currency,
        "requested_currencies": requested_currencies,
        "request_date": "2024-09-01"
    })

    assert response.json() == expected_response
