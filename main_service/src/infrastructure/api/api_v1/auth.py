from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from main_service.src.domain.entities.user import UserRead, UserCreate
from main_service.src.infrastructure.api.dependencies.authentication.backend import (
    authentication_backend,
)
from main_service.src.infrastructure.api.dependencies.authentication.fastapi_usr import (
    fastapi_usr,
)
from main_service.src.infrastructure.api.api_v1.users import router as users_router

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(dependencies=[Depends(http_bearer)])

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

# /login
# /logout
auth_router.include_router(
    router=fastapi_usr.get_auth_router(
        authentication_backend, requires_verification=True
    )
)

# /register
auth_router.include_router(router=fastapi_usr.get_register_router(UserRead, UserCreate))


# /request-verify-token
# /verify
auth_router.include_router(router=fastapi_usr.get_verify_router(UserRead))


# /forgot-password
# /reset-password
auth_router.include_router(router=fastapi_usr.get_reset_password_router())


router.include_router(auth_router)
router.include_router(users_router)
