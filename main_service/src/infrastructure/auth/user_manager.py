from typing import Optional, TYPE_CHECKING

from fastapi_users import BaseUserManager, IntegerIDMixin

from main_service.src.infrastructure.config.access_token_config import access_token
from main_service.src.infrastructure.config.logging_config import logging_config
from main_service.src.infrastructure.models.user import UserOrm

if TYPE_CHECKING:
    from fastapi import Request

logger = logging_config.get_logger()


class UserManager(IntegerIDMixin, BaseUserManager[UserOrm, id]):
    reset_password_token_secret = access_token.RESET_PASSWORD_TOKEN_SECRET
    verification_token_secret = access_token.VERIFICATION_TOKEN_SECRET

    async def on_after_register(
        self, user: UserOrm, request: Optional["Request"] = None
    ):
        logger.warning("User %r has registered.", user.id)

    async def on_after_forgot_password(
        self, user: UserOrm, token: str, request: Optional["Request"] = None
    ):
        logger.warning(
            "User %r has forgot their password. Reset token: %r", user.id, token
        )

    async def on_after_request_verify(
        self, user: UserOrm, token: str, request: Optional["Request"] = None
    ):
        logger.warning(
            "Verification requested for user %r. Verification token: %r", user.id, token
        )
