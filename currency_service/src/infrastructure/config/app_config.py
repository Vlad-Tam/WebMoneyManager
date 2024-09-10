from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):

    def __init__(self):
        config_dir = Path(__file__).parent.parent.parent.parent / 'config'
        dotenv_path = config_dir / 'app.env'
        super().__init__(_env_file=dotenv_path)

    DEBUG: str = Field(...)

    def get_mode(self) -> bool:
        return self.DEBUG.lower() == 'true'


app_config = AppConfig()
