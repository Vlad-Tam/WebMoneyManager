from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel


class TransactionAddDTO(BaseModel):
    user_id: int
    category_id: int
    value: Decimal
    description: str
    created_at: datetime


class TransactionDTO(TransactionAddDTO):
    id: int
