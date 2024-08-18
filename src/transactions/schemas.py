import enum
from decimal import Decimal
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TransactionType(enum.Enum):
    add = "ADD"
    sub = "SUB"


class TransactionAddDTO(BaseModel):
    user_id: int
    category_id: int
    value: Decimal
    description: Optional[str]
    operation_type: TransactionType


class TransactionDTO(TransactionAddDTO):
    id: int
    created_at: datetime
