import fastapi_users.router
from fastapi import APIRouter

from main_service.src.domain.entities.user import UserCreate, UserRead
from main_service.src.infrastructure.api.dependencies.authentication.fastapi_usr import (
    fastapi_usr,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

# /me
# /id
router.include_router(
    router=fastapi_usr.get_users_router(
        UserRead,
        UserCreate,
    )
)
