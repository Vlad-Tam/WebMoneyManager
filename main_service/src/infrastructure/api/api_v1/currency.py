import json
import re
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from main_service.src.domain.entities.response import ResponseFailure, ResponseStatus
from main_service.src.domain.usecases.send_currency_history_request import SendCurrencyRequest
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
    # print(type(response.data))
    response.data = response.data.decode('utf-8')
    response.data = json.loads(response.data)
    # response.data = response.data.decode('utf-8')
    # print(type(decoded_data))
    # data_string = decoded_data.replace("=", ":").replace("'", '"')
    # print(1)
    # data_string = re.sub(r'datetime\.date\((\d{4}), (\d{1,2}), (\d{1,2})\)', r'\1-\2-\3', data_string)
    # print(2)
    # data_string = data_string.replace(" ", ", ")
    # print(3)
    # data_dict = f'{{"data": "{data_string}"}}'
    # print(data_dict)
    # json_output = json.loads(data_dict)
    # print(5)
    # formatted_json = json.dumps(json_output, indent=4)
    # print(6)

    if isinstance(response, ResponseFailure):
        raise HTTPException(status_code=response.status_code, detail=response.details)

    logger.info("Endpoint GET '/currency/history' worked successfully")
    return response


def create_params_string(request_date: str, base_currency: str, requested_currencies: Optional[list[str]]) -> str:
    currencies_str = ';'.join(requested_currencies) if requested_currencies else ''
    return f"{request_date},{base_currency},{currencies_str}"
