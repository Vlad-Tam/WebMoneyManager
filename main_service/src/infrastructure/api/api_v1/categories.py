from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from main_service.src.domain.entities.category import CategoryAddDTO
from main_service.src.infrastructure.api.dependencies.authentication.fastapi_usr import current_user
from main_service.src.infrastructure.models.user import UserOrm
from main_service.src.infrastructure.repositories.category_repo import (
    CategoryRepository,
)
from main_service.src.infrastructure.config.logging_config import logging_config

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)

logger = logging_config.get_logger()


@router.get("")
async def get_categories_list(
        user: Annotated[
            UserOrm,
            Depends(current_user),
        ],
        page: int = 1,
        page_size: int = 10
):
    logger.debug(f"Endpoint GET '/categories' (user_id={user.id}) was called")
    try:
        offset = (page - 1) * page_size
        categories_list = await CategoryRepository.find_all_by_user_id(
            user.id, limit=page_size, offset=offset
        )
        logger.info(f"Endpoint GET '/categories' (user_id={user.id}) worked successfully")
        return {
            "status": "ok",
            "data": {
                "categories_list": categories_list,
                "page": page,
                "size": page_size,
            },
            "details": None,
        }
    except Exception as e:
        logger.error(
            f"Endpoint GET '/categories' (user_id={user.id}) raised an exception \"{e}\""
        )
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "data": None,
                "details": "Something is wrong in get_categories_list function",
            },
        )


@router.post("")
async def create_new_category(
        user: Annotated[
            UserOrm,
            Depends(current_user),
        ],
        category: CategoryAddDTO
):
    logger.debug(f"Endpoint POST '/categories' (user_id={user.id}) was called")
    try:
        category.user_id = user.id
        new_id = await CategoryRepository.add_one(category)
        logger.info(f"Endpoint POST '/categories' (user_id={user.id}) worked successfully")
        return {
            "status": "ok",
            "data": {
                "new_id": new_id
            },
            "details": None
        }
    except Exception as e:
        logger.error(
            f"Endpoint POST '/categories' (user_id={user.id}) raised an exception \"{e}\""
        )
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "data": None,
                "details": "Something is wrong in create_new_category function",
            },
        )


@router.get("/add")
def get_create_categories_form():
    return f"Categories /add GET page is in development"


@router.get("{/category_id}")
async def get_one_category(
        user: Annotated[
            UserOrm,
            Depends(current_user),
        ],
        category_id: int
):
    logger.debug(f"Endpoint GET '/categories/{category_id}' (user_id={user.id}) was called")
    try:
        category = await CategoryRepository.find_by_id(user.id, category_id)
    except Exception as e:
        logger.error(
            f"Endpoint GET '/categories/{category_id}' (user_id={user.id}) raised an exception \"{e}\""
        )
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "data": None,
                "details": "Something is wrong in get_one_category function",
            },
        )
    if not category:
        warning_message = f"Category with ID {category_id} not found for user {user.id}"
        logger.warning(
            f"Endpoint GET '/categories/{category_id}' (user_id={user.id}) raised a warning \"{warning_message}\""
        )
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "data": None,
                "details": warning_message
            },
        )
    logger.info(f"Endpoint GET '/categories/{category_id}' (user_id={user.id}) worked successfully")
    return {
        "status": "ok",
        "data": category,
        "details": None
    }


@router.delete("{/category_id}")
async def delete_category(
        user: Annotated[
            UserOrm,
            Depends(current_user),
        ],
        category_id: int
):
    logger.debug(f"Endpoint DELETE '/categories/{category_id}' (user_id={user.id}) was called")
    try:
        deleted_id = await CategoryRepository.delete_by_id(user.id, category_id)
    except Exception as e:
        logger.error(f"Endpoint DELETE '/categories/{category_id}' (user_id={user.id}) raised an exception \"{e}\"")
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "data": None,
                "details": "Something is wrong in delete_category function",
            },
        )
    if not deleted_id:
        warning_message = f"Category with ID {category_id} not found for user {user.id}"
        logger.warning(
            f"Endpoint DELETE '/categories/{category_id}' (user_id={user.id}) raised a warning \"{warning_message}\""
        )
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "data": None,
                "details": warning_message
            },
        )
    logger.info(f"Endpoint DELETE '/categories/{category_id}' (user_id={user.id}) worked successfully")
    return {
        "status": "ok",
        "data": {
            "deleted_id": deleted_id
        },
        "details": None
    }


@router.put("{/category_id}")
async def update_category(
        user: Annotated[
            UserOrm,
            Depends(current_user),
        ],
        category_id: int,
        category: CategoryAddDTO
):
    logger.debug(f"Endpoint PUT '/categories/{category_id}' (user_id={user.id}) was called")
    try:
        category.user_id = user.id
        await CategoryRepository.update_by_id(user.id, category_id, category)
        logger.info(
            f"Endpoint PUT '/categories/{category_id}' (user_id={user.id}) worked successfully"
        )
        return {
            "status": "ok",
            "data": {
                "updated_id": category_id
            },
            "details": None
        }
    except Exception as e:
        logger.error(
            f"Endpoint PUT '/categories/{category_id}' (user_id={user.id}) raised an exception \"{e}\""
        )
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "data": None,
                "details": "Something is wrong in update_category function",
            },
        )


@router.get("{/category_id}/edit")
def get_update_categories_form(category_id: int):
    return f"Categories GET page for /categories/{category_id}/edit is in development"
