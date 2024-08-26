from typing import Optional

from main_service.src.home.repository import HomeRepository
from main_service.src.utils.logging_config import logger


async def get_homepage_info(user_id: int, time_period: Optional[str] = "month"):
    db_data = await HomeRepository.get_homepage_info(user_id, time_period)

    warnings = []

    last_spending = {
        "value": db_data["last_spending_value"],
        "description": db_data["last_spending_description"],
        "time": db_data["last_spending_time"]
    } if db_data["last_spending_value"] is not None or db_data["last_spending_time"] is not None else None

    current_sub = 0 if db_data["current_sub"] is None else db_data["current_sub"]
    current_balance = 0 if db_data["current_balance"] is None else db_data["current_balance"]

    if current_balance < 0:
        warnings.append("Balance is negative")

    if db_data["month_limit"] is not None:
        if db_data["current_month_sub"] > db_data["month_limit"]:
            warnings.append("Monthly limit exceeded")

    return {
        "name": db_data["name"],
        "surname": db_data["surname"],
        "email": db_data["email"],
        "main_currency": db_data["main_currency"],
        "month_limit": db_data["month_limit"],
        "birth_date": db_data["birth_date"],
        "current_sub": current_sub,
        "current_balance": current_balance,
        "last_spending": last_spending,
        "warnings": warnings
    }
