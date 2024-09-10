from datetime import date
from typing import Optional

from currency_service.src.domain.entities.request import RequestModel
from currency_service.src.domain.entities.response import ResponseModel, ResponseSuccess
from currency_service.src.domain.interfaces.usecase import IUseCase
from currency_service.src.infrastructure.config.logging_config import logging_config

logger = logging_config.get_logger()


class ParseParamsFromRMQString(IUseCase):
    class Request(RequestModel):
        params_str: str

    class Response(ResponseModel):
        requested_currencies: Optional[list[str]]
        request_date: str
        base_currency: str

        def __init__(self, requested_currencies: Optional[list[str]], request_date: str,  base_currency: str):
            super().__init__(
                requested_currencies=requested_currencies,
                request_date=request_date,
                base_currency=base_currency
            )

    def execute(self, request: Request) -> Response:
        logger.debug("Method 'parse_params_string' was called")
        parts = request.params_str.split(',')
        request_date = parts[0]
        base_currency = parts[1] if len(parts) > 1 else "USD"
        requested_currencies = parts[2].split(';') if len(parts) > 2 and parts[2] else None
        logger.warning(f"Parse results: {request_date}, {base_currency}, {requested_currencies}")
        logger.debug("Method 'parse_params_string' worked successfully")
        return self.Response(
            request_date=request_date,
            base_currency=base_currency,
            requested_currencies=requested_currencies
        )
