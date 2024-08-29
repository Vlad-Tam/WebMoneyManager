from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from main_service.src.infrastructure.models.user import UserOrm
from main_service.src.infrastructure.repositories.db_repo import get_session

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_db(
    session: Annotated[
        "AsyncSession",
        Depends(get_session),
    ],
):
    yield UserOrm.get_db(session=session)
