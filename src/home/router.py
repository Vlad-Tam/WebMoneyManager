from fastapi import APIRouter

router = APIRouter(
    prefix="/{user_id}/home",
    tags=["Home"],
)


@router.get("")
def get_homepage(user_id: int):
    return f"Homepage for {user_id} is in development"
