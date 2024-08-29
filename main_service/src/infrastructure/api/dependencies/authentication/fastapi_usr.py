from fastapi_users import FastAPIUsers

from main_service.src.infrastructure.api.dependencies.authentication.backend import (
    authentication_backend,
)
from main_service.src.infrastructure.api.dependencies.authentication.user_manager import (
    get_user_manager,
)
from main_service.src.infrastructure.models.user import UserOrm

fastapi_usr = FastAPIUsers[UserOrm, int](
    get_user_manager,
    [authentication_backend],
)

current_user = fastapi_usr.current_user(active=True)
