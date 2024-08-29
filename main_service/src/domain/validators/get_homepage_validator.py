from typing import Optional

from pydantic import BaseModel, field_validator


class GetHomepageValidator(BaseModel):
    period: Optional[str] = "month"

    @field_validator('period')
    def check_period_value(cls, v):
        allowed_values = {'year', 'month', 'week'}
        if v not in allowed_values:
            raise ValueError(f'Invalid period value. Allowed values are: {", ".join(allowed_values)}')
        return v
