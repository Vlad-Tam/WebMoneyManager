from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class AccessToken(BaseSettings):

    def __init__(self):
        config_dir = Path(__file__).parent.parent.parent.parent / "config"
        dotenv_path = config_dir / "auth.env"
        super().__init__(_env_file=dotenv_path)

    lifetime_seconds: int = 3600
    RESET_PASSWORD_TOKEN_SECRET: str = Field(...)
    VERIFICATION_TOKEN_SECRET: str = Field(...)


access_token = AccessToken()
