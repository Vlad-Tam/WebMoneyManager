from pathlib import Path
from urllib.parse import quote_plus

from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings


class APIConfig(BaseSettings):

    def __init__(self):
        config_dir = Path(__file__).parent.parent.parent.parent / 'config'
        dotenv_path = config_dir / 'api.env'
        super().__init__(_env_file=dotenv_path)

    API_TOKEN: SecretStr = Field(...)
    API_PATH: str = Field(...)

    def get_api_token(self):
        token = quote_plus(self.API_TOKEN.get_secret_value())
        return token

    def get_api_path(self):
        return self.API_PATH
