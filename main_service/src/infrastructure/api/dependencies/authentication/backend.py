from fastapi_users.authentication import AuthenticationBackend

from main_service.src.infrastructure.api.dependencies.authentication.strategy import (
    get_database_strategy,
)
from main_service.src.infrastructure.auth.transport import bearer_transport

authentication_backend = AuthenticationBackend(
    name="access-token-db",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)
