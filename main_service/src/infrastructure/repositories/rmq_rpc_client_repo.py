import asyncio
import uuid
from typing import Any

import pika

from main_service.src.infrastructure.config.rmq_config import rmq_config, connection_params


class RPCClientRepo:
    def __init__(self):
        self.connection = pika.BlockingConnection(parameters=connection_params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=rmq_config.RMQ_REQUEST_QUEUE)
        self.channel.queue_declare(queue=rmq_config.RMQ_RESPONSE_QUEUE)

    async def call(self, message) -> Any:
        corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=rmq_config.RMQ_REQUEST_QUEUE,
            properties=pika.BasicProperties(
                reply_to=rmq_config.RMQ_RESPONSE_QUEUE,
                correlation_id=corr_id
            ),
            body=message
        )
        try:
            response = await asyncio.wait_for(self.wait_for_response(corr_id), timeout=15)
        except asyncio.TimeoutError:
            return "timeout"
        return response

    async def wait_for_response(self, corr_id) -> Any:
        response = None

        def on_response(ch, method, properties, body):
            nonlocal response
            if properties.correlation_id == corr_id:
                response = body

        self.channel.basic_consume(
            queue=rmq_config.RMQ_RESPONSE_QUEUE,
            on_message_callback=on_response,
            auto_ack=True
        )
        while response is None:
            self.connection.process_data_events()
            await asyncio.sleep(0.1)
        return response
