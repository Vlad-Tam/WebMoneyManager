import pika

RMQ_HOST = "127.0.0.1"
RMQ_PORT = "5672"
RMQ_USER = "guest"
RMQ_PASSWORD = "guest"
RMQ_ROUTING_KEY = "currency"
RMQ_EXCHANGE = ""
RMQ_REQUEST_QUEUE = "request_queue"
RMQ_RESPONSE_QUEUE = "response_queue"

connection_params = pika.ConnectionParameters(
    host=RMQ_HOST,
    port=RMQ_PORT,
    credentials=pika.PlainCredentials(RMQ_USER, RMQ_PASSWORD),
)


def get_connection() -> pika.BlockingConnection:
    return pika.BlockingConnection(
        parameters=connection_params,
    )
