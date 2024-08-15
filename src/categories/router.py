from fastapi import APIRouter

router = APIRouter(
    prefix="/{user_id}/categories",
    tags=["Categories"],
)


@router.get("")
def get_categories(user_id: int):
    return f"Categories GET page for {user_id} is in development"


@router.post("")
def create_new_category(user_id: int):
    return f"Categories POST page for {user_id} is in development"


@router.get("/add")
def get_create_categories_form(user_id: int):
    return f"Categories /add GET page for {user_id} is in development"


@router.get("{/category_id}")
def get_one_category(user_id: int, category_id: int):
    return f"Categories GET page for {user_id}:{category_id} is in development"


@router.delete("{/category_id}")
def delete_category(user_id: int, category_id: int):
    return f"Categories DELETE page for {user_id}:{category_id} is in development"


@router.put("{/category_id}")
def update_category(user_id: int, category_id: int):
    return f"Categories UPDATE page for {user_id}:{category_id} is in development"


@router.get("{/category_id}/edit")
def get_update_categories_form(user_id: int, category_id: int):
    return f"Categories GET page for {user_id}:{category_id}/edit is in development"
