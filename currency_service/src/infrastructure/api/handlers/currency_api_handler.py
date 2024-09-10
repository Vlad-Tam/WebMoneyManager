import asyncio

import pika

from currency_service.src.domain.entities.response import ResponseFailure, ResponseSuccess
from currency_service.src.domain.usecases.get_current_exchange_rate import GetCurrentExchangeRate
from currency_service.src.domain.usecases.get_exchange_rate_history import GetExchangeRateHistory
from currency_service.src.domain.usecases.parse_params_from_rmq_string import ParseParamsFromRMQString
from currency_service.src.infrastructure.config.logging_config import logging_config
from currency_service.src.infrastructure.config.rmq_config import rmq_config, connection_params

logger = logging_config.get_logger()


def on_request(ch, method, properties, body):
    logger.debug("Method 'on_request' was called")
    asyncio.get_event_loop().run_until_complete(async_on_request(ch, method, properties, body))


async def async_on_request(ch, method, properties, body):
    logger.debug("Method 'async_on_request' was called")
    params = ParseParamsFromRMQString().execute(ParseParamsFromRMQString().Request(params_str=body.decode('utf-8')))

    if params.request_date == "latest":
        logger.warning("'latest' request from RMQ")
        response = (await GetCurrentExchangeRate().execute(GetCurrentExchangeRate.Request(
            base_currency=params.base_currency,
            requested_currencies=params.requested_currencies
        ))).response



    else:
        logger.warning(f"'history' request from RMQ with date '{params.request_date}'")
        response = (await GetExchangeRateHistory().execute(GetExchangeRateHistory.Request(
            base_currency=params.base_currency,
            request_date=params.request_date,
            requested_currencies=params.requested_currencies
        ))).response

    if isinstance(response, ResponseSuccess):
        response_str = response.data.json()

    if isinstance(response, ResponseFailure):
        logger.error(f"ResponseFailure ({response.status_code}, {response.details})")
        response_str = f"ResponseFailure {response.status_code}, {response.details}".encode()

    logger.warning(f"response_str: '{response_str}'")
    logger.debug(f"Sending response from 'async_on_request'")
    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id
        ),
        body=response_str
    )
    logger.debug("Method 'async_on_request' worked successfully")


def start_server():
    connection = pika.BlockingConnection(parameters=connection_params)
    channel = connection.channel()
    channel.queue_declare(queue=rmq_config.RMQ_REQUEST_QUEUE)

    channel.basic_consume(
        queue=rmq_config.RMQ_REQUEST_QUEUE,
        on_message_callback=on_request,
        auto_ack=True
    )
    logger.warning("Awaiting RPC requests")
    channel.start_consuming()
