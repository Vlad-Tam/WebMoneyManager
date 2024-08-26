from typing import Optional

from pydantic import BaseModel, constr
from pydantic import field_validator


class GetExchangeRatesValidator(BaseModel):
    base_currency: constr(min_length=3, max_length=3)
    requested_currencies: Optional[list[constr(min_length=3, max_length=3)]]

    @field_validator('requested_currencies')
    def check_currency_length(cls, v):
        if v is not None:
            for el in v:
                if len(el) != 3:
                    raise ValueError('Every currency length must be 3 symbols')
                return v
