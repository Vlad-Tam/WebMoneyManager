import asyncio
import contextlib
from typing import Optional

from fastapi_users.exceptions import UserAlreadyExists

from main_service.src.domain.entities.user import UserCreate
from main_service.src.infrastructure.api.dependencies.authentication.user import (
    get_user_db,
)
from main_service.src.infrastructure.api.dependencies.authentication.user_manager import (
    get_user_manager,
)
from main_service.src.infrastructure.auth.user_manager import UserManager
from main_service.src.infrastructure.models.user import UserOrm
from main_service.src.infrastructure.repositories.db_repo import database_repository

default_name = "admin"
default_surname = "admin"
default_main_currency = "USD"
default_month_limit = None
default_birth_date = "2000-01-01"
default_email = "admin@email.com"
default_password = "admin"
default_is_active = True
default_is_superuser = True
default_is_verified = True

get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(user_manager: UserManager, user_create: UserCreate) -> UserOrm:
    user = await user_manager.create(user_create=user_create, safe=False)
    return user


async def create_superuser(
    name: str = default_name,
    surname: str = default_surname,
    main_currency: str = default_main_currency,
    month_limit: Optional[str] = default_month_limit,
    birth_date: str = default_birth_date,
    email: str = default_email,
    password: str = default_password,
    is_active: bool = default_is_active,
    is_superuser: bool = default_is_superuser,
    is_verified: bool = default_is_verified,
):
    user_create = UserCreate(
        name=name,
        surname=surname,
        password=password,
        main_currency=main_currency,
        month_limit=month_limit,
        birth_date=birth_date,
        email=email,
        is_active=is_active,
        is_superuser=is_superuser,
        is_verified=is_verified,
    )
    try:
        async with database_repository.a_sessionmaker() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    return await create_user(
                        user_manager=user_manager,
                        user_create=user_create,
                    )

    except UserAlreadyExists:
        print(f"User {email} already exists")
        raise


if __name__ == "__main__":
    asyncio.run(create_superuser())
