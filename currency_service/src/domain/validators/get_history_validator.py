from datetime import datetime
from typing import Optional

from pydantic import constr, field_validator, BaseModel


class GetHistoryValidator(BaseModel):
    base_currency: constr(min_length=3, max_length=3)
    requested_currencies: Optional[list[constr(min_length=3, max_length=3)]]
    request_date: str

    @field_validator('request_date')
    def check_date_format(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Invalid date format. Expected "YYYY-MM-DD"')

    @field_validator('requested_currencies')
    def check_currency_length(cls, v):
        if v is not None:
            for el in v:
                if len(el) != 3:
                    raise ValueError('Every currency length must be 3 symbols')
                return v