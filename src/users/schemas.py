import enum
from datetime import date, datetime

from pydantic import BaseModel


class Currency(enum.Enum):
    byn = "BYN"
    rub = "RUB"
    usd = "USD"
    eur = "EUR"
    cny = "CNY"


class UserAddDTO(BaseModel):
    name: str
    surname: str
    email: str
    password: str
    main_currency: Currency
    birth_date: date
    created_at: datetime


class UserDTO(UserAddDTO):
    id: int
