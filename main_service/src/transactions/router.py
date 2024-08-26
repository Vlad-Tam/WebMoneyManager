from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from main_service.src.transactions.schemas import TransactionAddDTO
from main_service.src.transactions.repository import TransactionRepository
from main_service.src.utils.logging_config import logger

router = APIRouter(
    prefix="/{user_id}/transactions",
    tags=["Transactions"],
)


@router.get("")
async def get_transactions_list(user_id: int, page: int = 1, page_size: int = 10):
    logger.debug(f"Endpoint GET '/{user_id}/transactions' was called")
    try:
        offset = (page - 1) * page_size
        transactions_list = await TransactionRepository.find_all_by_user_id(user_id, limit=page_size, offset=offset)
        logger.info(f"Endpoint GET '/{user_id}/transactions' worked successfully")
        return {
            "status": "ok",
            "data": {
                "transactions_list": transactions_list,
                "page": page,
                "size": page_size
            },
            "details": None
        }
    except Exception as e:
        logger.error(f"Endpoint GET '/{user_id}/transactions' raised an exception \"{e}\"")
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Something is wrong in get_transactions_list function"
        })


@router.post("")
async def create_new_transaction(user_id: int, transaction: TransactionAddDTO):
    logger.debug(f"Endpoint POST '/{user_id}/transactions' was called")
    try:
        transaction.user_id = user_id
        new_id = await TransactionRepository.add_one(transaction)
        logger.info(f"Endpoint POST '/{user_id}/transactions' worked successfully")
        return {
            "status": "ok",
            "data": {"new_id": new_id},
            "details": None
        }
    except Exception as e:
        logger.error(f"Endpoint POST '/{user_id}/transactions' raised an exception \"{e}\"")
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Something is wrong in create_new_transaction function"
        })


@router.get("/add")
def get_create_transactions_form(user_id: int):
    return f"Transactions /add GET page for {user_id} is in development"


@router.get("/{transaction_id}")
async def get_one_transaction(user_id: int, transaction_id: int):
    logger.debug(f"Endpoint GET '/{user_id}/transactions/{transaction_id}' was called")
    try:
        transaction = await TransactionRepository.find_by_id(user_id, transaction_id)
    except Exception as e:
        logger.error(f"Endpoint GET '/{user_id}/transactions/{transaction_id}' raised an exception \"{e}\"")
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Something is wrong in get_one_transaction function"
        })
    if not transaction:
        warning_message = f"Transaction with ID {transaction_id} not found for user {user_id}"
        logger.warning(f"Endpoint GET '/{user_id}/transactions/{transaction_id}' raised a warning \"{warning_message}\"")
        raise HTTPException(status_code=404, detail={
            "status": "error",
            "data": None,
            "details": warning_message
        })
    logger.info(f"Endpoint GET '/{user_id}/transactions/{transaction_id}' worked successfully")
    return {
        "status": "ok",
        "data": transaction,
        "details": None
    }


@router.delete("/{transaction_id}")
async def delete_transaction(user_id: int, transaction_id: int):
    logger.debug(f"Endpoint DELETE '/{user_id}/transactions/{transaction_id}' was called")
    try:
        deleted_id = await TransactionRepository.delete_by_id(user_id, transaction_id)
    except Exception as e:
        logger.error(f"Endpoint DELETE '/{user_id}/transactions/{transaction_id}' raised an exception \"{e}\"")
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Something is wrong in delete_transaction function"
        })
    if not deleted_id:
        warning_message = f"Transaction with ID {transaction_id} not found for user {user_id}"
        logger.warning(f"Endpoint DELETE '/{user_id}/transactions/{transaction_id}' raised a warning \"{warning_message}\"")
        raise HTTPException(status_code=404, detail={
            "status": "error",
            "data": None,
            "details": warning_message
        })
    logger.info(f"Endpoint DELETE '/{user_id}/transactions/{transaction_id}' worked successfully")
    return {
        "status": "ok",
        "data": {"deleted_id": deleted_id},
        "details": None
    }


@router.put("/{transaction_id}")
async def update_transaction(user_id: int, transaction_id: int, transaction: TransactionAddDTO):
    logger.debug(f"Endpoint PUT '/{user_id}/transactions/{transaction_id}' was called")
    try:
        transaction.user_id = user_id
        await TransactionRepository.update_by_id(user_id, transaction_id, transaction)
        logger.info(f"Endpoint PUT '/{user_id}/transactions/{transaction_id}' worked successfully")
        return {
            "status": "ok",
            "data": {"updated_id": transaction_id},
            "details": None
        }
    except Exception as e:
        logger.error(f"Endpoint PUT '/{user_id}/transactions/{transaction_id}' raised an exception \"{e}\"")
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Something is wrong in update_transaction function"
        })


@router.get("/{transaction_id}/edit")
def get_update_transactions_form(user_id: int, transaction_id: int):
    return f"Transactions GET page for {user_id}:{transaction_id}/edit is in development"
