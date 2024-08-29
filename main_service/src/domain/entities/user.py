import enum
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from fastapi_users import schemas


class Currency(enum.Enum):
    byn = "BYN"
    rub = "RUB"
    usd = "USD"
    eur = "EUR"
    cny = "CNY"


class UserRead(schemas.BaseUser[int]):
    name: str
    surname: str
    main_currency: Currency
    month_limit: Optional[float]
    birth_date: date
    created_at: datetime


class UserCreate(schemas.BaseUserCreate):
    name: str
    surname: str
    password: str
    main_currency: Currency
    month_limit: Optional[float]
    birth_date: date


class UserUpdate(schemas.BaseUserUpdate):
    name: str
    surname: str
    password: str
    main_currency: Currency
    month_limit: Optional[float]
    birth_date: date
    created_at: datetime
