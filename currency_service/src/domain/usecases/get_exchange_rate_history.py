from datetime import date
from typing import Union, Optional

from currency_service.src.domain.entities.request import RequestModel
from currency_service.src.domain.entities.response import ResponseSuccess, ResponseStatus, \
    ResponseFailure, ResponseModel
from currency_service.src.domain.interfaces.usecase import IUseCase
from currency_service.src.domain.usecases.change_base_currency import ChangeBaseCurrency
from currency_service.src.domain.usecases.parse_api_response_to_dto import ParseAPIResponseToDTO
from currency_service.src.infrastructure.config.logging_config import LoggingConfig
from currency_service.src.infrastructure.repositories.api_repo import APIRepository
from currency_service.src.infrastructure.repositories.db_repo import database_repository
from currency_service.src.infrastructure.repositories.exchange_rate_repo import ExchangeRateRepository


class GetExchangeRateHistory(IUseCase):

    def __init__(self):
        self.db_repository = ExchangeRateRepository(database_repository)
        self.api_repository = APIRepository()
        self.currency_base_changer = ChangeBaseCurrency()
        self.api_parser = ParseAPIResponseToDTO()
        self.BASE_CURRENCY = "USD"
        self.logger = LoggingConfig().get_logger()

    class Request(RequestModel):
        base_currency: str
        request_date: str
        requested_currencies: Optional[list[str]]

    class Response(ResponseModel):
        response: Union[ResponseSuccess, ResponseFailure]

        class Config:
            arbitrary_types_allowed = True

        def __init__(self, response: Union[ResponseSuccess, ResponseFailure]):
            super().__init__(response=response)

    async def execute(self, request: Request) -> Response:
        self.logger.debug(f"Method '{self.__class__.__name__}.execute' was called")
        request_date = date.fromisoformat(request.request_date)
        requested_base_currency = request.base_currency.upper()
        try:
            result_dto = await self.db_repository.get_exchange_rate_by_date(request_date)
            if result_dto is None:
                api_result_dict = await self.api_repository.get_exchange_rates_history(request_date)
                result_dto = self.api_parser.execute(self.api_parser.Request(data_from_api=api_result_dict,
                                                                             request_date=request_date
                                                                             )).exchange_rate_dto
                await self.db_repository.insert_exchange_rate(result_dto)
        except Exception as e:
            self.logger.error(f"Class '{self.__class__.__name__}' raised an exception \"{e}\"")
            return self.Response(ResponseFailure(status=ResponseStatus.NOT_FOUND, details="Getting result error"))

        try:
            if requested_base_currency != self.BASE_CURRENCY:
                result_dto.rates = self.currency_base_changer.execute(
                    self.currency_base_changer.Request(new_base=requested_base_currency,
                                                       old_values=result_dto.rates
                                                       )).new_values
                result_dto.base_currency = requested_base_currency

            if request.requested_currencies is not None:
                selected_rates = {}
                for currency in request.requested_currencies:
                    selected_rates[currency.upper()] = result_dto.rates[currency.upper()]
                result_dto.rates = selected_rates
        except KeyError as e:
            self.logger.error(f"Class '{self.__class__.__name__}' raised an exception \"{e}\"")
            return self.Response(ResponseFailure(status=ResponseStatus.NOT_FOUND, details="Currency is not found"))
        except Exception as e:
            self.logger.error(f"Class '{self.__class__.__name__}' raised an exception \"{e}\"")
            return self.Response(ResponseFailure(status=ResponseStatus.INTERNAL_ERROR, details="Processing result error"))
        self.logger.info(f"Method '{self.__class__.__name__}.execute' worked successfully")
        return self.Response(ResponseSuccess(data=result_dto, status=ResponseStatus.SUCCESS))

