from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from src.transactions.schemas import TransactionAddDTO
from src.transactions.service import TransactionRepository
from src.utils.logging_config import logger

router = APIRouter(
    prefix="/{user_id}/transactions",
    tags=["Transactions"],
)


@router.get("")
async def get_transactions_list(user_id: int):
    logger.debug(f"Endpoint '/{user_id}/transactions' was called")
    try:
        transactions_list = await TransactionRepository.find_all_by_user_id(user_id)
        logger.info(f"Endpoint '/{user_id}/transactions' worked successfully")
        return {
            "status": "ok",
            "data": transactions_list,
            "details": None
        }
    except Exception as e:
        logger.warning(f"Endpoint '/{user_id}/transactions' raised an exception {type(e).__name__}")
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Something is wrong in get_transactions_list function"
        })


@router.post("")
async def create_new_transaction(user_id: int, transaction: TransactionAddDTO):
    try:
        transaction.user_id = user_id
        new_id = await TransactionRepository.add_one(transaction)
        return {
            "status": "ok",
            "data": {"new_id": new_id},
            "details": None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Something is wrong in create_new_transaction function"
        })


@router.get("/add")
def get_create_transactions_form(user_id: int):
    return f"Transactions /add GET page for {user_id} is in development"


@router.get("/{transaction_id}")
async def get_one_transaction(user_id: int, transaction_id: int):
    try:
        transaction = await TransactionRepository.find_by_id(user_id, transaction_id)
        if not transaction:
            raise HTTPException(status_code=404, detail={
                "status": "error",
                "data": None,
                "details": f"Transaction with ID {transaction_id} not found for user {user_id}"
            })
        return {
            "status": "ok",
            "data": transaction,
            "details": None
        }
    except Exception as e:
        logger.warning(f"Endpoint '/{user_id}/transactions/{transaction_id}' raised an exception {type(e).__name__}")
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": f"Something is wrong in get_one_transaction function"
        })


@router.delete("/{transaction_id}")
def delete_transaction(user_id: int, transaction_id: int):
    return f"Transactions DELETE page for {user_id}:{transaction_id} is in development"


@router.put("/{transaction_id}")
def update_transaction(user_id: int, transaction_id: int):
    return f"Transactions UPDATE page for {user_id}:{transaction_id} is in development"


@router.get("/{transaction_id}/edit")
def get_update_transactions_form(user_id: int, transaction_id: int):
    return f"Transactions GET page for {user_id}:{transaction_id}/edit is in development"
