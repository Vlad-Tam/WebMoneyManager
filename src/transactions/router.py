from fastapi import APIRouter

router = APIRouter(
    prefix="/{user_id}/transactions",
    tags=["Transactions"],
)


@router.get("")
def get_transactions_list(user_id: int):
    return f"Transactions GET page for {user_id} is in development"


@router.post("")
def create_new_transaction(user_id: int):
    return f"Transactions POST page for {user_id} is in development"


@router.get("/add")
def get_create_transactions_form(user_id: int):
    return f"Transactions /add GET page for {user_id} is in development"


@router.get("/{transaction_id}")
def get_one_transaction(user_id: int, transaction_id: int):
    return f"Transactions GET page for {user_id}:{transaction_id} is in development"


@router.delete("/{transaction_id}")
def delete_transaction(user_id: int, transaction_id: int):
    return f"Transactions DELETE page for {user_id}:{transaction_id} is in development"


@router.put("/{transaction_id}")
def update_transaction(user_id: int, transaction_id: int):
    return f"Transactions UPDATE page for {user_id}:{transaction_id} is in development"


@router.get("/{transaction_id}/edit")
def get_update_transactions_form(user_id: int, transaction_id: int):
    return f"Transactions GET page for {user_id}:{transaction_id}/edit is in development"
