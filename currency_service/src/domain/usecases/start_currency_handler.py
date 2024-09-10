# import asyncio
# from typing import Union, Optional
#
# from aio_pika import connect, IncomingMessage, DeliveryMode, Message
#
# from currency_service.src.domain.entities.request import RequestModel
# from currency_service.src.domain.entities.response import ResponseModel, ResponseSuccess, ResponseFailure, \
#     ResponseStatus
# from currency_service.src.domain.interfaces.usecase import IUseCase
# from currency_service.src.domain.usecases.get_exchange_rate_history import GetExchangeRateHistory
# from currency_service.src.infrastructure.config.logging_config import LoggingConfig
#
#
# class StartCurrencyHandler(IUseCase):
#
#     def __init__(self):
#         self.logger = LoggingConfig().get_logger()
#
#     class Request(RequestModel):
#         pass
#
#     class Response(ResponseModel):
#         response: Union[ResponseSuccess, ResponseFailure]
#
#         class Config:
#             arbitrary_types_allowed = True
#
#         def __init__(self, response: Union[ResponseSuccess, ResponseFailure]):
#             super().__init__(response=response)
#
#     async def execute(self, request: Request) -> Response:
#         connection = await connect(RMQ_URL)
#         async with connection:
#             channel = await connection.channel()
#             await channel.set_qos(prefetch_count=1)
#             queue = await channel.declare_queue(RMQ_QUEUE_NAME)
#             await queue.consume(self.on_request)
#             await asyncio.Future()
#         return self.Response(ResponseSuccess(data="", status=ResponseStatus.SUCCESS))
#
#     async def on_request(self, message: IncomingMessage) -> None:
#         async with message.process():
#             request_data = message.body.decode()
#             self.logger.info(f"Received request: {request_data}")
#
#             try:
#                 if request_data == "Test history request":
#                     self.logger.error("FOUND")
#                     response_data = (await GetExchangeRateHistory().execute(GetExchangeRateHistory.Request(
#                         base_currency="USD",
#                         request_date="2024-09-01",
#                     ))).response
#                 elif request_data == "now":
#                     self.logger.error("FOUND")
#                     pass
#                 else:
#                     self.logger.error("FOUND")
#                     raise ValueError()
#                 response = ResponseSuccess(data=response_data, status=ResponseStatus.SUCCESS)
#             except ValueError:
#                 response = ResponseFailure(status=ResponseStatus.INTERNAL_ERROR, details="Invalid input")
#
#             await message.channel.default_exchange.publish(
#                 Message(
#                     body=response.json().encode(),
#                     delivery_mode=DeliveryMode.PERSISTENT,
#                 ),
#                 routing_key=message.reply_to
#             )
#             self.logger.info(f"Sent response: {response.json()}")
