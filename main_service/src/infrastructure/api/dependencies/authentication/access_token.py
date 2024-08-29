from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from main_service.src.infrastructure.models.access_token import AccessTokenOrm
from main_service.src.infrastructure.repositories.db_repo import get_session

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_access_token_db(
    session: Annotated[
        "AsyncSession",
        Depends(get_session),
    ],
):
    yield AccessTokenOrm.get_db(session=session)
