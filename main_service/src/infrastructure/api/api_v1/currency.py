import json
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from main_service.src.domain.entities.response import ResponseFailure, ResponseStatus
from main_service.src.domain.usecases.send_currency_history_request import SendCurrencyRequest
from main_service.src.domain.validators.get_exchange_rates_validator import GetExchangeRatesValidator
from main_service.src.domain.validators.get_history_validator import GetHistoryValidator
from main_service.src.infrastructure.config.logging_config import LoggingConfig

router = APIRouter(
    prefix="/currency",
    tags=["Currency"],
)

logger = LoggingConfig().get_logger()


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

    request_data = create_params_string(request.request_date, request.base_currency, request.requested_currencies)
    response = (await SendCurrencyRequest().execute(SendCurrencyRequest.Request(request_data=request_data))).response
    response.data = response.data.decode('utf-8')
    if str(response.data).startswith("ResponseFailure"):
        raise HTTPException(
            status_code=ResponseStatus.INTERNAL_ERROR.status_code,
            detail=ResponseStatus.INTERNAL_ERROR.status_msg
        )
    else:
        response.data = json.loads(response.data)

    if isinstance(response, ResponseFailure):
        raise HTTPException(status_code=response.status_code, detail=response.details)

    logger.info("Endpoint GET '/currency/history' worked successfully")
    return response


@router.get("/exchange_rates")
async def get_exchange_rates(
        base_currency: str = "USD",
        requested_currencies: Optional[list[str]] = Query(default=None, min_length=1)
):
    logger.debug("Endpoint GET '/currency/exchange_rates' was called")
    try:
        request = GetExchangeRatesValidator(
            base_currency=base_currency,
            requested_currencies=requested_currencies
        )
    except ValueError as e:
        logger.error(f"Endpoint GET '/currency/exchange_rates' raised an exception \"{e}\"")
        raise HTTPException(
            status_code=ResponseStatus.BAD_REQUEST.status_code,
            detail=ResponseStatus.BAD_REQUEST.status_msg
        )
    request_data = create_params_string("latest", request.base_currency, request.requested_currencies)
    response = (await SendCurrencyRequest().execute(SendCurrencyRequest.Request(request_data=request_data))).response
    response.data = response.data.decode('utf-8')
    if str(response.data).startswith("ResponseFailure"):
        raise HTTPException(
            status_code=ResponseStatus.INTERNAL_ERROR.status_code,
            detail=ResponseStatus.INTERNAL_ERROR.status_msg
        )
    else:
        response.data = json.loads(response.data)

    if isinstance(response, ResponseFailure):
        raise HTTPException(status_code=response.status_code, detail=response.details)

    logger.info("Endpoint GET '/currency/exchange_rates' worked successfully")
    return response


def create_params_string(request_date: str, base_currency: str, requested_currencies: Optional[list[str]]) -> str:
    currencies_str = ';'.join(requested_currencies) if requested_currencies else ''
    return f"{request_date},{base_currency},{currencies_str}"
