from currency_service.src.domain.entities.request import RequestModel
from currency_service.src.domain.entities.response import ResponseModel
from currency_service.src.domain.interfaces.usecase import IUseCase


class ChangeBaseCurrency(IUseCase):
    class Request(RequestModel):
        new_base: str
        old_values: dict[str, float]

    class Response(ResponseModel):
        new_values: dict[str, float]

        def __init__(self, new_values: dict[str, float]):
            super().__init__(new_values=new_values)

    def execute(self, request: Request) -> Response:
        new_values = {}
        coefficient = request.old_values.get(request.new_base)
        for currency, value in request.old_values.items():
            new_value = round(value / coefficient, 4)
            new_values[currency] = new_value
        return self.Response(new_values)
