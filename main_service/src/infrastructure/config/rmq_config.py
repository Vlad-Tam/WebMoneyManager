from pathlib import Path
from urllib.parse import quote_plus

import pika
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class RMQConfig(BaseSettings):

    def __init__(self):
        config_dir = Path(__file__).parent.parent.parent.parent / 'config'
        dotenv_path = config_dir / 'rmq.env'
        super().__init__(_env_file=dotenv_path)

    RMQ_HOST: str = Field(...)
    RMQ_PORT: str = Field(...)
    RMQ_USER: str = Field(...)
    RMQ_PASSWORD: SecretStr = Field(...)
    RMQ_REQUEST_QUEUE: str = Field(...)
    RMQ_RESPONSE_QUEUE: str = Field(...)

    def get_password(self) -> str:
        return quote_plus(self.RMQ_PASSWORD.get_secret_value())


rmq_config = RMQConfig()


connection_params = pika.ConnectionParameters(
    host=rmq_config.RMQ_HOST,
    port=rmq_config.RMQ_PORT,
    credentials=pika.PlainCredentials(rmq_config.RMQ_USER, rmq_config.get_password()),
)
