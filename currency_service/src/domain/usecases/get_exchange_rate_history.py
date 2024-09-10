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
        self.logger.critical(f"1")
        request_date = date.fromisoformat(request.request_date)
        requested_base_currency = request.base_currency.upper()
        self.logger.critical(f"2")
        try:
            result_dto = await self.db_repository.get_exchange_rate_by_date(request_date)
            self.logger.critical(f"3")
            if result_dto is None:
                api_result_dict = await self.api_repository.get_exchange_rates_history(request_date)
                self.logger.critical(f"3.1")
                result_dto = self.api_parser.execute(self.api_parser.Request(data_from_api=api_result_dict,
                                                                             request_date=request_date
                                                                             )).exchange_rate_dto
                self.logger.critical(f"4")
                await self.db_repository.insert_exchange_rate(result_dto)
                self.logger.critical(f"5")
        except Exception as e:
            self.logger.critical(f"6")
            self.logger.error(f"Class '{self.__class__.__name__}' raised an exception \"{e}\"")
            return self.Response(ResponseFailure(status=ResponseStatus.NOT_FOUND, details="Getting result error"))

        try:
            self.logger.critical(f"7")
            if requested_base_currency != self.BASE_CURRENCY:
                self.logger.critical(f"8")
                result_dto.rates = self.currency_base_changer.execute(
                    self.currency_base_changer.Request(new_base=requested_base_currency,
                                                       old_values=result_dto.rates
                                                       )).new_values
                result_dto.base_currency = requested_base_currency
                self.logger.critical(f"9")

            if request.requested_currencies is not None:
                self.logger.critical(f"10")
                selected_rates = {}
                for currency in request.requested_currencies:
                    selected_rates[currency.upper()] = result_dto.rates[currency.upper()]
                result_dto.rates = selected_rates
            self.logger.critical(f"11")
        except KeyError as e:
            self.logger.critical(f"12")
            self.logger.error(f"Class '{self.__class__.__name__}' raised an exception \"{e}\"")
            return self.Response(ResponseFailure(status=ResponseStatus.NOT_FOUND, details="Currency is not found"))
        except Exception as e:
            self.logger.critical(f"13")
            self.logger.error(f"Class '{self.__class__.__name__}' raised an exception \"{e}\"")
            return self.Response(ResponseFailure(status=ResponseStatus.INTERNAL_ERROR, details="Processing result error"))
        self.logger.critical(f"14")
        self.logger.info(f"Method '{self.__class__.__name__}.execute' worked successfully")
        return self.Response(ResponseSuccess(data=result_dto, status=ResponseStatus.SUCCESS))

