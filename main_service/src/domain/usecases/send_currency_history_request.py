from typing import Union

from main_service.src.domain.entities.request import RequestModel
from main_service.src.domain.entities.response import ResponseSuccess, ResponseFailure, ResponseModel, ResponseStatus
from main_service.src.domain.interfaces.usecase import IUseCase
from main_service.src.infrastructure.config.logging_config import logging_config
from main_service.src.infrastructure.repositories.rmq_rpc_client_repo import RPCClientRepo


class SendCurrencyRequest(IUseCase):

    def __init__(self):
        self.logger = logging_config.get_logger()

    class Request(RequestModel):
        request_data: str

    class Response(ResponseModel):
        response: Union[ResponseSuccess, ResponseFailure]

        class Config:
            arbitrary_types_allowed = True

        def __init__(self, response: Union[ResponseSuccess, ResponseFailure]):
            super().__init__(response=response)

    async def execute(self, request: Request):
        self.logger.debug(f"Method '{self.__class__.__name__}.execute' was called")

        rpc_client = RPCClientRepo()
        response = await rpc_client.call(request.request_data)
        if response == "timeout":
            self.logger.error(f"Method '{self.__class__.__name__}.call' raised an exception (timeout)")
            self.Response(ResponseFailure(status=ResponseStatus.INTERNAL_ERROR, details=response))

        self.logger.debug(f"Method '{self.__class__.__name__}.execute' was called")
        return self.Response(ResponseSuccess(data=response, status=ResponseStatus.SUCCESS))
