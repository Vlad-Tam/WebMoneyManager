import asyncio
import json

import aio_pika
import pika

from currency_service.src.domain.usecases.get_current_exchange_rate import GetCurrentExchangeRate
from currency_service.src.domain.usecases.get_exchange_rate_history import GetExchangeRateHistory
from currency_service.src.infrastructure.config.logging_config import LoggingConfig
from currency_service.src.infrastructure.config.rmq_config import RMQ_REQUEST_QUEUE, connection_params

logger = LoggingConfig().get_logger()


def parse_params_string(params: str):
    parts = params.split(',')

    request_date = parts[0]
    base_currency = parts[1] if len(parts) > 1 else "USD"
    requested_currencies = parts[2].split(';') if len(parts) > 2 and parts[2] else None

    return request_date, base_currency, requested_currencies


def on_request(ch, method, properties, body):
    logger.warning("ON REQUEST")
    asyncio.get_event_loop().run_until_complete(async_on_request(ch, method, properties, body))
    # async_on_request(ch, method, properties, body)


async def async_on_request(ch, method, properties, body):
    logger.warning("ASYNC ON REQUEST")
    request_date, base_currency, requested_currencies = parse_params_string(body.decode('utf-8'))
    if request_date == "latest":
        logger.warning("LATEST RMQ REQUEST")
        response = (await GetCurrentExchangeRate().execute(GetCurrentExchangeRate.Request(
            base_currency=base_currency,
            requested_currencies=requested_currencies
        ))).response
        response_str = str(response)
        # response = "rere"
    else:
        logger.warning("HISTORY RMQ REQUEST")
        logger.warning(base_currency)
        logger.warning(request_date)
        logger.warning(requested_currencies)
        response = (await GetExchangeRateHistory().execute(GetExchangeRateHistory.Request(
            base_currency=base_currency,
            request_date=request_date,
            requested_currencies=requested_currencies
        ))).response

        response_str = response.data.json()
        # response = "rere2"
    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id
        ),
        body=response_str
    )


def start_server():
    connection = pika.BlockingConnection(parameters=connection_params)
    channel = connection.channel()
    channel.queue_declare(queue=RMQ_REQUEST_QUEUE)

    channel.basic_consume(
        queue=RMQ_REQUEST_QUEUE,
        on_message_callback=on_request,
        auto_ack=True
    )
    print("Awaiting RPC requests")
    channel.start_consuming()
