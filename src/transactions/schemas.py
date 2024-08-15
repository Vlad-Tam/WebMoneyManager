import enum
from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel


class TransactionType(enum.Enum):
    add = "ADD"
    sub = "SUB"


class TransactionAddDTO(BaseModel):
    user_id: int
    category_id: int
    value: Decimal
    description: str
    operation_type: TransactionType
    created_at: datetime


class TransactionDTO(TransactionAddDTO):
    id: int
