from typing import Optional, Union

from fastapi import APIRouter, Query, HTTPException

from currency_service.src.domain.entities.response import ResponseStatus, ResponseFailure
from currency_service.src.domain.usecases.get_current_exchange_rate import GetCurrentExchangeRate
from currency_service.src.domain.usecases.get_exchange_rate_history import GetExchangeRateHistory
from currency_service.src.domain.validators.get_exchange_rates_validator import GetExchangeRatesValidator
from currency_service.src.domain.validators.get_history_validator import GetHistoryValidator
from currency_service.src.infrastructure.config.logging_config import LoggingConfig

router = APIRouter(
    prefix="/currency",
    tags=["Currency"],
)

logger = LoggingConfig().get_logger()


@router.get("/exchange_rates")
async def get_exchange_rates(base_currency: str = "USD",
                             requested_currencies: Optional[list[str]] = Query(default=None, min_length=1)
                             ):
    logger.debug("Endpoint GET '/currency/exchange_rates' was called")
    try:
        request = GetExchangeRatesValidator(base_currency=base_currency,
                                            requested_currencies=requested_currencies
                                            )
    except ValueError as e:
        logger.error(f"Endpoint GET '/currency/exchange_rates' raised an exception \"{e}\"")
        raise HTTPException(status_code=ResponseStatus.BAD_REQUEST.status_code,
                            detail=ResponseStatus.BAD_REQUEST.status_msg
                            )
    response = await GetCurrentExchangeRate().execute(GetCurrentExchangeRate.Request(
        base_currency=request.base_currency, requested_currencies=request.requested_currencies)
    )

    if isinstance(response, ResponseFailure):
        raise HTTPException(status_code=response.status_code, detail=response.details)

    logger.info("Endpoint GET '/currency/exchange_rates' worked successfully")
    return response


@router.get("/history")
async def get_history(request_date: str,
                      base_currency: str = "USD",
                      requested_currencies: Optional[list[str]] = Query(default=None, min_length=1)
                      ):
    logger.debug("Endpoint GET '/currency/history' was called")
    try:
        request = GetHistoryValidator(base_currency=base_currency,
                                      requested_currencies=requested_currencies,
                                      request_date=request_date)
    except ValueError as e:
        logger.error(f"Endpoint GET '/currency/history' raised an exception \"{e}\"")
        raise HTTPException(status_code=ResponseStatus.BAD_REQUEST.status_code,
                            detail=ResponseStatus.BAD_REQUEST.status_msg
                            )
    response = await GetExchangeRateHistory().execute(GetExchangeRateHistory.Request(
        base_currency=request.base_currency,
        request_date=request.request_date,
        requested_currencies=requested_currencies
    ))

    if isinstance(response, ResponseFailure):
        raise HTTPException(status_code=response.status_code, detail=response.details)

    logger.info("Endpoint GET '/currency/history' worked successfully")
    return response
