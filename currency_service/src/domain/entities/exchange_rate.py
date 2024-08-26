from datetime import date

from pydantic import BaseModel


class AddExchangeRateDTO(BaseModel):
    base_currency: str
    request_date: date
    rates: dict[str, float]


class ExchangeRateDTO(AddExchangeRateDTO):
    id: int
