from typing import Annotated, TYPE_CHECKING

from fastapi import Depends

from main_service.src.infrastructure.api.dependencies.authentication.user import (
    get_user_db,
)
from main_service.src.infrastructure.auth.user_manager import UserManager

if TYPE_CHECKING:
    from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase


async def get_user_manager(
    user_db: Annotated["SQLAlchemyUserDatabase", Depends(get_user_db)]
):
    yield UserManager(user_db)
