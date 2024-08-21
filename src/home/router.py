from typing import Optional

from fastapi import APIRouter

from src.home.service import get_homepage_info
from src.utils.logging_config import logger
from fastapi.exceptions import HTTPException

router = APIRouter(
    prefix="/{user_id}/home",
    tags=["Home"],
)


@router.get("")
async def get_homepage(user_id: int, period: Optional[str] = "month"):
    logger.debug(f"Endpoint GET '/{user_id}/home' was called with period={period}")
    try:
        data = await get_homepage_info(user_id, period)
        logger.info(f"Endpoint GET '/{user_id}/home' worked successfully")
        return {
            "status": "ok",
            "data": data,
            "details": None
        }
    except Exception as e:
        logger.error(f"Endpoint GET '/{user_id}/home' raised an exception \"{e}\"")
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Something is wrong in get_homepage function"
        })
