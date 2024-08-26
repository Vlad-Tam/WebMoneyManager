from datetime import date

from currency_service.src.domain.entities.exchange_rate import AddExchangeRateDTO
from currency_service.src.domain.entities.request import RequestModel
from currency_service.src.domain.entities.response import ResponseModel
from currency_service.src.domain.interfaces.usecase import IUseCase


class ParseAPIResponseToDTO(IUseCase):
    class Request(RequestModel):
        data_from_api: dict
        request_date: date

    class Response(ResponseModel):
        exchange_rate_dto: AddExchangeRateDTO

        def __init__(self, exchange_rate_dto: AddExchangeRateDTO):
            super().__init__(exchange_rate_dto=exchange_rate_dto)

    def execute(self, request: Request) -> Response:
        data_dict = request.data_from_api
        exchange_rate_dto = AddExchangeRateDTO(
            base_currency=data_dict["base"],
            request_date=request.request_date,
            rates=data_dict["rates"]
        )
        return self.Response(exchange_rate_dto=exchange_rate_dto)
