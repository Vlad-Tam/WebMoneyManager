from typing import Optional, Annotated

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from main_service.src.domain.entities.response import ResponseFailure, ResponseStatus
from main_service.src.domain.usecases.get_homepage_info import GetHomepageInfo
from main_service.src.domain.validators.get_homepage_validator import GetHomepageValidator
from main_service.src.infrastructure.api.dependencies.authentication.fastapi_usr import current_user
from main_service.src.infrastructure.config.logging_config import logging_config
from main_service.src.infrastructure.models.user import UserOrm

router = APIRouter(
    prefix="/home",
    tags=["Home"],
)

logger = logging_config.get_logger()


@router.get("")
async def get_homepage(
        user: Annotated[
            UserOrm,
            Depends(current_user),
        ],
        period: Optional[str] = "month"
):
    logger.debug(f"Endpoint GET '/home' (user_id={user.id}) was called with period={period}")
    try:
        request = GetHomepageValidator(period=period)
    except ValueError as e:
        logger.error(f"Endpoint GET '/home' (user_id={user.id}) raised an exception \"{e}\"")
        raise HTTPException(
            status_code=ResponseStatus.BAD_REQUEST.status_code,
            detail=ResponseStatus.BAD_REQUEST.status_msg
        )
    response = (await GetHomepageInfo().execute(
        GetHomepageInfo.Request(
            user_id=user.id,
            time_period=request.period)
        )
    ).response

    if isinstance(response, ResponseFailure):
        raise HTTPException(status_code=response.status_code, detail=response.details)

    logger.info(f"Endpoint GET '/home' (user_id={user.id}) worked successfully")
    return response

