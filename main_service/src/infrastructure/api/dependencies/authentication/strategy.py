from typing import Annotated

from fastapi import Depends
from fastapi_users.authentication.strategy import AccessTokenDatabase
from fastapi_users.authentication.strategy import DatabaseStrategy

from main_service.src.infrastructure.api.dependencies.authentication.access_token import (
    get_access_token_db,
)
from main_service.src.infrastructure.config.access_token_config import access_token
from main_service.src.infrastructure.models.access_token import AccessTokenOrm


def get_database_strategy(
    access_token_db: Annotated[
        AccessTokenDatabase[AccessTokenOrm],
        Depends(get_access_token_db),
    ],
) -> DatabaseStrategy:
    return DatabaseStrategy(
        database=access_token_db, lifetime_seconds=access_token.lifetime_seconds
    )
