import enum
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class Currency(enum.Enum):
    byn = "BYN"
    rub = "RUB"
    usd = "USD"
    eur = "EUR"
    cny = "CNY"


class UserAddDTO(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    main_currency: Currency
    month_limit: Optional[float]
    birth_date: date


class UserDTO(UserAddDTO):
    id: int
    created_at: datetime
