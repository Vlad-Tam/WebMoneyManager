from pathlib import Path
from urllib.parse import quote_plus

from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings


class DBConfig(BaseSettings):

    def __init__(self):
        config_dir = Path(__file__).parent.parent.parent.parent / "config"
        dotenv_path = config_dir / "db.env"
        super().__init__(_env_file=dotenv_path)

    DB_HOST: str = Field(...)
    DB_PORT: int = Field(...)
    DB_NAME: str = Field(...)
    DB_USER: str = Field(...)
    DB_PASS: SecretStr = Field(...)
    DB_DRIVER: str = Field(...)

    def get_db_url(self):
        password = quote_plus(self.DB_PASS.get_secret_value())
        return f"{self.DB_DRIVER}://{self.DB_USER}:{password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


db_config = DBConfig()
